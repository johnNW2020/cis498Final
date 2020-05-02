from cis498.mongodb.mongoclient import MongoClientHelper


class Staff:

    def __init__(self):
        self.mc = MongoClientHelper()
        self.db = self.mc.db['staff']

    # Define Actions of a staff member

    # Update Order Status
    # def updateOrder

