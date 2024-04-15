from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app import db
from datetime import datetime
from app.models.books import Book
from app.models.companies import Company  # Assuming Company is imported
from flask_jwt_extended import jwt_required
from traceback import print_exc

from collections.abc import Mapping  # Import Mapping explicitly



# Define Blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')

#create a book
@books.route('/', methods=['POST'])
def create_book():
    try:
        # Extract data from request
        data = request.get_json()

        # Basic input validation
        required_fields = ['title', 'pages', 'price', 'price_unit', 'publication_date',
                           'isbn', 'genre', 'description', 'company_id', 'user_id']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "All required fields are missing"}), 400

        # Validate company ID
        company = Company.query.get(data['company_id'])
        if not company:
            error_message = "Invalid company ID"
            raise Exception(error_message)

        # Validate publication date format
        try:
            publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid publication date format (YYYY-MM-DD)"}), 400

        # Create a new book
        new_book = Book(
            title=data['title'],
            pages=data['pages'],
            price=data['price'],
            price_unit=data['price_unit'],
            publication_date=publication_date,
            isbn=data['isbn'],
            genre=data['genre'],
            description=data['description'],
            image=data.get('image'),  # Handle optional image
            company_id=data['company_id'],
            user_id=data['user_id']
        )

        # Add and commit to database
        db.session.add(new_book)
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Book '{new_book.title}' has been created"}), 201

    except IntegrityError as e:
        print(f"Database integrity error: {str(e)}")
        return jsonify({"error": "An error occurred during book creation. Please check the provided data."}), 400

    except ValueError as e:  # Catch potential value parsing errors
        print(f"Value parsing error: {str(e)}")
        return jsonify({"error": "Invalid data format. Please refer to the API documentation."}), 400

    except Exception as e:  # Fallback for unexpected errors
        print(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    
# Search Books (GET) with Access Token
@books.route('/', methods=['GET'])
@jwt_required(optional=True)  # Allow the request without JWT (optional)
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
                "access_token": access_token,
            })

        return jsonify({"books": book_data}), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Delete a Book (DELETE)
@books.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Fetch book by ID (using book_id from route arguments)
        book = Book.query.get(book_id)

        # Check if book exists
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Authorization check (optional)
        # You can perform additional authorization checks here
        # (e.g., verify user ownership or admin privileges)

        # Delete book
        db.session.delete(book)
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Book '{book.title}' has been deleted"}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Update a Book (PUT)
@books.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        # Fetch book by ID (using book_id from route arguments)
        book = Book.query.get(book_id)

        # Check if book exists
        if not book:
            return jsonify({"error":
 "Book not found"}), 404

        # Authorization check (optional)
        # You can perform additional authorization checks here
        # (e.g., verify user ownership or admin privileges)

        # Extract data from request (using `get_json` for proper parsing)
        data = request.get_json()

        # Update book fields (using dictionary unpacking if data is provided)
        if data:
            for key, value in data.items():
                setattr(book, key, value)  # Update attributes dynamically

        # Commit changes to the database
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Book '{book.title}' has been updated"}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Get a Specific Book (GET)
@books.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        # Fetch book by ID from the database
        book = Book.query.get(book_id)

        # Check if book exists
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Build response data with basic book information
        book_data = {
    "id": book.id,
    "title": book.title,
    # "author": book.author,  # Remove this line if author is not relevant
    "genre": book.genre,
    "description": book.description,
    "publication_date": book.publication_date.strftime("%Y-%m-%d"),
    "image": book.image,
}


        # Return book data
        return jsonify(book_data), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()  # Print the full traceback for debugging
    return jsonify({"error": "Internal server error"}), 500

