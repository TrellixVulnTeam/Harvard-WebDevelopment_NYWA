import os


from flask import Flask, session, render_template, request,redirect, session, request, url_for, flash, session
from flask_session import Session

from functools import wraps

from flask_socketio import SocketIO, emit, send



app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Keep track of channels created (Check for channel name)
channelsCreated = []

#keep track of users connected
users_connected = []

#handles send message event
@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)


#On ‘my event’, function receives the json objects and sends it to the ‘my response’ event in js.
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json)


def login_required(f):
    """
       Decorate routes to require login.

       http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
       """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        #using dict.get() to see if user has logged in
        if not session.get('logged_in'):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    if not session.get('logged_in'):
        return redirect(url_for('channels'))
    else:
        return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":

            flash('You were successfully logged in')

            username = request.form.get("your_name")
            session['logged_in'] = True
            session['user'] = username
            users_connected.append(session['user'])
            print(users_connected)
            session.permanent = True

            return redirect(url_for('channels'))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    try:
        users_connected.remove(session['username'])
    except ValueError:
        pass

    session.clear()

    return redirect(url_for('login'))




@app.route("/channels",methods=["GET","POST"])
@login_required
def channels():
    if request.method == "POST":
        new_channel = request.form.get('channel')
        channelsCreated.append(new_channel)
        return render_template('index.html',channelsCreated=channelsCreated)


    return render_template('index.html',channelsCreated=channelsCreated)

@app.route("/chat/<channel_link>",methods=["GET","POST"])
@login_required
def chat(channel_link):
    channel_id = channel_link
    messages = ['message 1', 'message 2']
    return render_template('chat.html', messages = messages,channel_id=channel_id,channelsCreated=channelsCreated)

if __name__ == '__main__':
	socketio.run(app)