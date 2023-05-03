from flask import Blueprint, render_template, send_from_directory, redirect

auth =Blueprint('auth',__name__)

@auth.route("/")
def home():
    #if auth
    # redirect to /lobby
    #else
    # redirect to /welcome
    pass

@auth.route("/welcome")
def welcome():
    #return welcome page
    pass
