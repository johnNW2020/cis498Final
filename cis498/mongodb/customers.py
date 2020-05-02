from cis498.mongodb.mongoclient import MongoClientHelper


class Customers:

    # Established mongo connection and customers collection
    def __init__(self):
        self.mc = MongoClientHelper()
        self.customersdb = self.mc.db['customers']

    def createCustomer(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        address = form.cleaned_data.get('address')
        phonenumber = form.cleaned_data.get('phonenumber')
        customer = {"name": name,
                    "email": email,
                    "address": address,
                    "phonenumber": phonenumber}

        self.customersdb.insert_one(customer)
