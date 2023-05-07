from flask import Blueprint, render_template, send_from_directory, redirect

game =Blueprint('game',__name__)

@game.route("/lobby")
def loadLobby():
    return render_template("lobby.html")

@game.route("/playing")
def playingGame():
    return render_template("game.html")