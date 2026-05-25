from flask import render_template, request, redirect
from config.mongodb import mongo

def get_products_service():
    data = mongo.db.productos.find()

    products = list(data)

    return render_template(
        'products.html',
        products=products
    )

# Mostrar formulario
def new_product_form_service():
    return render_template('new_product.html')


# Crear producto
def create_product_service():

    product = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion'),
        'precio': float(request.form.get('precio')),
        'stock': int(request.form.get('stock')),
        'categoria': request.form.get('categoria'),
        'imagen': request.form.get('imagen')
    }

    mongo.db.productos.insert_one(product)

    return redirect('/products')