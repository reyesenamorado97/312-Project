from database import Database_Handler
from flask import Flask, render_template, send_from_directory, request, redirect, jsonify, make_response
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import html
import json
import uuid
import random
from werkzeug.urls import url_parse
from keys import secret_key

database = Database_Handler()

future_users = {}
room_num = [0]
game_rooms = {}
list_rooms = set()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secret_key
socketio = SocketIO(app=app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin):
    # room=None
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
        return User(user['username'])
    else:
        return False


def create_response(arg):
    response = make_response(arg)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route("/")
def hello_world():
    if current_user.is_authenticated:
        return create_response(redirect("/home", code=301))
    return create_response(redirect("/welcome", code=301))


@app.route("/welcome")
def welcome():
    if current_user.is_authenticated:
        return create_response(redirect("/home", code=301))
    return create_response(render_template("welcome.html"))


@app.route("/templates/<file>")
def templates(file):
    return create_response(send_from_directory('templates', file))


@app.route("/images/<image>")
def hero(image):
    return create_response(send_from_directory('images', image))


@app.route("/signupForm", methods=['POST', 'GET'])
def signupForm():
    return create_response(render_template("signup.html"))


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return create_response(redirect("/home", code=301))
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        username = html.escape(username)
        # profile = {'username': username, "password": password}

        # boolean containing T/F on whether account was created or username is in use
        registered = database.add_new_user(
            username=username, password=password)
        # user_collection.insert_one(profile)
        if registered:
            return create_response(redirect("/loginForm", code=301))

        test = "Username Already in Use"
        return create_response(render_template("signup.html", error=test))
    return create_response(redirect("/signupForm", code=301))


@app.route("/loginForm", methods=['POST', 'GET'])
def loginForm():
    return create_response(render_template("login.html"))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return create_response(redirect("/home", code=301))
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        # wins = request.form["wins"]
        username = html.escape(username)
        user = database.authenticate(
            username=username, password=password)
        if user:
            # enter the user into flask_login session
            authenticated_user = User(username)
            login_user(authenticated_user, remember=True)
            # remember=True will set a cookie for the user
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                # next_page = url_for('home')
                return create_response(redirect("/home", code=301))
            return create_response(redirect(next_page, code=301))

    return create_response(render_template("login.html", error="Incorrect Credentials"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return create_response(redirect("/welcome", code=301))


@app.route("/home")
@login_required
def home():
    return create_response(render_template("home.html"))


@app.route("/user")
@login_required
def user():
    # Uncomment to increment wins/test leaderboard
    # User.increment_wins(current_user)
    display_name = User.get_id(current_user)
    total_wins = User.get_wins(current_user)

    return create_response(render_template("user.html", display_name=display_name, total_wins=total_wins))


@app.route("/edit")
@login_required
def edit():
    return create_response(render_template("edit.html"))


@app.route("/currentGames")
@login_required
def send_rooms():
    rooms = {"rooms": list(list_rooms)}
    return create_response(jsonify(rooms))


@app.route("/leaderboard")
@login_required
def send_leaderboard():
    return create_response(database.create_leaderboard())


@ app.route("/lobby")
@ login_required
def lobby():
    return create_response(render_template("lobby.html"))

# game


@ app.route("/game")
@ login_required
def game():
    return create_response(render_template("game.html"))


@app.route('/game/<room>')
@ login_required
def join_game(room):
    if room in list_rooms:
        future_users[current_user.username] = room
        list_rooms.remove(room)
        return create_response(render_template("game.html"))
    return create_response(redirect("/home", code=301))


### Websocket Stuff ###
@socketio.on('connect')
# Feel free to remove login_required on any of the routes if it makes testing easier
@login_required
def connect():
    room = ''
    start = False
    user = current_user.username
    if user in future_users:
        room = future_users[user]
        del future_users[user]
        win_button = random.randint(1, 16)
        game_rooms[room][0].append(user)
        game_rooms[room][1].append(win_button)
        start = True
        join_room(room)
    else:
        room = 'room'+str(room_num[0])
        room_num[0] += 1
        win_button = random.randint(1, 16)
        game_rooms[room] = [[user], [win_button]]
        list_rooms.add(room)
        join_room(room)

    test = json.dumps({"room": room, 'youAre': user, "start": start})
    emit('room', test, to=request.sid)
    if len(game_rooms[room][0]) == 2:
        players = json.dumps(
            {"p1": game_rooms[room][0][0], "p2": game_rooms[room][0][1]})
        emit('players', players, to=room)
    pass


@socketio.on('disconnect')
def disconnect():
    pass


@socketio.on('button')
def socket_message(data):
    button = int(data['button'].split('n')[1])
    room = data['room']
    info = game_rooms[room]
    ans = {'user': data['user'], 'winner': 'None'}

    if data['user'] == info[0][0]:
        if button == info[1][1]:
            ans['winner'] = info[0][0]
            del game_rooms[room]
            current_user.increment_wins()
        emit('gameResponse', ans, to=room)
    else:
        if button == info[1][0]:
            ans['winner'] = info[0][1]
            del game_rooms[room]
            current_user.increment_wins()
        emit('gameResponse', ans, to=room)
    pass


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
