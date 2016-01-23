#all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests, json
from logging.handlers import RotatingFileHandler
import logging


# configuration
DATABASE = '/tmp/instadough.db'
DEBUG = True
IG_CLIENT_ID = 'c05fe5e5ea30400fbf66f088560b259e'
IG_CLIENT_SECRET = 'fc3481826bba47c682b4c627cd60722b'
IG_REDIRECT_URI = 'http://instadough.co/oauthsuccess.html'
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'
from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'c05fe5e5ea30400fbf66f088560b259e'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_index():
    # cur = g.db.execute('select username, nessie_id from users order by id desc')
    # users = [dict(username=row[0], nessie_id=row[1]) for row in cur.fetchall()]
    # return render_template('show_users.html', users=users)
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('main.html')

@app.route('/main.html')
def show_mainpage():
    # if not session.get('images'):
    access_token = '213665890.c05fe5e.5f748d07a787466a9044883e1176a18a'

    resp = requests.request('GET','https://api.instagram.com/v1/users/self/media/recent/?access_token=' + access_token)
    # print(json.loads(resp.content))
    dict = json.loads(resp.content)
    if len(dict["data"]) == 0:
        print("we got nothing")

    data = dict["data"]
    session["images"] = []
    session["caption"] = []
    for i in xrange(0,len(data)):
        session["images"].append(data[i]["images"]['standard_resolution'])
        session["caption"].append(data[i]["caption"]["text"].lower())
    
    # images = [{'url':'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e35/12424344_180566928966669_438670868_n.jpg', 'width':678, 'height': 678},
            # {'url': 'https://scontent.cdninstagram.com/hphotos-xtf1/t51.2885-15/e35/12545483_1197925680258714_777727123_n.jpg', 'width':640, 'height': 640},
            # {'url': 'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e35/12547117_1152951288063483_1691935294_n.jpg', 'width':640, 'height': 640}]
    
    return render_template('main.html', images=session['images'])


@app.route('/search.html', methods=['POST'])
def search():
    text = request.form["search"].lower()
    session["search_results"] = []
    for i in xrange(0,len(session["images"])):
        if text in session["caption"][i]:
            session["search_results"].append(session["images"][i])
            print(session["search_results"])

    return render_template('main.html')


# @app.route('/add', methods=['POST'])
# def add_user():
    # # if not session.get('logged_in'):
        # # abort(401)
    # g.db.execute('insert into users (username, password, nessie_id) values (?, ?, ?)',
                 # [request.form['username'], request.form['password'], request.form['nessie_id']])
    # g.db.commit()
    # flash('New user was successfully posted')
    # return redirect(url_for('show_users'))

@app.route('/oauthsuccess.html')
def instagram_oauth():
    return "Hello there."
    app.logger.info('start of oath')
    code = request.args.get('code', '')
    oauthparams = {
            'client_id': IG_CLIENT_ID,
            'client_secret':IG_CLIENT_SECRET,
            'grant_type':'authorization_code',
            'redirect_uri':IG_REDIRECT_URI,
            'code':code 
    }
    app.logger.info('sending post request')
    r = requests.post("https://api.instagram.com/oauth/access_token", data = oauthparams)
    response = r.json()
    app.logger.info(response.text)
    return redirect(url_for('show_mainpage'), code=302)
    # access_token = request.args.get('access_token', '')
    # session['ig_token'] = True
    # return redirect(url_for('show_mainpage'), code=302)

if __name__ == "__main__":
    handler = RotatingFileHandler('debug.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8080, debug=True)

