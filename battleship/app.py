from flask import Flask, render_template, send_from_directory, request, redirect, jsonify
from flask import Flask
# from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import html
import json
import uuid
from werkzeug.urls import url_parse

from database import Database_Handler

database = Database_Handler()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = '2f79c11eff273693c3fffe7c0329aa274221a4e9d7034f42b7df75f76abbeee8'
socketio = SocketIO(app=app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, username, _id=None):

        self.username = username
        self.wins = database.find_user(self.username)["wins"]
        # self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # This method is required for the UserMixin class
    # It returns the username NOT id
    def get_id(self):
        return self.username

    def get_wins(self):
        return self.wins

    def increment_wins(self):
        # increments wins in database
        database.users_collection.update_one(
            {"username": self.username},
            {"$inc": {"wins": 1}}
        )
        # also increments
        self.wins += 1


@login_manager.user_loader
def load_user(username):
    # not sure if we should load by id or username
    user = database.find_user(username)
    if user != None:
        # print("--------------user_loader---------------")
        # print("user is:", user)
        # print("--------------user_loader---------------")
        # TODO: make sure that id is a string?
        return User(user['username'])
    else:
        return False


@app.route("/")
def hello_world():
    if current_user.is_authenticated:
        return redirect("/home", code=301)
    return redirect("/welcome")


@app.route("/welcome")
def welcome():
    if current_user.is_authenticated:
        return redirect("/home", code=301)
    return render_template("welcome.html")


@app.route("/templates/<file>")
def templates(file):
    return send_from_directory('templates', file)


@app.route("/images/<image>")
def hero(image):
    return send_from_directory('images', image)


@app.route("/signupForm", methods=['POST', 'GET'])
def signupForm():
    return render_template("signup.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect("/home", code=301)
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        username = html.escape(username)
        profile = {'username': username, "password": password}

        print(profile)
        # boolean containing T/F on whether account was created or username is in use
        registered = database.add_new_user(
            username=username, password=password)
        # user_collection.insert_one(profile)
        if registered:
            return redirect("/home", code=301)

        test = "Username Already in Use"
        return render_template("signup.html", error=test)
    return redirect("/signupForm", code=301)


@app.route("/loginForm", methods=['POST', 'GET'])
def loginForm():
    return render_template("login.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect("/home", code=301)
    if request.method == 'POST':
        # print(request.form.keys())
        username = request.form['email']
        password = request.form['password']
        # wins = request.form["wins"]
        username = html.escape(username)
        user = database.authenticate(
            username=username, password=password)
        print(user)
        if user != None:
            # redirect_response = redirect("/home")
            # redirect_response.set_cookie("authToken", "random_cookie_value")
            # return redirect_response
            # enter the user into flask_login session
            print(user)
            authenticated_user = User(username)
            login_user(authenticated_user, remember=True)
            # remember=True will set a cookie for the user
            next_page = request.args.get('next')
            print("-----------------------------------")
            print("next_page is:", next_page)
            print("-----------------------------------")
            if not next_page or url_parse(next_page).netloc != '':
                # next_page = url_for('home')
                return redirect("/home", code=301)
            return redirect(next_page, code=301)

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/welcome", code=301)


@app.route("/home")
@login_required
def home():
    # auth_token = request.cookies.get('authToken')
    # print(auth_token)
    return render_template("home.html")


@app.route("/user")
@login_required
def user():
    # Uncomment to increment wins/test leaderboard
    # User.increment_wins(current_user)
    display_name = User.get_id(current_user)
    total_wins = User.get_wins(current_user)

    return render_template("user.html", display_name=display_name, total_wins=total_wins)


@app.route("/edit")
@login_required
def edit():
    return render_template("edit.html")


@app.route("/currentGames")
@login_required
def send_rooms():
    rooms = {"rooms": [1, 2, 3, 4, 5]}
    return jsonify(rooms)


@app.route("/leaderboard")
@login_required
def send_leaderboard():
    return database.create_leaderboard()


@ app.route("/lobby")
@ login_required
def lobby():
    return render_template("lobby.html")


@ app.route("/game")
@ login_required
def game():
    return render_template("game.html")


### Websocket Stuff ###
@ socketio.on('connect')
# Feel free to remove login_required on any of the routes if it makes testing easier
@ login_required
def connect():
    test = json.dumps({"youAre": "Unknown"})
    emit('user', test, broadcast=True)
    pass


@ socketio.on('disconnect')
def disconnect():
    print('disconnected')
    pass


@ socketio.on('message')
def socket_message():
    pass


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
