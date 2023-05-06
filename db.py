from pymongo import MongoClient
import json
import sys

class Databse_Handler():
    def __init__(self):
        self.mongo_client= MongoClient("localhost:27017")
        self.db = self.mongo_client["demo"]
        self.users_collection=self.db["users"]

    def testdb(self):
        self.users_collection.insert_one({"name":"Ad'vita"})