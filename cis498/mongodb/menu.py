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
            em = MenuItem(m['Name'], m['Price'], m['Description'], m['Type'], m['_id'])
            myMenuList.append(em)
        return myMenuList

    def menuNames(self):
        menuItems = self.db
        myMenuList = []
        for m in menuItems.find():
            myMenuList.append(m['Name'])
        return myMenuList

    def findById(self, id):
        return self.db.find_one({'_id': ObjectId(id)})

    def findByName(self, name):
        item = self.db.find_one({'Name': name})
        menuItem = MenuItem(item['Name'], item['Price'], item['Description'], item['Type'], item['_id'])
        return menuItem

    def updateMenuItem(self, form):
        name = form['name'].data.strip()
        type = form['type'].data.strip()
        description = form['description'].data.strip()
        price = form['price'].data.strip()
        id = form['item_id'].data

        query_by_id = {'_id': ObjectId(id)}
        self.db.update_one(query_by_id, {"$set": {'Name': name, 'Type': type, 'Description': description, 'Price': price}})

    def createNewItem(self, form):
        name = form['name'].data.strip()
        type = form['type'].data.strip()
        description = form['description'].data.strip()
        price = form['price'].data.strip()

        menuItem = {
            'Name': name,
            'Price': price,
            'Type': type,
            'Description': description
        }

        self.db.insert_one(menuItem)



    # Functional Requirement 2
    # def editMenuItem()

    # Functional Requirement 3
    # def editMenuPrice()

class MenuItem:

    def __init__(self, name, price, description, type, id):
        self.name = name
        self.price = price
        self.description = description
        self.type = type
        self.id = id

