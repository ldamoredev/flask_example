from app import configure_app
from extensions import db
from models import User, Product
from flask import Flask

# Create an app instance and configure it
app = configure_app(Flask(__name__))

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
