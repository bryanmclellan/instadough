#all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_from_directory, make_response, \
     send_file
from contextlib import closing
import requests, json
from logging.handlers import RotatingFileHandler
import logging
from app import *
import urllib2

# configuration
DATABASE = '/tmp/instadough.db'
DEBUG = True
IG_CLIENT_ID = 'c05fe5e5ea30400fbf66f088560b259e'
IG_CLIENT_SECRET = 'fc3481826bba47c682b4c627cd60722b'
IG_REDIRECT_URI = 'http://instadough.co/create-account.html'

# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(__name__)

app.secret_key = 'c05fe5e5ea30400fbf66f088560b259e'

def query_db(query, args=(), one=True):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if hasattr(rv, '__iter__'):
        return rv[0] if len(rv) > 0 else ''
    else:
        return rv

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
    access_token_justin = '774251592.c05fe5e.e9ccb4581efb49bebbade115105fbd08'
    access_token_grant = '963309449.c05fe5e.53a36e2b5b5741d79bc5b35b1ef8bd07'
    resp = requests.request('GET','https://api.instagram.com/v1/users/self/media/recent/?access_token=' + access_token)
    resp_justin = requests.request('GET','https://api.instagram.com/v1/users/self/media/recent/?access_token=' + access_token_justin)
    resp_grant = requests.request('GET','https://api.instagram.com/v1/users/self/media/recent/?access_token=' + access_token_grant)
    # print(json.loads(resp.content))

    dict = json.loads(resp.content)
    dict_justin = json.loads(resp_justin.content)
    dict_grant = json.loads(resp_grant.content)
    if len(dict["data"]) == 0:
        print("we got nothing")

    data = dict["data"] + dict_justin["data"] + dict_grant["data"]
    session["images"] = []
    session["caption"] = []
    for i in xrange(0,len(data)):
        print(data[i]["user"])
        dictionary = data[i]["images"]['standard_resolution']
        dictionary["tags"] = data[i]["tags"]
        dictionary["username"] = data[i]["user"]["username"]
        rv = g.db.execute('select id, username from users where username = "{}"'.format(dictionary["username"]))
        for row in rv:
            dictionary["to_id"] = str(row[0])
        dictionary["caption"] = data[i]["caption"]["text"]
        dictionary["id"] = data[i]["id"]
        session["images"].append(dictionary)
        # session["caption"].append(data[i]["caption"]["text"].lower())
        session['caption'].append(dictionary['caption'].lower())
    
    # images = [{'url':'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e35/12424344_180566928966669_438670868_n.jpg', 'width':678, 'height': 678},
            # {'url': 'https://scontent.cdninstagram.com/hphotos-xtf1/t51.2885-15/e35/12545483_1197925680258714_777727123_n.jpg', 'width':640, 'height': 640},
            # {'url': 'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e35/12547117_1152951288063483_1691935294_n.jpg', 'width':640, 'height': 640}]
    
    return render_template('main.html', images=session['images'])

@app.route('/charge.html', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    g.db.execute('insert into history values (?, ?, ?, ?)',
        [request.form['from_id'], request.form['to_id'], request.form['image_url'], request.form['image_id']])
    g.db.commit()


    f = urllib2.urlopen(str(request.form['image_url']))
    return send_file(f, mimetype='image/jpg', as_attachment=True,\
            attachment_filename='{}.jpg'.format(request.form['image_id']))
    # img = f.read()

    # headers = {"Content-Disposition:": "attachment; filename={}.jpg".format(request.form['image_id'])}

    # return make_response((img, headers))

@app.route('/search.html', methods=['POST'])
def search():
    text = request.form["search"].lower()
    session["search_results"] = []
    for i in xrange(0,len(session["images"])):
        if text in session["caption"][i]:
            session["search_results"].append(session["images"][i])

    return render_template('main.html', images=session["search_results"])


@app.route('/profile.html')
def show_profile():
    # for user in query_db('select * from users'):
    #     print user['username'], 'has the id', user['user_id']
    name = g.db.execute('select * from users where id = ' + str(session['user_id']))
    namerv = name.fetchall()
    for row in namerv:
        username = row[1]

    cur = g.db.execute('select * from history')
    rv = cur.fetchall()

    finalFromNames = []
    fromNames = g.db.execute('select from_id from history')
    for n in fromNames:
        print(n)
        r = g.db.execute('select * from users where id = ' + n[0])
        for name in r:
            finalFromNames.append(name[1])

    finalToNames = []
    toNames = g.db.execute('select to_id from history')
    for n in toNames:
        r = g.db.execute('select * from users where id = ' + n[0])
        for name in r:
            finalToNames.append(name[1])



    return render_template('profile.html', fromNames=finalFromNames, toNames=finalToNames, rows=rv, name=username)

@app.route('/dumptables')
def dump_tables():
    usernames = g.db.execute('select * from users')
    history = g.db.execute('select * from history')
    usr_str = ""
    for username in usernames:
        usr_str += ("".join(map(str, username)))
        usr_str += ("<br/>")
    history_str = ""
    for his in history:
        history_str += ("".join(map(str, his)))
        history_str += ("<br/>")

    return "<html><body>" + usr_str + history_str + "</body></html>"

# def query_db(query, args=(), one=False):
#     cur = g.db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv


# @app.route('/add', methods=['POST'])
# def add_user():
    # # if not session.get('logged_in'):
        # # abort(401)
    # g.db.execute('insert into users (username, password, nessie_id) values (?, ?, ?)',
    #              [request.form['username'], request.form['password'], request.form['nessie_id']])
    # g.db.commit()
    # flash('New user was successfully posted')
    # return redirect(url_for('show_users'))

@app.route('/login.html', methods=['GET'])
def login():
    #do_the_login()
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    if (username != '' and password != ''):
        cur = g.db.execute('select id, username, password from users order by id desc')
        rv = cur.fetchall()#[dict(title=row[0], text=row[1]) for row in cur.fetchall()]
        for row in rv:
            if row[1] == username and row[2] == password:
                session['user_id'] = row[0]
                return redirect(url_for('show_mainpage'), code=302)
        return render_template('login.html', failed = True)
    else:
        return render_template('login.html')

@app.route('/create-account.html')
def create_account():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    if (username != '' and password != ''):
        cur = g.db.execute('select id, username, password from users where username = "{}"'.format(username))
        for row in cur.fetchall():
            return render_template('create-account.html', failed = True)
        g.db.execute('insert into users (username, password) values (?, ?)', [username, password])
        g.db.commit()
        rv = g.db.execute('select id, username from users where username = ?', username)
        for row in rv:
            session['user_id'] = str(row[0])
        # return session['user_id']
        return redirect(url_for('show_mainpage'), code=302)
    else:
        return render_template('create-account.html')


def add_user():
    # if not session.get('logged_in'):
        # abort(401)
    g.db.execute('insert into users (username, password, nessie_id) values (?, ?, ?)',
                 [request.form['username'], request.form['password'], request.form['nessie_id']])
    g.db.commit()
    flash('New user was successfully posted')
    return redirect(url_for('show_users'))

@app.route('/oauthsuccess.html')
def instagram_oauth():
#    return "Hello there"
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
    app.logger.info(r.text)
#    if 'access_token' in response:
#        session['ig_token'] = response['access_token']
    return redirect(url_for('show_mainpage'), code=302)
#    else:
#        return redirect(url_for('show_index'), code=302)
    # access_token = request.args.get('access_token', '')
    # session['ig_token'] = True
    # return redirect(url_for('show_mainpage'), code=302)

if __name__ == "__main__":
    handler = RotatingFileHandler('debug.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8080, debug=True)

