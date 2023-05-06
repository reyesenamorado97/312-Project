from flask import Blueprint, render_template, send_from_directory, redirect

#--- Importing the database object from __init__ (website project)
from website import database

user_edit =Blueprint('user_edit',__name__)