# -*- coding: utf-8 -*-
import os
import datetime
from werkzeug import secure_filename
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# import model
import myhash

app_path = os.getcwd()

#configuration----------------------------------------------------------------
DATABASE = '/tmp/blog.db'
DEBUG = True
SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD ='default'
UPLOAD_FOLDER = app_path + '/files'

#database utils---------------------------------------------------------------
def init_db():
    """Initializes the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet
    for the current application context."""
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    res = cur.fetchall()
    cur.close()
    return (res[0] if res else None) if one else res

#create application-----------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(__name__) # import and look for all UPPERCASE variables defined

#@app.cli.command('initdb')
#def initdb_command():
#    init_db()
#
#@app.before_request
#def before_request():
#    init_db()
#    g.db = connect_db()

@app.teardown_appcontext
def close_db(error):
    """Close the databases again."""
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

@app.route('/') #---------- homepage ----------
def homepage():
    g.db = connect_db()
    cur = g.db.execute('select entries.id, entries.userid, entries.title, entries.create_time, entries.text, users.username from entries, users where entries.userid=users.id order by entries.create_time desc')
    entries = cur.fetchall()
    return render_template('homepage.html', entries=entries)

@app.route('/add', methods=['POST']) #---------- add_entry ----------
def add_entry():
    if not session.get('logged_in'):
        abort(401) # will never happen
    db = get_db()
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if not session.get('userid'): session['userid'] = -1
    db.execute('insert into entries (userid, title, create_time, text) values (?, ?, ?, ?)',
            [session['userid'], request.form['title'], cur_time, request.form['text']])
    db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('homepage'))

def get_userid(username):
    g.db = connect_db()
    res = g.db.execute('select id from users where username="%s"' % username).fetchall()
    return -1 if (len(res) == 0) else res[0][0]

@app.route('/sign_up', methods=['GET', 'POST']) #---------- sign up ----------
def sign_up():
    error = None
    if request.method == 'POST':
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        username = request.form['username']
        password = request.form['password']
        if myhash.check_text(username, password) is False:
            error = "Invalid Input."
            return render_template('homepage.html', signup_error=error) #return render_template('sign_up.html', error=error)
        g.db = connect_db()
        cur = g.db.execute('select username from users where username="%s"' % username)
        if len(cur.fetchall()) != 0:
            error = "Username already exist."
            return render_template('homepage.html', signup_error=error) #return render_template('sign_up.html', error=error)
        password = myhash.calc_sha1(password)
        db = get_db()
        db.execute('insert into users (username, password, create_time, birthday, sex, description) values (?, ?, ?, "", -1, "")',
                [username, password, cur_time])
        db.commit()
        flash('Welcome New user: %s!' % username)
        session['logged_in'] = True
        session['username'] = username
        session['userid'] = get_userid(username)
        flash('You are logged in, %s' % username)
        return redirect(url_for('homepage'))
    return render_template('homepage.html', signup_error=error) #return render_template('sign_up.html', error=error)

def login_check(username, password): #---------- login [check]----------
    if session.get('logged_in'):
        abort(401) # TODO: SHOW a message "Please logout first"
    g.db = connect_db()
    cur = g.db.execute('select id, username, password from users where username="%s"' % username)
    users = cur.fetchall()
    if len(users) == 0:
        return -2
    else:
        assert(len(users) == 1)
        if (users[0][2] == myhash.calc_sha1(password) ):
            return users[0][0]
        else:
            return -1

@app.route('/login', methods=['GET', 'POST']) #---------- login ----------
def login():
    error = None
    if request.method ==  'POST':
        res = login_check(request.form['username'], request.form['password'])
        if res == -2:
            error = 'Username not exist!'
        elif res == -1:
            error = 'Wrong password!'
        else:
            session['logged_in'] = True
            session['userid'] = res
            session['username'] = request.form['username']
            flash('You are logged in!')
            return redirect(url_for('homepage'))
    return render_template('homepage.html', login_error=error) 

@app.route('/logout') #---------- logout ----------
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('homepage'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method ==  'POST':
        db = get_db()
        if len(request.form['password']) >=3:
            password = myhash.calc_sha1( request.form['password'] )
            db.execute('update users set password="%s", birthday="%s", description="%s", sex="%s" where id="%s"' % 
                (password, request.form['birthday'], request.form['description'], request.form['sex'], str(session["userid"])) )
        else:
            db.execute('update users set birthday="%s", description="%s", sex="%s" where id="%s"' % 
                (request.form['birthday'], request.form['description'], request.form['sex'], str(session["userid"])) )
        db.commit()
        return redirect(url_for('user', username=session["username"]))
    g.db = connect_db()
    res = g.db.execute('select id, username, create_time, birthday, sex, description from users where id="%s"' % str(session["userid"]) ).fetchall()
    assert len(res) == 1 # TODO: Need test
    return render_template('profile.html', userinfo=res[0])
    
@app.route('/user/<username>')
def user(username):
    error = None
    g.db = connect_db()
    res = g.db.execute('select id, username, create_time, birthday, sex, description from users where username="%s"' % username).fetchall()
    userinfo = (list)(res[0])
    userinfo[4] = myhash.sex_repr(userinfo[4])
    if len(res) == 0:
        error = "User not found! Show admin instead."
        res = g.db.execute('select id, username, create_time, birthday, sex, description from users where username="admin"').fetchall()
    return render_template('user.html', userinfo=userinfo, error=error)
    

@app.route('/video')
def show_video():
    return render_template('show_video.html')

@app.route('/music')
def set_music():
    return render_template('set_music.html')

@app.route('/upload', methods=['GET', 'POST']) #---------- upload ----------
def upload():
    if request.method == 'POST':
        file = request.files['file'] # use [files] dictionary on the request object
        text = request.form['text']
        if file and myhash.check_filename(file.filename):
            filename = secure_filename(file.filename) # secure_filename(): Strip filename To ASCII string
            # TODO: filename DIY, user
            # TODO: file already exist
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # save(): save file permanently
            if not session.get('userid'): session['userid'] = -1
            cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            db = get_db()
            db.execute('insert into files (userid, filename, upload_time, text) values (?, ?, ?, ?)',
                    [session['userid'], filename, cur_time, text])
        db.commit()
        flash('File Uploaded!')
        return redirect(url_for('uploaded', filename=filename)) # Uploaded Successfully, Redirect to [uploaded]
    # Upload Failed ? or List
    g.db = connect_db()
    cur = g.db.execute('select id, userid, filename, upload_time, text from files order by upload_time desc')
    all = cur.fetchall()
    # ID, UID, filename, up_time, text
    file_dict = []
    for index in xrange(len(all)):
        aid, auid, afile, atime, atext = ((list)(all[index]))[0:5]
        apath = os.path.join(app.config['UPLOAD_FOLDER'], afile)
        asize = os.path.getsize(apath)
        amd5  = myhash.get_md5(apath)
        asha1 = myhash.get_sha1(apath)
        file_dict.append( (index+1, aid, auid, afile, atime, asize, atext, amd5, asha1) )
    return render_template('upload.html', files=file_dict)

@app.route('/uploaded/<filename>')
# send_from_directory(): Show a [file] in server
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

######################################

#start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)





