from cis498.mongodb.mongoclient import MongoClientHelper
from bson.objectid import ObjectId

class Menu:

    def __init__(self):
        self.mc = MongoClientHelper()
        self.db = self.mc.db['menu']

    def pizza(self):
        menuItems = self.db
        myMenuList = []
        for m in menuItems.find():
            em = Menu()
            em.name = m['Name']
            em.price = m['Price']
            em.description = m['Description']
            em.type = m['Type']
            em.id = m['_id']
            myMenuList.append(em)
        return myMenuList

    def findById(self, id):
        return self.db.find_one({'_id': ObjectId(id)})

    # Functional Requirement 2
    # def editMenuItem()

    # Functional Requirement 3
    # def editMenuPrice()


