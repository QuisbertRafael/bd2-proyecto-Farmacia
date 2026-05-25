from bson import ObjectId
from bson.errors import InvalidId
from flask import flash, redirect, render_template, request, url_for

from config.mongodb import mongo


def _clean_product_payload(form):
    return {
        "nombre": form.get("nombre", "").strip(),
        "descripcion": form.get("descripcion", "").strip(),
        "precio": float(form.get("precio") or 0),
        "stock": int(form.get("stock") or 0),
        "categoria": form.get("categoria", "").strip(),
        "imagen": form.get("imagen", "").strip(),
    }


def get_products_service():
    products = list(mongo.db.productos.find().sort("nombre", 1))
    return render_template("products.html", products=products)


def new_product_form_service():
    return render_template("new_product.html", product=None, action_url=url_for("product.create_product"), form_title="Crear producto")


def create_product_service():
    try:
        product_data = _clean_product_payload(request.form)
    except ValueError:
        flash("El precio y el stock deben tener valores numéricos válidos.", "danger")
        return redirect(url_for("product.new_product"))

    if not product_data["nombre"]:
        flash("El nombre del producto es obligatorio.", "danger")
        return redirect(url_for("product.new_product"))

    mongo.db.productos.insert_one(product_data)
    flash("Producto creado correctamente.", "success")
    return redirect(url_for("product.get_products"))


def edit_product_form_service(id):
    try:
        found_product = mongo.db.productos.find_one({"_id": ObjectId(id)})
    except InvalidId:
        found_product = None

    if not found_product:
        flash("Producto no encontrado.", "warning")
        return redirect(url_for("product.get_products"))

    return render_template(
        "new_product.html",
        product=found_product,
        action_url=url_for("product.update_product", id=id),
        form_title="Editar producto",
    )


def update_product_view_service(id):
    try:
        product_data = _clean_product_payload(request.form)
        object_id = ObjectId(id)
    except ValueError:
        flash("El precio y el stock deben tener valores numéricos válidos.", "danger")
        return redirect(url_for("product.edit_product", id=id))
    except InvalidId:
        flash("Identificador de producto inválido.", "danger")
        return redirect(url_for("product.get_products"))

    mongo.db.productos.update_one({"_id": object_id}, {"$set": product_data})
    flash("Producto actualizado correctamente.", "success")
    return redirect(url_for("product.get_products"))


def delete_product_view_service(id):
    try:
        response = mongo.db.productos.delete_one({"_id": ObjectId(id)})
    except InvalidId:
        response = None

    if response and response.deleted_count == 1:
        flash("Producto eliminado correctamente.", "success")
    else:
        flash("Producto no encontrado.", "warning")

    return redirect(url_for("product.get_products"))
