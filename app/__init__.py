from flask import Flask
from extensions import db, migrate, jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.auth.companies_controller import company
from app.controllers.auth.book_controller import books
import datetime
from flask_swagger_ui import get_swaggerui_blueprint
# from app.controllers.auth.revoked_tokencontroller import revoked_token

def create_app():
    from flask import Flask

    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False  # Allow non-ASCII characters in JSON responses

    app.config.from_object('config.config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Importing and registering models
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book
    

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(company)
    app.register_blueprint(books)
    # app.register_blueprint(revoked_token) 

    @app.route('/')
    def home():
        return "AuthorS API Project Setup"  # Corrected indentation

    return app

# Assuming you call create_app() to get the Flask application instance
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)





 
