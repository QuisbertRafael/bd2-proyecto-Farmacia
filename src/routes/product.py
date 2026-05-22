from flask import Blueprint
from services.product import get_products_service

product = Blueprint('product', __name__)

@product.route('/', methods=['GET'])
def get_products():
    return get_products_service()