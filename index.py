#all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests
from logging.handlers import RotatingFileHandler


# configuration
DATABASE = '/tmp/instadough.db'
DEBUG = True
IG_CLIENT_ID = 'c05fe5e5ea30400fbf66f088560b259e'
IG_CLIENT_SECRET = 'fc3481826bba47c682b4c627cd60722b'
IG_REDIRECT_URI = 'http://instadough.co/oauthsuccess'
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'
from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

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
    app.logger.info('start of oath')
    code = request.args.get('code', '')
    oathparams = {
            'client_id': IG_CLIENT_ID,
            'client_secret':IG_CLIENT_SECRET,
            'grant_type':authorization_code,
            'redirect_uri':IG_REDIRECT_URI,
            'code':code 
    }
    app.logger.info('sending post request')
    r = requests.post("https://api.instagram.com/oauth/access_token", data = oauthparams)
    response = r.json()
    if response['access_token']:
        'got valid response'
        session['ig_token'] = response['access_token']
        return redirect(url_for('show_mainpage'), code=302)
    else:
        return redirect(url_for('show_index'), code=302)
    # access_token = request.args.get('access_token', '')
    # session['ig_token'] = True
    # return redirect(url_for('show_mainpage'), code=302)

if __name__ == "__main__":
    handler = RotatingFileHandler('debug.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8080)
