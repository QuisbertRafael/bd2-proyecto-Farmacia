from flask import Blueprint
from services.product import (
    get_products_service,
    create_product_service,
    new_product_form_service
)

product = Blueprint('product', __name__)

@product.route('/', methods=['GET'])
def get_products():
    return get_products_service()

# Mostrar formulario
@product.route('/new', methods=['GET'])
def new_product():
    return new_product_form_service()

# Guardar producto
@product.route('/new', methods=['POST'])
def create_product():
    return create_product_service()