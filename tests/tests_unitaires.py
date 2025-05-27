import pytest
from inf349 import controller
from inf349.models import Product
from peewee import DoesNotExist

class TestController(object):

    def test_validate_order_data_valid(self):
        data = {
            "product": {
                "id": 1,
                "quantity": 2
            }
        }
        valid, result = controller.validate_order_data(data)
        assert valid is True
        assert result == {"id": 1, "quantity": 2}

    def test_validate_order_data_missing_product(self):
        data = {}
        valid, result = controller.validate_order_data(data)
        assert not valid
        assert result["errors"]["product"]["code"] == "missing-fields"

    def test_validate_order_data_invalid_quantity(self):
        data = {
            "product": {
                "id": 1,
                "quantity": 0
            }
        }
        valid, result = controller.validate_order_data(data)
        assert not valid
        assert result["errors"]["product"]["code"] == "missing-fields"

    def test_check_inventory_success(self, app):
        with app.app_context():
            product = Product.create(
                name="Produit disponible",
                description="",
                price=10.0,
                in_stock=5,
                image="",
                weight=1.0
            )

            valid, result = controller.check_inventory(product.id)
            assert valid is True
            assert result == product

    def test_check_inventory_out_of_stock(self, app):
        with app.app_context():
            product = Product.create(
                name="Produit épuisé",
                description="",
                price=15.0,
                in_stock=0,
                image="",
                weight=0.5
            )

            valid, result = controller.check_inventory(product.id)
            assert not valid
            assert result["errors"]["product"]["code"] == "out-of-inventory"
