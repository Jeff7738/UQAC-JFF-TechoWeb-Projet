import os

from peewee import DoesNotExist
from flask import Flask, jsonify, request, redirect, url_for, abort

from products.models import init_app,Product

def create_app(initial_config=None):
    app = Flask("products")
    init_app(app)

    @app.route('/', methods=['GET'])
    def get_products():
        products = Product.select()
        result = {"products": []}
        for p in products:
            result["products"].append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "in_stock": p.in_stock,
            "image": p.image,
            "weight": p.weight
        })
        return jsonify(result)
    
    return app


