from bson import ObjectId, json_util
from bson.errors import InvalidId
from flask import Response, request

from config.mongodb import mongo


def product_helper(data):
    return {
        "nombre": data.get("nombre"),
        "descripcion": data.get("descripcion"),
        "precio": data.get("precio"),
        "stock": data.get("stock"),
        "categoria": data.get("categoria"),
        "imagen": data.get("imagen"),
    }


def create_product_service():
    data = request.get_json() or {}
    product = product_helper(data)

    if not product["nombre"]:
        return "El nombre es obligatorio", 400

    response = mongo.db.productos.insert_one(product)
    result = {"id": str(response.inserted_id), **product}
    return result, 201


def get_products_service():
    data = mongo.db.productos.find()
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


def get_product_service(id):
    try:
        data = mongo.db.productos.find_one({"_id": ObjectId(id)})
    except InvalidId:
        return "Identificador inválido", 400

    if data is None:
        return "Producto no encontrado", 404

    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


def update_product_service(id):
    data = request.get_json() or {}

    if len(data) == 0:
        return "Invalid payload", 400

    try:
        response = mongo.db.productos.update_one({"_id": ObjectId(id)}, {"$set": data})
    except InvalidId:
        return "Identificador inválido", 400

    if response.modified_count >= 1:
        return "Producto actualizado satisfactoriamente", 200

    return "Producto no encontrado", 404


def delete_product_service(id):
    try:
        response = mongo.db.productos.delete_one({"_id": ObjectId(id)})
    except InvalidId:
        return "Identificador inválido", 400

    if response.deleted_count >= 1:
        return "Producto eliminado satisfactoriamente", 200

    return "Producto no encontrado", 404
