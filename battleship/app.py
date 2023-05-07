from flask import Flask, render_template, send_from_directory, request, redirect
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

mongo_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
db = mongo_client.db

user_collection = db['users']
leaderboard_collection = db['leaderboard']

# [User accounts]
# Each user's profile must track at least one value related to that user (eg. display name, avatar, number of wins, etc.)
# Users must have a way to view this data for their own profile. They do not have to have a way to change this data (eg. display name, avatar can be chosen at account creation and never change)


def add_new_user(username, password):
    profile = {
        'username': username,
        'password': password,
        'wins': 0,
        'losses': 0
    }
    user_collection.insert_one(profile)
    leaderboard_collection.insert_one(
        # username and number of wins
        {username: 0}
    )


def find_user(username):
    profile = user_collection.find_one(
        {"username": username}
    )
    # could also just return profile and check if None outside of function
    if profile != None:
        return profile
    return False


def build_leaderboard():
    leaderboard = []
    for user in user_collection.find({}, {"_id": 0, "username": 1, "wins": 1}):
        leaderboard.append(user)


@app.route("/")
def hello_world():
    return render_template("welcome.html")


@app.route("/templates/<file>")
def templates(file):
    return send_from_directory('templates', file)


# @app.route("/static/<file>")
# def static(file):
#     return send_from_directory('static', file)


@app.route("/images/<image>")
def hero(image):
    return send_from_directory('images', image)


@app.route("/signupForm", methods=['POST', 'GET'])
def signupForm():
    return render_template("signup.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        profile = {'username': username, "password": password}
        print(profile)
        user_collection.insert_one(profile)
        print("-------something happened!!!!!!!!!!!-------")
        return "nice"
    return "not nice"


@app.route("/loginForm")
def login():
    return render_template("login.html")
