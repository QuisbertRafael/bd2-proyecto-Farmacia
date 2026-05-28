# BD II - Productos con Flask, MongoDB y Bootstrap

Implementación de las historias:

- US-04: Formulario Bootstrap para crear producto con nombre, descripción, precio, stock, categoría e imagen URL.
- US-06: Vista de listado de productos en tarjetas Bootstrap con imagen, nombre, precio, stock, categoría y botones visibles de editar/eliminar.

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Configuración

Copia `.env.example` como `.env` y ajusta la conexión si corresponde:

```bash
MONGO_URI=mongodb://localhost:27017/bd2_productos
SECRET_KEY=bd2-productos-secret-key
```

## Ejecutar

```bash
python app.py
```

Rutas principales:

- `/products/`: listado de productos en tarjetas.
- `/products/new`: formulario de creación.
- `/products/edit/<id>`: formulario de edición.
- `/todo/`: API JSON básica.
