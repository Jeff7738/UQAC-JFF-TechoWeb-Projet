import os
import tempfile
import pytest
from peewee import SqliteDatabase

os.environ['DATABASE'] = ":memory:"

from inf349 import create_app
from inf349.models import Product, Order,get_db_path

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, Order])

    yield app

    database.drop_tables([Product, Order])

@pytest.fixture
def client(app):
    return app.test_client()
