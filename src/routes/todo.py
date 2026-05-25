from flask import Blueprint

from services.todo import (
    create_product_service,
    delete_product_service,
    get_product_service,
    get_products_service,
    update_product_service,
)

todo = Blueprint("todo", __name__)


@todo.route("/", methods=["GET"])
def get_products():
    return get_products_service()


@todo.route("/<id>", methods=["GET"])
def get_product(id):
    return get_product_service(id)


@todo.route("/", methods=["POST"])
def create_product():
    return create_product_service()


@todo.route("/<id>", methods=["PUT"])
def update_product(id):
    return update_product_service(id)


@todo.route("/<id>", methods=["DELETE"])
def delete_product(id):
    return delete_product_service(id)
