from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from app import db
from datetime import datetime
from app.models.books import Book
from app.models.companies import Company
import logging  # Import for error logging

# Define Blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')


@books.route('/register', methods=['POST'])
@jwt_required()
def create_book():
    try:
        data = request.get_json()

        required_fields = ['title', 'pages', 'price', 'price_unit',
                           'publication_date', 'isbn', 'genre', 'description',
                           'company_id', 'user_id']

        # Check for missing required fields
        if not all(field in data for field in required_fields):
            return jsonify({"error": "All required fields are missing"}), 422

        # Extract data from request
        title = data['title']
        pages = data['pages']
        price = data['price']
        price_unit = data['price_unit']
        publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d').date()
        isbn = data['isbn']
        genre = data['genre']
        description = data['description']
        image = data.get('image')  # Optional image field
        company_id = data['company_id']
        user_id = data['user_id']

        # Create a new book instance
        new_book = Book(title=title, pages=pages, price=price, price_unit=price_unit,
                        publication_date=publication_date, isbn=isbn, genre=genre,
                        description=description, image=image, company_id=company_id,
                        user_id=user_id)

        # Add the book to the database session
        db.session.add(new_book)

        # Commit changes to the database
        db.session.commit()

        # Return success message with the book ID
        return jsonify({"message": f"Book '{new_book.title}' has been created",
                       "book_id": new_book.id}), 201

    except IntegrityError as e:
        # Log the error for debugging
        logging.error(f"Database integrity error: {str(e)}")
        # Return specific error message based on constraint violation
        return jsonify({"error": f"An error occurred creating the book: {e.constraint}"}), 400

    except ValueError as e:
        # Log the error for debugging
        logging.error(f"Value parsing error: {str(e)}")
        # Return error message for invalid data format
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400

    except Exception as e:
        # Log the error for debugging
        logging.error(f"An unexpected error occurred: {str(e)}")
        # Return generic error message (improve later for better user feedback)
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
            # "author": book.author,  # Optional: Remove if author is not relevant
            "genre": book.genre,
            "description": book.description,
            "publication_date": book.publication_date.strftime("%Y-%m-%d"),
            "image": book.image,
        }

        # Return book data
        return jsonify(book_data), 200

    except Exception as e:
        # Log the error for better debugging (use a logging library)
        print(f"An error occurred: {str(e)}")
        # Consider providing more specific error messages based on the exception type
        return jsonify({"error": "Internal server error"}), 500