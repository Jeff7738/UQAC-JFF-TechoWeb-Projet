import pytest
from inf349.models import Product, Order

class TestProductsRoutes(object):

    def test_get_products_empty(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert response.get_json() == {"products": []}

    def test_create_order_success(self, app, client):
        with app.app_context():
            product = Product.create(
                id = 1,
                name="toto",
                description="toto",
                price=5.0,
                in_stock=5,
                image="image.png",
                weight=0.5
            )

            response = client.post("/order", json={"product": {"id": product.id, "quantity": 2}})
            assert response.status_code == 302
            assert response.headers["Location"].endswith("1")

    def test_create_order_invalid_data(self, app, client):
        with app.app_context():
            response = client.post("/order", json={})
            assert response.status_code == 422
            assert "error" in response.get_json() or "errors" in response.get_json()

    def test_create_order_out_of_stock(self, app, client):
        with app.app_context():
            product = Product.create(
                id = 2,
                name="nostock",
                description="toto",
                price=5.0,
                in_stock=0,
                image="image.png",
                weight=0.5
            )

            response = client.post("/order", json={"product": {"id": product.id, "quantity": 2}})
            assert response.status_code == 422
            assert "inventory" in str(response.get_json()).lower()

    # TODO à changer selon le modèle pour order
    def test_get_order_success(self, app, client):
        with app.app_context():
            product = Product.create(
                name="Produit Test",
                description="Un super produit",
                price=19.99,
                in_stock=10,
                image="image.png",
                weight=1.0
            )
            order = Order.create(product=product, quantity=3)

            response = client.get(f"/order/{order.id}")
            assert response.status_code == 200
            data = response.get_json()
            assert data["order_id"] == order.id
            assert data["product"]["id"] == product.id
            assert data["product"]["quantity"] == 3

    def test_get_order_not_found(self, app, client):
        with app.app_context():
            response = client.get("/order/999")
            assert response.status_code == 404
            assert response.get_json() == {"error": "Order not found"}
