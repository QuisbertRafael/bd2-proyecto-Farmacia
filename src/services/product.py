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
    # ── 1. Leer parámetros de query ───────────────────────────────────
    nombre     = request.args.get("nombre", "").strip()
    categoria  = request.args.get("categoria", "").strip()
    precio_min = request.args.get("precio_min", "").strip()
    precio_max = request.args.get("precio_max", "").strip()

    # ── 2. Construir filtro dinámico ──────────────────────────────────
    filtro = {}

    if nombre:
        filtro["nombre"] = {"$regex": nombre, "$options": "i"}

    if categoria:
        filtro["categoria"] = categoria

    rango_precio = {}
    if precio_min:
        try:
            rango_precio["$gte"] = float(precio_min)
        except ValueError:
            flash("Precio mínimo inválido, se ignoró el filtro.", "warning")

    if precio_max:
        try:
            rango_precio["$lte"] = float(precio_max)
        except ValueError:
            flash("Precio máximo inválido, se ignoró el filtro.", "warning")

    if rango_precio:
        filtro["precio"] = rango_precio

    # ── 3. Consultar MongoDB ──────────────────────────────────────────
    products  = list(mongo.db.productos.find(filtro).sort("nombre", 1))
    categorias = mongo.db.productos.distinct("categoria")

    return render_template(
        "products.html",
        products=products,
        categorias=categorias,
        filtros={
            "nombre":     nombre,
            "categoria":  categoria,
            "precio_min": precio_min,
            "precio_max": precio_max,
        },
    )


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
