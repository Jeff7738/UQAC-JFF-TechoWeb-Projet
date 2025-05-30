from inf349.models import Product, Order

def validate_order_data(data):
    product_data = data.get('product') if data else None
    if not product_data or 'id' not in product_data or 'quantity' not in product_data:
        return False, {
            "errors": {
                "product": {
                    "code": "missing-fields",
                    "name": "La création d'une commande nécessite un produit"
                }
            }
        }
    
    quantity = product_data.get('quantity')
    if  quantity < 1:
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
    try:
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
    except Product.DoesNotExist:
        return False, {
            "errors": {
                "product": {
                    "code": "out-of-inventory",
                    "name": "Le produit demandé n'est pas en inventaire"
                }
            }
        }
    
def validate_order_update_informations(informations):
    errors = {
        "order": {
            "code": "missing-fields",
            "name": "Il manque un ou plusieurs champs qui sont obligatoires"
        }
    }

    if not informations or "order" not in informations:
        return False, errors

    order_data = informations["order"]
    required_fields = ["email", "shipping_information"]
    shipping_required_fields = ["country", "address", "postal_code", "city", "province"]

    for field in required_fields:
        if field not in order_data:
            return False, errors

    shipping_info = order_data.get("shipping_information", {})
    for field in shipping_required_fields:
        if field not in shipping_info:
            return False, errors

    return True, order_data

