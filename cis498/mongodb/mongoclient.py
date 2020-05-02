from pymongo import MongoClient

class MongoClientHelper():

    #Constructor generates mongo connection and authentication
    def __init__(self):
        self.myclient = MongoClient('mongodb://admin2:WWSSXXccddee33@ds349587.mlab.com:49587/heroku_ffx9mlpp?retryWrites=false')
        self.db = self.myclient['heroku_ffx9mlpp']


