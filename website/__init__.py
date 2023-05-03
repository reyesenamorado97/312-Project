from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='hsfjdsfjnoaolnsuveueoop'

    from .auth import auth
    from .game import game
    from .lobby import lobby
    from .user_edit import user_edit
    from .views import views

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/auth")
    app.register_blueprint(game,url_prefix="/game")
    app.register_blueprint(lobby,url_prefix="/lobby")
    app.register_blueprint(user_edit,url_prefix="/user_edit")

    return app