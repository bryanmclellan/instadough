#all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing


# configuration
DATABASE = '/tmp/instadough.db'
DEBUG = True
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
def show_users():
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

@app.route('/add', methods=['POST'])
def add_user():
    # if not session.get('logged_in'):
        # abort(401)
    g.db.execute('insert into users (username, password, nessie_id) values (?, ?, ?)',
                 [request.form['username'], request.form['password'], request.form['nessie_id']])
    g.db.commit()
    flash('New user was successfully posted')
    return redirect(url_for('show_users'))

@app.route('/oauthsuccess')
def instagram_oauth():
    access_token = request.args.get('access_token', '')
    session['ig_token'] = True
    return redirect(url_for('show_mainpage'), code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
