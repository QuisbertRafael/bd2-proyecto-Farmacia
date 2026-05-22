from flask import request, Response
from bson import json_util, ObjectId

from config.mongodb import mongo

# Documento base de producto
def product_helper(data):
    return {
        'nombre': data.get('nombre'),
        'descripcion': data.get('descripcion'),
        'precio': data.get('precio'),
        'stock': data.get('stock'),
        'categoria': data.get('categoria'),
        'imagen': data.get('imagen')
    }

# Crear producto
def create_product_service():
    data = request.get_json()

    product = product_helper(data)

    # Validación básica
    if not product['nombre']:
        return 'El nombre es obligatorio', 400

    response = mongo.db.productos.insert_one(product)

    result = {
        'id': str(response.inserted_id),
        **product
    }

    return result

# Obtener todos los productos
def get_products_service():
    data = mongo.db.productos.find()
    result = json_util.dumps(data)
    return Response(result, mimetype='application/json')

# Obtener un producto por ID
def get_product_service(id):
    data = mongo.db.productos.find_one({
        '_id': ObjectId(id)
    })

    result = json_util.dumps(data)

    return Response(result, mimetype='application/json')

# Actualizar producto
def update_product_service(id):
    data = request.get_json()

    if len(data) == 0:
        return 'Invalid payload', 400

    response = mongo.db.productos.update_one(
        {'_id': ObjectId(id)},
        {'$set': data}
    )

    if response.modified_count >= 1:
        return 'Producto actualizado satisfactoriamente', 200
    else:
        return 'Producto no encontrado', 404

# Eliminar producto
def delete_product_service(id):
    response = mongo.db.productos.delete_one({
        '_id': ObjectId(id)
    })

    if response.deleted_count >= 1:
        return 'Producto eliminado satisfactoriamente', 200
    else:
        return 'Producto no encontrado', 404