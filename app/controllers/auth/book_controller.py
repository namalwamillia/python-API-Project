from flask import Blueprint, request, jsonify

from app import db
from datetime import datetime
from app.models.books import Book
from flask_jwt_extended import create_access_token

# Define Blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')

# Create a Book (POST)
@books.route('/', methods=['POST'])
def create_book():
    try:
        # Extract data from request (using `get_json` for proper parsing)
        data = request.get_json()

        # Basic input validation
        required_fields = ['title', 'pages', 'price', 'price_unit', 'publication_date',
                           'isbn', 'genre', 'description', 'company_id', 'user_id']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "All required fields are missing"}), 400

        # Create a new book
        new_book = Book(
            title=data['title'],
            pages=data['pages'],
            price=data['price'],
            price_unit=data['price_unit'],
            publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date(),  # Parse date string
            isbn=data['isbn'],
            genre=data['genre'],
            description=data['description'],
            image=data['image'] if data.get('image') else None,  # Handle optional image
            company_id=data['company_id'],
            user_id=data['user_id']
        )

        # Add and commit to database
        db.session.add(new_book)
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Book '{new_book.title}' has been created"}), 201

    except Exception as e:
        # Handle exceptions appropriately (e.g., database errors, validation errors)
        return jsonify({"error": str(e)}), 500

# ... (Other routes for GET, PUT, DELETE operations for books, if needed)


# Search Books (GET) with Access Token
@books.route('/', methods=['GET'])
def search_books():
    try:
        # Extract query parameters (optional)
        title = request.args.get('title')
        genre = request.args.get('genre')

        # Build query based on parameters
        query = Book.query
        if title:
            query = query.filter(Book.title.like("%" + title + "%"))
        if genre:
            query = query.filter(Book.genre == genre)

        # Execute query and fetch books
        books = query.all()

        # Build response data with access token for each book (if user is authenticated)
        book_data = []
        current_user = get_jwt_identity()

        for book in books:
            access_token = None
            if current_user: 
                try:
                    access_token = create_access_token(identity=book.id)
                except Exception as e: 
                    print(f"Error creating access token for book {book.id}: {str(e)}")

            book_data.append({
                "id": book.id,
                "title": book.title,
                "genre": book.genre,
                "access_token": access_token,  # Include access token if available
            
            })

        return jsonify({"books": book_data}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")  
        return jsonify({"error": "Internal server error"}), 500
