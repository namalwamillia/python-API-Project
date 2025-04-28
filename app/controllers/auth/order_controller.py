from flask import Blueprint, request, jsonify
from extensions import db
from app.models.orders import Order  # Assuming the Order model is in models/order.py
from datetime import datetime

order_bp = Blueprint('order', __name__)

# Simulated notification service (replace with actual email/SMS service in production)
def send_notification(user_id, message):
    # Placeholder for notification logic (e.g., email, SMS, or push notification)
    print(f"Notification sent to user {user_id}: {message}")
    # Example: Integrate with an email service like SendGrid or SMS service like Twilio
    # from sendgrid import SendGridAPIClient
    # sg = SendGridAPIClient('YOUR_API_KEY')
    # sg.send(message)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'product_id', 'quantity', 'total_price', 
                         'payment_method', 'contact_number', 'delivery_location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create new order
        new_order = Order(
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            total_price=data['total_price'],
            payment_method=data['payment_method'],
            contact_number=data['contact_number'],
            delivery_location=data['delivery_location'],
            status='pending'
        )

        # Save to database
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            'message': 'Order created successfully',
            'order': {
                'id': new_order.id,
                'user_id': new_order.user_id,
                'product_id': new_order.product_id,
                'quantity': new_order.quantity,
                'total_price': new_order.total_price,
                'payment_method': new_order.payment_method,
                'contact_number': new_order.contact_number,
                'delivery_location': new_order.delivery_location,
                'status': new_order.status,
                'order_date': new_order.order_date.isoformat()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        
        # Validate status field
        if 'status' not in data:
            return jsonify({'error': 'Missing required field: status'}), 400

        # Find order
        order = Order.query.get_or_404(order_id)
        
        # Update status
        new_status = data['status']
        order.status = new_status
        order.updated_at = datetime.utcnow()
        
        db.session.commit()

        # Send notification if order is delivered
        if new_status.lower() == 'delivered':
            message = f"Your order #{order.id} has been successfully delivered to {order.delivery_location}."
            send_notification(order.user_id, message)

        return jsonify({
            'message': 'Order status updated successfully',
            'order': {
                'id': order.id,
                'status': order.status,
                'updated_at': order.updated_at.isoformat()
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500