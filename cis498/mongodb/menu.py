from cis498.mongodb.mongoclient import MongoClientHelper
from bson.objectid import ObjectId

class Menu:

    def pizza(self):
        mc = MongoClientHelper()
        menuItems = mc.db['menu']
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
        mc = MongoClientHelper()
        menuItems = mc.db['menu']
        return menuItems.find_one({'_id': ObjectId(id)})
