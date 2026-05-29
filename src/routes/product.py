from flask import Blueprint


from services.product import (
    create_product_service,
    delete_product_view_service,
    edit_product_form_service,
    get_products_service,
    new_product_form_service,
    update_product_view_service,
    product_detail_service,
)

product = Blueprint("product", __name__)

@product.route("/<id>", methods=["GET"])
def product_detail(id):
    return product_detail_service(id)


@product.route("/", methods=["GET"])
def get_products():
    return get_products_service()


@product.route("/new", methods=["GET"])
def new_product():
    return new_product_form_service()


@product.route("/new", methods=["POST"])
def create_product():
    return create_product_service()


@product.route("/edit/<id>", methods=["GET"])
def edit_product(id):
    return edit_product_form_service(id)


@product.route("/edit/<id>", methods=["POST"])
def update_product(id):
    return update_product_view_service(id)


@product.route("/delete/<id>", methods=["POST"])
def delete_product(id):
    return delete_product_view_service(id)
