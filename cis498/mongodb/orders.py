from cis498.mongodb.customers import Customers
from cis498.mongodb.mongoclient import MongoClientHelper
from bson.objectid import ObjectId
import datetime

import uuid

class Orders:
    ORDER_STATUS = 'orderStatus'
    ORDER_TYPE = 'orderType'
    RECEIVED = 'Received'
    IN_PROGRESS = 'In Progress'
    ORDER_READY = 'Order Ready'
    IN_TRANSIT = 'In Transit'
    READY_FOR_PICKUP = 'Ready For Pickup'
    ORDER_COMPLETE = 'Order Complete'

    def __init__(self):
        self.mc = MongoClientHelper()
        self.orders_db = self.mc.db['orders']

    # This will generate an order document and also update the customer record
    def generateOrder(self, customer, order, order_comments):
        #Generate a UUID https://en.wikipedia.org/wiki/Universally_unique_identifier
        datetime_time = datetime.datetime.now()
        order = {
            'email': customer.email,
            'items': order,
            'comments': order_comments,
            'orderStatus': 'Received',
            'orderType': 'Delivery',
            'dateTime': datetime_time
        }
        generatedOrder = self.orders_db.insert_one(order)
        self.updateCustomerRecord(customer.email, generatedOrder.inserted_id)

    # Updates the customer record
    def updateCustomerRecord(self, email, orderId):
        customer = Customers()
        customer.updateCustomerOrders(email, orderId)


    # Functional Requirement 5
    def getCurrentOrders(self):
        orderCollection = self.orders_db.find({'orderStatus': {"$ne": self.ORDER_COMPLETE}})
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
        if orderToUpdate[self.ORDER_STATUS] == self.RECEIVED:
            orderToUpdate[self.ORDER_STATUS] = self.IN_PROGRESS
        elif orderToUpdate[self.ORDER_STATUS] == self.IN_PROGRESS:
            orderToUpdate[self.ORDER_STATUS] = self.ORDER_READY
        elif orderToUpdate[self.ORDER_STATUS] == self.ORDER_READY and orderToUpdate[self.ORDER_TYPE] == 'Delivery':
            orderToUpdate[self.ORDER_STATUS] = self.IN_TRANSIT
        elif orderToUpdate[self.ORDER_STATUS] == self.ORDER_READY and orderToUpdate[self.ORDER_TYPE] == 'Pickup':
            orderToUpdate[self.ORDER_STATUS] = self.READY_FOR_PICKUP
        elif orderToUpdate[self.ORDER_STATUS] == self.IN_TRANSIT or orderToUpdate[self.ORDER_STATUS] == self.READY_FOR_PICKUP:
            orderToUpdate[self.ORDER_STATUS] = self.ORDER_COMPLETE

        self.orders_db.update_one(oidQuery, {"$set": {self.ORDER_STATUS: orderToUpdate[self.ORDER_STATUS]}})




