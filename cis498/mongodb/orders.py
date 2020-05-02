
from cis498.mongodb.mongoclient import MongoClientHelper


class Orders:

    def __init__(self):
        self.mc = MongoClientHelper()
        self.ordersdb = self.mc.db['orders']

    def generateOrder(self, customer, order):
        orders = self.mc.db['orders']
        order = {
            'orderId': '001',
            'email': customer.email,
            'items': order
        }
        orders.insert_one(order)
