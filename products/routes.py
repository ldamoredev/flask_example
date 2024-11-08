from flask import Blueprint, request, jsonify, session
from extensions import db  # Import from extensions
from models import User, Product
from functools import wraps  # Import wraps for the decorator

products_bp = Blueprint("products", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

@products_bp.route("/", methods=["POST"])
@login_required
def create_product():
    data = request.json
    product_name = data.get("name")
    product_price = data.get("price")

    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    product = Product(name=product_name, price=product_price, created_by=user.id)
    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created!",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "created_by": user.username
        }
    }), 201

@products_bp.route("/", methods=["GET"])
@login_required
def show_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "created_by": product.user.username
    } for product in products]), 200
