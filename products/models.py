import os

import click
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, TextField, CharField, FloatField, IntegerField,BooleanField
import requests

def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite')

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())

class Product(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    description = TextField()
    price = FloatField()
    in_stock = BooleanField()
    image = CharField()
    weight = IntegerField()


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.connect()
    database.create_tables([Product])
    database.close()
    r = requests.get('http://dimensweb.uqac.ca/~jgnault/shops/products/')
    data = r.json()
    products = data.get('products', [])
    with database.atomic():
        for p in products:
            Product.create(
                id=p['id'],
                name=p['name'],
                description=p.get('description', ''),
                price=p['price'],
                in_stock=p['in_stock'],
                image=p['image'],
                weight=p['weight']
            )
    click.echo('Database initialized with products')

def init_app(app):
    app.cli.add_command(init_db_command)