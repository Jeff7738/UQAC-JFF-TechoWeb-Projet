from inf349.models import Order, Product,Client


class OrderServices:
    @classmethod
    def create_new_order(cls, product_id, quantity):
        product = Product.get_or_none(Product.id == product_id)
        order = Order.create(product=product, quantity=quantity)
        return order
    
    @classmethod
    def create_client(cls,email, shipping_info):
        client = Client.create(
            email=email,
            country=shipping_info["country"],
            address=shipping_info["address"],
            postal_code=shipping_info["postal_code"],
            city=shipping_info["city"],
            province=shipping_info["province"]
        )
        client.save()
        return client

    def calculate_total_price(unit_price, quantity):
        return unit_price * quantity

    def calculate_shipping_price(weight):
        if weight < 500:
            return 500
        elif weight < 2000:
            return 1000
        else:
            return 2500

    def get_tax_rate(province):
        rates = {
            "QC": 0.15,
            "ON": 0.13,
            "AB": 0.05,
            "BC": 0.12,
            "NS": 0.14
        }
        return rates.get(province, 0)
    
    def calculate_total_price_tax(total_price, province):
        tax_rate = OrderServices.get_tax_rate(province)
        return round(total_price * (1 + tax_rate), 2)
    
    @classmethod
    def update_order_customer_info(cls, order_id, client):
        order = Order.get_by_id(order_id)
        order.client = client 
        order.save()           
        return order