from flask import render_template, Flask, request
import flask
import flask_login
import threading
import Main_Run
import Main_backend as back
import gevent
from gevent import monkey

monkey.patch_all()
import requests
import barset as barget
from flask import Blueprint

# from . import db

# monkey.patch_all()

# app = Blueprint('main', __name__)

app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!

flask_login.login_manager = flask_login.LoginManager()

flask_login.login_manager.init_app(app)

users = {'ryanrocksforever@icloud.com': {'password': 'sheeprock12'}}

booleantoken = "27545ef1-d7f8-45cb-9f14-739ee6777fe6"
booleanid = "b98a6c8b-fda9-4f0f-af42-a4d9323f51ab"

global alreadyrunning


class User(flask_login.UserMixin):
    pass


@flask_login.login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@flask_login.login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


global greenlet
print("got here")
stop_event = threading.Event()
mainthread = threading.Thread(target=Main_Run.mainstuff, daemon=True, args=(stop_event,))
print("got here2")


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/main')
@flask_login.login_required
def main(name=None):
    global alreadyrunning
    # profit = 233
    print("endprice")
    endprice = back.Actions().project(option="AAPL")
    print("price:")
    price = barget.get("AAPL")
    print("profit:")
    profit = back.Actions().profit()
    #print(profit)
    orders = back.Actions().getorders()
    line = orders["symbol"] + ",_______" + orders["filled_qty"] + ",________" + orders["side"]
    return render_template('hello.html', name=name, endprice=endprice, running=alreadyrunning, price=price,
                           profit=profit, orders=line)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id + '<head>  <meta http-equiv="refresh" content="1; URL=/main" /></head><body>  <p>If you are not redirected in five seconds, <a href="https://127.0.0.1:5000/">click here</a>.</p></body>'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@flask_login.login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/run', methods=['POST', 'GET'])
def run():
    global alreadyrunning
    global greenlet
    if request.method == 'GET':
        if mainthread.is_alive():
            return {"alive": "true"}
        if not mainthread.is_alive():
            return {"alive": "false"}

    if request.method == 'POST':
        patch = requests.patch("https://api.booleans.io/" + booleanid, data={'label': 'True'},
                               headers={"Authorization": "Token " + booleantoken})
        print(patch.text)

        alreadyrunning = True
        greenlet = gevent.spawn(Main_Run.mainstuff)
        print("starting")
        return '<head>  <meta http-equiv="refresh" content="1; URL=/main" /></head><body>  <p>If you are not redirected in five seconds, <a href="https://127.0.0.1:5000/">click here</a>.</p></body>'


@app.route('/stop', methods=['POST'])
def stop():
    global alreadyrunning
    if request.method == 'POST':
        patch = requests.patch("https://api.booleans.io/" + booleanid, data={'label': 'False'},
                               headers={"Authorization": "Token " + booleantoken})
        print(patch.text)

        alreadyrunning = False
        global greenlet
        print("stopping")
        # stop_event.set()
        # mainthread.kill()
        try:
            greenlet.kill()
        except:
            print("cant kill")
        print("stopped")
        return '<head>  <meta http-equiv="refresh" content="1; URL=/main" /></head><body>  <p>If you are not redirected in five seconds, <a href="https://127.0.0.1:5000/">click here</a>.</p></body>'


# isrunning = requests.get("https://api.booleans.io/" + booleanid)
# jsoncontent = isrunning.json()
# value = jsoncontent["label"]
# print(value)
# if "True" in value:
#     greenlet = gevent.spawn(Main_Run.mainstuff)
#     print("starting")
#     alreadyrunning = True
#
# else:
#     alreadyrunning = False

if __name__ == '__main__':
    app.run()
