# from flask import Blueprint, jsonify, request
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.models.inventory_management import InventoryManagement
# from app.models.stock_changes import StockChange
# from app.models.users import User  # Import User from the correct module

# inventory_management_bp = Blueprint('inventory_management', __name__, url_prefix='/admin/inventory-management')

# def admin_required(fn):
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
#         if user.role != 'admin':
#             return jsonify({'message': 'Admin access required'}), 403
#         return fn(*args, **kwargs)
#     return wrapper

# @inventory_management_bp.route('/', methods=['GET'])
# @admin_required
# def get_inventory_management():
#     inventory_items = InventoryManagement.query.all()
#     return jsonify([{
#         'id': item.id,
#         'product_id': item.product_id,
#         'product_name': item.product.name,
#         'current_quantity': item.current_quantity,
#         'low_stock_threshold': item.low_stock_threshold,
#         'location': item.location,
#         'is_low_stock': item.is_low_stock(),
#         'stock_status': item.get_stock_status()
#     } for item in inventory_items]), 200

# @inventory_management_bp.route('/low-stock', methods=['GET'])
# @admin_required
# def get_low_stock():
#     low_stock_items = InventoryManagement.query.filter(InventoryManagement.current_quantity <= InventoryManagement.low_stock_threshold).all()
#     return jsonify([{
#         'product_id': item.product_id,
#         'product_name': item.product.name,
#         'current_quantity': item.current_quantity,
#         'low_stock_threshold': item.low_stock_threshold
#     } for item in low_stock_items]), 200

# @inventory_management_bp.route('/<int:inventory_id>/update', methods=['POST'])
# @admin_required
# def update_stock(inventory_id):
#     inventory = InventoryManagement.query.get_or_404(inventory_id)
#     data = request.get_json()
#     quantity_change = data.get('quantity_change')
#     change_type = data.get('change_type')
#     if not quantity_change or not change_type:
#         return jsonify({'message': 'quantity_change and change_type are required'}), 400
#     try:
#         inventory.update_stock(quantity_change, change_type)
#         return jsonify({
#             'message': 'Stock updated successfully',
#             'new_quantity': inventory.current_quantity
#         }), 200
#     except ValueError as e:
#         return jsonify({'message': str(e)}), 400

# @inventory_management_bp.route('/<int:inventory_id>/history', methods=['GET'])
# @admin_required
# def get_stock_history(inventory_id):
#     inventory = InventoryManagement.query.get_or_404(inventory_id)
#     stock_changes = inventory.stock_changes
#     return jsonify([{
#         'id': change.id,
#         'change_type': change.change_type,
#         'change_amount': change.change_amount,
#         'created_at': change.created_at.isoformat()
#     } for change in stock_changes]), 200