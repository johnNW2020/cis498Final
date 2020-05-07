from cis498.mongodb.customers import Customers
from cis498.mongodb.mongoclient import MongoClientHelper
from bson.objectid import ObjectId
import datetime


deliveryDict = {
    "1": "Pickup - No Delivery",
    "2": "Delivery - In House",
    "3": "Delivery - 3rd Party"
}

tipDict = {
    "1": "15%",
    "2": "18%",
    "3": "20%",
    "4": "Custom Amount",
    "5": "None"
}

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
    def generateOrder(self, customer, order, form):
        #Generate a UUID https://en.wikipedia.org/wiki/Universally_unique_identifier
        datetime_time = datetime.datetime.now()
        # TODO :update driver to be an option
        order = {
            'email': customer.email,
            'items': order,
            'comments': form['comments'].data,
            'orderStatus': 'Received',
            'orderType': deliveryDict.get(form['delivery_method'].data),
            'dateTime': datetime_time,
            'driver': 'jackiestewart@willyspizza.com'
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
                'items': order['items'],
                'status': order['orderStatus']
            })
            orderList.append(Dict)
        return orderList

        # Functional Requirement 5
    def getCurrentUserOrder(self, email, customer):
        #First get the customer order history
        final_result = None
        customerOrders = customer.orders
        for order in customerOrders:
            status = self.orders_db.find_one({'_id': ObjectId(order)})
            if status['orderStatus'] != 'Order Complete':
                final_result = status

        if final_result == None:
            order_list = {
                'email': '',
                'id': '',
                'comments': '',
                'items': '',
                'status': 'No Pending Orders'}
        else:
            order_list ={
                    'email': final_result['email'],
                    'id': final_result['_id'],
                    'comments': final_result['comments'],
                    'items': final_result['items'],
                    'status': final_result['orderStatus']
                }

        return order_list

    def get_driver_orders(self, user):
        orderCollection = self.orders_db.find({'orderStatus': self.IN_TRANSIT})
        orderList = []
        for order in orderCollection:
            if order['driver'] == user:
                Dict = dict({
                    'email': order['email'],
                    'id': order['_id'],
                    'comments': order['comments'],
                    'items': order['items'],
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
        elif orderToUpdate[self.ORDER_STATUS] == self.ORDER_READY and 'Pickup' not in orderToUpdate[self.ORDER_TYPE]:
            orderToUpdate[self.ORDER_STATUS] = self.IN_TRANSIT
        elif orderToUpdate[self.ORDER_STATUS] == self.ORDER_READY and 'Pickup' in orderToUpdate[self.ORDER_TYPE]:
            orderToUpdate[self.ORDER_STATUS] = self.READY_FOR_PICKUP
        elif orderToUpdate[self.ORDER_STATUS] == self.IN_TRANSIT or orderToUpdate[self.ORDER_STATUS] == self.READY_FOR_PICKUP:
            orderToUpdate[self.ORDER_STATUS] = self.ORDER_COMPLETE

        self.orders_db.update_one(oidQuery, {"$set": {self.ORDER_STATUS: orderToUpdate[self.ORDER_STATUS]}})



