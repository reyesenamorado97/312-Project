from flask import Blueprint, render_template, send_from_directory, redirect

views =Blueprint('views',__name__)

@views.route("/")
def home():
    return redirect("/welcome", code=301)
    #if auth
    # redirect to /lobby/
    #else
    # redirect to /welcome
    pass

@views.route("/welcome")
def welcome():
    return render_template("welcome.html")

@views.route("/templates/<file>")
def navbar(file):
    return send_from_directory('templates',file)

@views.route("/images/<image>")
def hero(image):
    return send_from_directory('images',image)