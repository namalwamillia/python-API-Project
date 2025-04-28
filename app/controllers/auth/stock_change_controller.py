# from flask import Blueprint, jsonify, request
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from extensions import db
# from app.models.inventory_management import InventoryManagement
# from app.models.stock_changes import StockChange
# from app.models.users import User

# stock_change_bp = Blueprint('stock_change', __name__, url_prefix='/admin/stock-changes')

# def admin_required(fn):
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
#         if user.role != 'admin':
#             return jsonify({'message': 'Admin access required'}), 403
#         return fn(*args, **kwargs)
#     return wrapper

# @stock_change_bp.route('/', methods=['GET'])
# @admin_required
# def get_stock_changes():
#     inventory_management_id = request.args.get('inventory_management_id', type=int)
#     query = StockChange.query

#     if inventory_management_id:
#         query = query.filter_by(inventory_management_id=inventory_management_id)

#     stock_changes = query.all()
#     return jsonify([{
#         'id': change.id,
#         'inventory_management_id': change.inventory_management_id,
#         'product_name': change.inventory_management.product.name,
#         'change_type': change.change_type,
#         'change_amount': change.change_amount,
#         'direction': change.get_direction(),
#         'notes': change.notes,
#         'created_at': change.created_at.isoformat()
#     } for change in stock_changes]), 200

# @stock_change_bp.route('/', methods=['POST'])
# @admin_required
# def create_stock_change():
#     data = request.get_json()
#     inventory_management_id = data.get('inventory_management_id')
#     change_type = data.get('change_type')
#     change_amount = data.get('change_amount')
#     notes = data.get('notes')  # Optional notes

#     if not all([inventory_management_id, change_type, change_amount]):
#         return jsonify({'message': 'inventory_management_id, change_type, and change_amount are required'}), 400

#     inventory = InventoryManagement.query.get_or_404(inventory_management_id)

#     try:
#         # Update the stock quantity in InventoryManagement
#         inventory.update_stock(change_amount, change_type)
#         return jsonify({
#             'message': 'Stock change created successfully',
#             'new_quantity': inventory.current_quantity
#         }), 201
#     except ValueError as e:
#         return jsonify({'message': str(e)}), 400

# @stock_change_bp.route('/<int:stock_change_id>', methods=['DELETE'])
# @admin_required
# def delete_stock_change(stock_change_id):
#     stock_change = StockChange.query.get_or_404(stock_change_id)
#     inventory = stock_change.inventory_management

#     reverse_amount = -stock_change.change_amount
#     reverse_type = 'stock_out' if stock_change.change_type == 'stock_in' else 'stock_in'

#     try:
#         inventory.update_stock(reverse_amount, reverse_type)
#         db.session.delete(stock_change)
#         db.session.commit()
#         return jsonify({
#             'message': 'Stock change deleted and inventory updated',
#             'new_quantity': inventory.current_quantity
#         }), 200
#     except ValueError as e:
#         return jsonify({'message': str(e)}), 400