from flask import Blueprint, render_template, send_from_directory, redirect
import sys
from flask import current_app as app
from pymongo import MongoClient

#--- Importing the database object from __init__ (website project)
from website import database



views =Blueprint('views',__name__)
@views.route("/testdb")
def testdb():
    database.testdb()
    return "Hello"

@views.route("/")
def home():
    print("hi")
    return redirect("/welcome", code=301)
    pass

@views.route("/welcome")
def welcome():
    return render_template("welcome.html")

@views.route("/templates/<file>")
def templates(file):
    return send_from_directory('templates',file)

@views.route("/static/<file>")
def static(file):
    return send_from_directory('static',file)

@views.route("/images/<image>")
def hero(image):
    return send_from_directory('images',image)