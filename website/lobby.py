from flask import Blueprint, render_template, send_from_directory, redirect

lobby =Blueprint('lobby',__name__)

@lobby.route("/home")
def loadHome():
    return render_template("home.html")