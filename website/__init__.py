from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

#--- Database object intialized
from db import Databse_Handler
database=Databse_Handler()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='hsfjdsfjnoaolnsuveueoop'
    app.config['MONGO_URI']="mongodb://localhost:27017/databaseOne"

    # from .extension import mongo
    # mongo.init_app(app,uri="mongodb://localhost:27017/databaseOne")
    # mongo=PyMongo(app)
    # users_collection=mongo.db.users
    app.logger.warning("hello")

    from .auth import auth
    from .game import game
    from .lobby import lobby
    from .user_edit import user_edit
    from .views import views

    # app.register_blueprint(db,url_prefix="/db") 
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/auth")
    app.register_blueprint(game,url_prefix="/game")
    app.register_blueprint(lobby,url_prefix="/lobby")
    app.register_blueprint(user_edit,url_prefix="/user_edit")

    return app