from products.models import Product, Order

def validate_order_data(data):
    product_data = data.get('product') 
    quantity = product_data.get('quantity')
    if quantity < 1:
        return False, {
            "errors": {
                "product": {
                    "code": "missing-fields",
                    "name": "La création d'une commande nécessite un produit"
                }
            }
        }

    return True, product_data

def check_inventory(product_id):
    product = Product.get(Product.id == product_id)
    if not product.in_stock:
        return False, {
            "errors": {
                "product": {
                    "code": "out-of-inventory",
                    "name": "Le produit demandé n'est pas en inventaire"
                            }
                }
            }
    return True, product
