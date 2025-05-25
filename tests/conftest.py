# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# import pytest
# from products.models import Product, get_db_path
# from inf349 import create_app
# from peewee import SqliteDatabase

# @pytest.fixture
# def app():

#     app = create_app({"TESTING": True})

#     database = SqliteDatabase(get_db_path())
#     database.create_tables(Product)

#     yield app
#     database.drop_tables([Product])

# @pytest.fixture
# def client(app):
#     return app.test_client()
