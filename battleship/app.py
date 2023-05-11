from flask import Flask, render_template, send_from_directory, request, redirect, jsonify
from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import html
import json
import random


from database import Database_Handler

game_rooms={}

database=Database_Handler()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET-KEY']="munch"
socketio=SocketIO(app=app)


# [User accounts]
# Each user's profile must track at least one value related to that user (eg. display name, avatar, number of wins, etc.)
# Users must have a way to view this data for their own profile. They do not have to have a way to change this data (eg. display name, avatar can be chosen at account creation and never change)

@app.route("/")
def hello_world():
    #if auth
    # return redirect("/home")
    #else
    return redirect("/welcome")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/templates/<file>")
def templates(file):
    return send_from_directory('templates', file)


# @app.route("/static/<file>")
# def static(file):
#     return send_from_directory('static', file)


@app.route("/images/<image>")
def hero(image):
    return send_from_directory('images', image)


@app.route("/signupForm", methods=['POST', 'GET'])
def signupForm():
    return render_template("signup.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        username=html.escape(username)
        profile = {'username': username, "password": password}
        

        print(profile)
        #boolean containing T/F on whether account was created or username is in use
        registered = database.add_new_user(username = username, password = password)
        # user_collection.insert_one(profile)
        if registered:
            return redirect("/home", code=301)
        
        test = "Username Already in Use"
        return render_template("signup.html", error = test)
    return redirect("/signupForm",code=301)


@app.route("/loginForm", methods=['POST', 'GET'])
def loginForm():
    return render_template("login.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        print(request.form.keys())
        username = request.form['email']
        password = request.form['password']
        username = html.escape(username)
        logged = database.authenticate(username = username, password = password)
        if logged:
            redirect_response = redirect("/home")
            redirect_response.set_cookie("authToken", "random_cookie_value")
            return redirect_response
    test = "Incorrect Credentials"
    return render_template("login.html", error = test)


@app.route("/home")
def home():
    auth_token = request.cookies.get('authToken')
    print(auth_token)
    return render_template("home.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/currentGames")
def send_rooms():
    rooms={"rooms":list(game_rooms.keys())}
    return jsonify(rooms)

@app.route("/leaderboard")
def send_leaderboard():
    leaderboardData={'leaderboard':[('munch',85),('Adavita',65), ('munchGod',40),('Ethanial',65)]}
    return jsonify(leaderboardData)


@app.route("/lobby")
def lobby():
    user=random.randint(0,1000)
    win_button=random.randint(1,16)
    game_rooms[0]=[[user],[win_button]]
    return render_template("lobby.html")

@app.route("/game")
def game():
    return render_template("game.html")
### game
# user_num=0
# room_num=0
# game_rooms={1:[[],[]],2:[[],[]]}
# @app.route("/lobby")
# def lobby(data):
#     #game_rooms
#     data=json.loads(data)


#     win_button=random.randint(1,16)
#     game_rooms[room_num]=[[user_num],[win_button]]

#     return render_template("lobby.html")



### Websocket Stuff ###
@socketio.on('connect')
def connect():
    if 'room0' not in game_rooms:
        win_button=random.randint(1,16)
        game_rooms['room0']=[[request.sid],[win_button]]
        join_room('room0')
        
    else:
        win_button=random.randint(1,16)
        game_rooms['room0'][0].append(request.sid)
        game_rooms['room0'][1].append(win_button)
        join_room('room0')

    test=json.dumps({"room":"room0",'youAre':request.sid})
    emit('room',test,to=request.sid)
    pass

@socketio.on('disconnect')
def disconnect():
    print('disconnected')
    pass

@socketio.on('button')
def socket_message(data):
    button=int(data['button'].split('n')[1])
    room=data['room']
    info=game_rooms[room]
    ans={'user':data['user'],'winner':'None'}
    # ans2={'user':info[0][1],'won':False,'lost':False}
    
    
    print(info)
    # print(data['user'])
    # emit('gameResponse',ans1,to=room)

    if data['user']==info[0][0]:
        if button==info[1][1]:
            ans['winner']=info[0][0]
        emit('gameResponse',ans,to=room)
        # else:
        #     emit('gameResponse',ans,to=room)
    else:
        if button==info[1][0]:
            ans['winner']=info[0][1]
        emit('gameResponse',ans,to=room)
        #     ans2['won']=True
        #     ans1=json.dumps(ans1)
        #     ans2=json.dumps(ans2)
        #     emit('gameResponse',ans1,to=room)
        #     emit('gameResponse',ans2,to=room)
        # else:
        #     emit('gameResponse',ans1,to=room)
    
    # ans1=json.dumps(ans1)
    # ans2=json.dumps(ans2)
    # emit('gameResponse',ans1,to=info[0][0])
    # emit('gameResponse',ans2,to=info[0][1])

    pass


if __name__=="__main__":
    socketio.run(app,debug=True,host='0.0.0.0',port=8000)
    

