from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello My World!'

@app.route('/test')
def hello():
    return 'Test Page'

@app.route('/user/<user_name>')
def show_user(user_name):
    return 'UserName = "%s"' % user_name

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'PostID = "%d"' % post_id


if __name__ == '__main__':
    app.run(host='0.0.0.0')

