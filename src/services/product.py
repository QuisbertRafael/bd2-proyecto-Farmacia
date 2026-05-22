from flask import render_template
from config.mongodb import mongo

def get_products_service():
    data = mongo.db.productos.find()

    products = list(data)

    return render_template(
        'products.html',
        products=products
    )