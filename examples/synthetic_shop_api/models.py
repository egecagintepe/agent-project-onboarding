class Item:
    def __init__(self, item_id: int, name: str, price_cents: int):
        self.item_id = item_id
        self.name = name
        self.price_cents = price_cents

class Order:
    def __init__(self, order_id: int, customer_id: str, status: str = "PENDING"):
        self.order_id = order_id
        self.customer_id = customer_id
        self.status = status
