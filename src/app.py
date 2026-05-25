import os

from dotenv import load_dotenv
from flask import Flask, render_template

from config.mongodb import mongo
from routes.product import product
from routes.todo import todo

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/bd2_productos")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "bd2-productos-secret-key")

mongo.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


app.register_blueprint(todo, url_prefix="/todo")
app.register_blueprint(product, url_prefix="/products")


if __name__ == "__main__":
    app.run(debug=True)
