from flask import Blueprint, render_template, send_from_directory, redirect

auth =Blueprint('auth',__name__)

@auth.route("/")
def home():
    return redirect("/welcome", code=301)
    #if auth
    # redirect to /lobby/
    #else
    # redirect to /welcome
    pass

@auth.route("/welcome")
def welcome():
    return render_template("welcome.html")
    
