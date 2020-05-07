from cis498.mongodb.mongoclient import MongoClientHelper


class Drivers:

    def __init__(self):
        self.mc = MongoClientHelper()
        self.db = self.mc.db['drivers']

    # Define Actions of a driver

    def is_driver(self, email):
        driver = self.db.find_one({"email": email})
        if driver is None:
            return False
        return True
    # Dashboard functionality - Requirement FR19
    # def numberOfOrdersFilled()

    # def onlineTips()

    # def currentOrders()

    # def updateOrder()