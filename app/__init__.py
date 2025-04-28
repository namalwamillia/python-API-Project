from flask import Flask, jsonify
from flask_cors import CORS  # type: ignore
from extensions import db, migrate, jwt
from app.controllers.auth.user_controller import user_bp
from app.controllers.auth.product_controller import product_bp
from app.controllers.auth.order_controller import order_bp
# from app.controllers.auth.inventory_management_controller import inventory_management_bp
# from app.controllers.auth.stock_change_controller import stock_change_bp

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object('config.Config')  # Ensure config.Config is set up with DB and JWT settings

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)  # Enable CORS for frontend requests

    # Import models
    from app.models.users import User
    from app.models.address_books import AddressBook
    from app.models.products import Product
    from app.models.orders import Order
    # from app.models.inventory_management import InventoryManagement
    # from app.models.stock_changes import StockChange
    from app.models.messages import Message

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    # app.register_blueprint(inventory_management_bp, url_prefix='/api/inventory-management')
    # app.register_blueprint(stock_change_bp, url_prefix='/api/stock-changes')

    @app.route('/')
    def home():
        return "KOK API Project Setup Successfully!"

    # Debug route to list all endpoints
    @app.route('/debug/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'url': str(rule)
            })
        return jsonify(routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)