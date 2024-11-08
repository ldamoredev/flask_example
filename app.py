import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from extensions import db  # Import db from extensions
from auth.routes import auth_bp
from products.routes import products_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

def configure_app(app):
    # PostgreSQL database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("SECRET_KEY")

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error("An internal error occurred: %s", e)
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

    return app

if __name__ == "__main__":
    server_app = configure_app(app)

    # Set up logging
    if not server_app.debug:
        handler = RotatingFileHandler("error.log", maxBytes=10000, backupCount=1)
        handler.setLevel(logging.ERROR)
        server_app.logger.addHandler(handler)
    server_app.run(debug=True)
