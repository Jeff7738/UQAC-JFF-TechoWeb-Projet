import os

from peewee import DoesNotExist
from flask import Flask, jsonify, request, redirect, url_for, abort

from products import controller
from products.models import init_app,Product,Order
from products.services import OrderServices

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
    
    @app.route('/order', methods=['POST'])
    def create_order():
        data = request.get_json()

        valid, result = controller.validate_order_data(data)
        if not valid:
            return jsonify(result), 422

        product_data = result
        product_id = product_data['id']
        quantity = product_data['quantity']

        in_stock, inventory_result = controller.check_inventory(product_id)
        if not in_stock:
            return jsonify(inventory_result), 422

        order = OrderServices.create_new_order(product_id, quantity)

        location_url = url_for('create_order', order_id=order.id)
        return redirect(location_url, code=302)
    
    # TODO exigences get + tests
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        try:
            order = Order.get(Order.id == order_id)
            return jsonify({
            "order_id": order.id,
            "product": {
                "id": order.product.id,
                "quantity": order.quantity
            }
            })
        except Order.DoesNotExist:
            return jsonify({"error": "Order not found"}), 404

    return app


