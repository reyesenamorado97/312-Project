from flask import Blueprint, render_template, send_from_directory, redirect

#--- Importing the database object from __init__ (website project)
from website import database

auth =Blueprint('auth',__name__)

    
@auth.route("/signupForm")
def signupForm():
    return render_template("signup.html")

@auth.route("/loginForm")
def loginForm():
    return render_template("login.html")