# -*- coding: utf-8 -*-
import os
import datetime
from werkzeug import secure_filename
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory

# import model
import myhash


#configuration
DATABASE = '/tmp/blog.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD ='default'
UPLOAD_FOLDER = '/home/playcrab/lab/blog_stable/blog/files'

#database utils
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

#create application
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

@app.route('/')
def homepage():
    g.db = connect_db()
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('homepage.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method ==  'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('homepage'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('homepage'))

#@app.route('/profile/<int:user_id>')
#def profile():
#    
@app.route('/video')
def show_video():
    return render_template('show_video.html')

@app.route('/music')
def set_music():
    return render_template('set_music.html')


ALLOWED_EXT = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'ogg', 'mp4', 'bmp', 'ico'])
def check_filename(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1] in ALLOWED_EXT)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file'] # use [files] dictionary on the request object
        if file and check_filename(file.filename):
            filename = secure_filename(file.filename) # secure_filename(): Strip filename To ASCII string
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # save(): save file permanently
            return redirect(url_for('uploaded_file', filename=filename)) # Uploaded Successfully, Redirect to [uploaded_file]
    # Upload Failed
    file_dict = []
    index = 1
    for afile in os.listdir(app.config['UPLOAD_FOLDER']):
        apath = os.path.join(app.config['UPLOAD_FOLDER'], afile)
        atime = os.path.getmtime(apath)
        adate = (datetime.datetime.fromtimestamp(atime)).strftime('%Y-%m-%d %H:%M:%S')
        asize = os.path.getsize(apath)
        amd5  = myhash.get_md5(apath)
        asha1 = myhash.get_sha1(apath)
        file_dict.append( (adate, index, afile, asize, amd5, asha1) )
        index = index + 1

    files = sorted(file_dict) 
    return render_template('upload_file.html', files=files)

@app.route('/uploaded/<filename>')
# send_from_directory(): Show a [file] in server
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

######################################

#start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)





