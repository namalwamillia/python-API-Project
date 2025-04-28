from flask import Blueprint, request, jsonify
from app.models.users import User
from extensions import db
from app.models.products import Product
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.decorators import admin_required  # Import the admin_required decorator
from datetime import datetime

product_bp = Blueprint('product', __name__)

# Get all products (public)
@product_bp.route('/', methods=['GET'])
def get_all_products():
    try:
        products = Product.query.all()
        return jsonify([{
            'id': product.id,
            'category': product.category,
            'name': product.name,
            'status': product.status,
            'price': product.price,
            'description': product.description,
            'details': product.details,
            'image': product.image,
            'rating': product.rating,
            'total_balance': product.total_balance,
            'created_at': product.created_at.isoformat()
        } for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a single product by ID (public)
@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify({
            'id': product.id,
            'category': product.category,
            'name': product.name,
            'status': product.status,
            'price': product.price,
            'description': product.description,
            'details': product.details,
            'image': product.image,
            'rating': product.rating,
            'total_balance': product.total_balance,
            'created_at': product.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@product_bp.route('/products', methods=['POST'])
@admin_required  # ✅ This restricts it to admin users only
def create_product():

    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        # Optional: If you only want logged-in users (not specifically admins), REMOVE the admin check
        # if user.role != 'admin':
        #     return jsonify({'message': 'Admin access required'}), 403

        data = request.get_json()
        # Example product fields:
        category = data.get('category')
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        status = data.get('status')
        details = data.get('details')
        image = data.get('image')
        rating = data.get('rating')
        total_balance = data.get('total_balance')

        if not all([category, name, price]):
            return jsonify({'error': 'Category, name, and price are required'}), 400

        new_product = Product(
            category=category,
            name=name,
            price=price,
            description=description,
            status=status,
            details=details,
            image=image,
            rating=rating,
            total_balance=total_balance
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a product (admin only)
@product_bp.route('/<int:id>', methods=['PUT'])
@admin_required  # Use admin_required instead of jwt_required
def update_product(id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()

        # Update fields if provided
        product.category = data.get('category', product.category)
        product.name = data.get('name', product.name)
        product.status = data.get('status', product.status).lower().strip()  # Normalize status
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        product.details = data.get('details', product.details)
        product.image = data.get('image', product.image)
        product.rating = data.get('rating', product.rating)
        product.total_balance = data.get('total_balance', product.total_balance)

        # Validate required fields
        if not all([product.category, product.name, product.price]):
            return jsonify({'error': 'Category, name, and price are required'}), 400

        # Validate price and numerical fields
        try:
            product.price = float(product.price)
            product.rating = float(product.rating)
            product.total_balance = float(product.total_balance)
        except (ValueError, TypeError):
            return jsonify({'error': 'Price, rating, and total_balance must be numbers'}), 400

        if product.price < 0 or product.rating < 0 or product.total_balance < 0:
            return jsonify({'error': 'Price, rating, and total_balance must be non-negative'}), 400

        # Validate status
        valid_statuses = ['available', 'out_of_stock']
        if product.status not in valid_statuses:
            return jsonify({'error': f'Status must be one of {valid_statuses}'}), 400

        db.session.commit()

        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'category': product.category,
                'name': product.name,
                'status': product.status,
                'price': product.price,
                'description': product.description,
                'details': product.details,
                'image': product.image,
                'rating': product.rating,
                'total_balance': product.total_balance,
                'created_at': product.created_at.isoformat()
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a product (admin only)
@product_bp.route('/<int:id>', methods=['DELETE'])
@admin_required  # Use admin_required instead of jwt_required
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500