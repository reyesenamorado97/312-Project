from flask import Blueprint, render_template, send_from_directory, redirect

#--- Importing the database object from __init__ (website project)
from website import database

lobby =Blueprint('lobby',__name__)

@lobby.route("/home")
def loadHome():
    return render_template("home.html")