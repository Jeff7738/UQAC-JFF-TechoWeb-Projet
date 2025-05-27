from inf349.models import Order, Product

class OrderServices:
    @classmethod
    def create_new_order(cls, product_id, quantity):
        product = Product.get_or_none(Product.id == product_id)
        order = Order.create(product=product, quantity=quantity)
        return order