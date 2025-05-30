from flask import Flask, jsonify, request, redirect, url_for

from inf349 import controller
from inf349.models import init_app,Product,Order
from inf349.services import OrderServices
from peewee import DoesNotExist

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
    
    # TODO tests
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        try:
            order = Order.get(Order.id == order_id)
            total_price = OrderServices.calculate_total_price(order.product.price, order.quantity)
            shipping_price = OrderServices.calculate_shipping_price(order.product.weight * order.quantity)
            # TODO en fonction de la province dans shipping information
            total_price_tax = OrderServices.calculate_total_price_tax(total_price, order.quantity)
            return jsonify({
            "order_id": order.id,
            "total_price": total_price,
            "total_price_tax": total_price_tax,
            "credit_card": order.credit_card or {},
            "email": order.client.email if order.client else None,
            "shipping_information": {
                "country": order.client.country,
                "address": order.client.address,
                "postal_code": order.client.postal_code,
                "city": order.client.city,
                "province": order.client.province
            } if order.client else {},
            "paid": order.paid,
            "transaction": order.transaction or {},
            "product": {
                "id": order.product.id,
                "quantity": order.quantity,
            },
            "shipping_price": shipping_price
            })
        except Order.DoesNotExist:
            return jsonify({"error": "Order not found"}), 404
        
    # TODO tests 
    @app.route('/order/<int:order_id>', methods=['PUT'])
    def update_order(order_id):
        data = request.get_json()

        valid, result = controller.validate_order_update_informations(data)
        if not valid:
            return jsonify({"errors": result}), 422

        email = result["email"]
        shipping_info = result["shipping_information"]

        try:
            order = Order.get_by_id(order_id)
        except Order.DoesNotExist:
            return jsonify({"error": "Order not found"}), 404

        client = OrderServices.create_client(email, shipping_info)
        OrderServices.update_order_customer_info(order_id, client)

        return jsonify({
            "order": {
                "id": order.id,
                "email": client.email,
                "shipping_information": {
                    "country": client.country,
                    "address": client.address,
                    "postal_code": client.postal_code,
                    "city": client.city,
                    "province": client.province
                },
                "credit_card": order.credit_card or {},
                "transaction": order.transaction or {},
                "paid": order.paid,
                "product": {
                    "id": order.product.id,
                    "quantity": order.quantity
                },
                "total_price": order.total_price,
                "total_price_tax": order.total_price_tax,
                "shipping_price": order.shipping_price
            }
        }), 200


    return app


