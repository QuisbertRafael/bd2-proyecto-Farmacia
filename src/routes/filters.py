"""
Lógica pura de filtros — extraída para poder testear sin Flask/MongoDB.
En product.py se importa así: from .filters import build_filter_query
"""

def build_filter_query(nombre=None, categoria=None, precio_min=None, precio_max=None):
    query = {}

    if nombre and nombre.strip():
        query["nombre"] = {"$regex": nombre.strip(), "$options": "i"}

    if categoria and categoria.strip():
        query["categoria"] = {"$regex": f"^{categoria.strip()}$", "$options": "i"}

    precio_query = {}
    if precio_min is not None:
        try:
            precio_query["$gte"] = float(precio_min)
        except (ValueError, TypeError):
            pass
    if precio_max is not None:
        try:
            precio_query["$lte"] = float(precio_max)
        except (ValueError, TypeError):
            pass
    if precio_query:
        query["precio"] = precio_query

    return query