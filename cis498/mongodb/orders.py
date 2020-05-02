from cis498.mongodb.customers import Customers
from cis498.mongodb.mongoclient import MongoClientHelper
from bson.objectid import ObjectId

import uuid

class Orders:

    def __init__(self):
        self.mc = MongoClientHelper()
        self.orders_db = self.mc.db['orders']

    # This will generate an order document and also update the customer record
    def generateOrder(self, customer, order, order_comments):
        #Generate a UUID https://en.wikipedia.org/wiki/Universally_unique_identifier
        orderId = uuid.uuid4()
        order = {
            'orderId': orderId,
            'email': customer.email,
            'items': order,
            'comments': order_comments,
            'orderStatus': 'Received',
            'orderType': 'Delivery'
        }
        generatedOrder = self.orders_db.insert_one(order)
        self.updateCustomerRecord(customer.email, generatedOrder.inserted_id)

    # Updates the customer record
    def updateCustomerRecord(self, email, orderId):
        customer = Customers()
        customer.updateCustomerOrders(email, orderId)


    # Functional Requirement 5
    def getCurrentOrders(self):
        query_received_orders = {"$not": {"orderStatus": 'Order Complete'}}
        orderCollection = self.orders_db.find({'orderStatus': {"$ne": "Order Complete"}})
        orderList = []
        for order in orderCollection:
            Dict = dict({
                'email': order['email'],
                'id': order['_id'],
                'comments': order['comments'],
                'items': order['items']['Name'],
                'status': order['orderStatus']
            })
            orderList.append(Dict)
        return orderList


    def updateOrder(self, order):

        oidQuery = {"_id": ObjectId(order)}
        orderToUpdate = self.orders_db.find_one(oidQuery)
        if orderToUpdate['orderStatus'] == 'Received':
            orderToUpdate['orderStatus'] = 'In Progress'
        elif orderToUpdate['orderStatus'] == 'In Progress':
            orderToUpdate['orderStatus'] = 'Order Ready'
        elif orderToUpdate['orderStatus'] == 'Order Ready' and orderToUpdate['orderType'] == 'Delivery':
            orderToUpdate['orderStatus'] = 'In Transit'
        elif orderToUpdate['orderStatus'] == 'Order Ready' and orderToUpdate['orderType'] == 'Pickup':
            orderToUpdate['orderStatus'] = 'Ready For Pickup'
        elif orderToUpdate['orderStatus'] == 'In Transit' or orderToUpdate['orderStatus'] == 'Ready For Pickup':
            orderToUpdate['orderStatus'] = 'Order Complete'

        self.orders_db.update_one(oidQuery, {"$set": {"orderStatus": orderToUpdate['orderStatus']}})




