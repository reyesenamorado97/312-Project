from pymongo import MongoClient
import json
import sys
import html
import bcrypt

class Database_Handler():
    def __init__(self):
        self.mongo_client = MongoClient("localhost:27017")
        self.db = self.mongo_client["Battleship"]
        self.users_collection = self.db["users"]

    def testdb(self):
        self.users_collection.insert_one({"name":"Ad'vita"})

    def add_new_user(self, username, password):
        #hash before storing
        if self.users_collection.find_one({"username":username}):
            #username exists
            return False
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            profile = {
                'username': username,
                'password': hashed_password,
                'wins': 0
            }
            self.users_collection.insert_one(profile)
            return True

    def authenticate(self, username, password):
        # Find a user in the database
        user = self.users_collection.find_one({'username': username})
        if user != None:
            return bcrypt.checkpw(password.encode(),user['password'])
        print("User does not exist.")
        return False

    def find_user(self, username):
        profile = self.users_collection.find_one(
            {"username": username}
        )
        # could also just return profile and check if None outside of function
        if profile != None:
            return profile
        return False
    