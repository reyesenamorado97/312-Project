from flask import Flask, render_template, send_from_directory, request, redirect
from flask import Flask
from flask_pymongo import PyMongo
import html
import time

from database import Database_Handler

database=Database_Handler()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# [User accounts]
# Each user's profile must track at least one value related to that user (eg. display name, avatar, number of wins, etc.)
# Users must have a way to view this data for their own profile. They do not have to have a way to change this data (eg. display name, avatar can be chosen at account creation and never change)

@app.route("/")
def hello_world():
    #if auth
    # return redirect("/home")
    #else
    return redirect("/welcome")

@app.route("/welcome")
def welcome():
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
        username=html.escape(username)
        profile = {'username': username, "password": password}
        

        print(profile)
        #boolean containing T/F on whether account was created or username is in use
        registered = database.add_new_user(username = username, password = password)
        # user_collection.insert_one(profile)
        if registered:
            return redirect("/home", code=301)
        
        test = "Username Already in Use"
        return render_template("signup.html", error = test)
        
    return redirect("/signupForm",code=301)


@app.route("/loginForm", methods=['POST', 'GET'])
def loginForm():
    return render_template("login.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        print(request.form.keys())
        username = request.form['email']
        password = request.form['password']
        username = html.escape(username)
        logged = database.authenticate(username = username, password = password)
        if logged:
            return redirect("/home")
    test = "Incorrect Credentials"
    return render_template("login.html", error = test)


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/user")
def user():
    return render_template("user.html")

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')

# if __name__=="__main__":
#     app = Flask(__name__)
#     app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#     mongo_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
#     db = mongo_client.db

#     user_collection = db['users']
#     leaderboard_collection = db['leaderboard']
