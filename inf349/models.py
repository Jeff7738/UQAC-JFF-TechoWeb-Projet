import os

import click
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, TextField, CharField, FloatField, IntegerField,BooleanField,AutoField,ForeignKeyField
import requests

def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite')

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())

class Product(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    description = TextField()
    price = FloatField()
    in_stock = BooleanField()
    image = CharField()
    weight = IntegerField()

class Order(BaseModel):
    id = AutoField(primary_key=True)
    total_price = FloatField(null=True)
    total_price_tax = FloatField(null=True)
    email = TextField(null=True)
    credit_card = TextField(null=True)
    shipping_information = TextField(null=True)
    paid = BooleanField(null=True)
    transaction = TextField(null=True)
    product = ForeignKeyField(Product, backref='orders')
    quantity = IntegerField()
    shipping_price = IntegerField(null=True)


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.connect()
    database.create_tables([Product,Order])
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
    click.echo('Database initialized with products && Order table create')

def init_app(app):
    app.cli.add_command(init_db_command)