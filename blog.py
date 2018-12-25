from flask import Flask, render_template, request, session, \
flash, redirect, url_for, g
from functools import wraps # used to create python decorators
import sqlite3

# flask config variables
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'qfKWWbF7nQyHczXdugfzvdNy'

# instantiate flask app
app = Flask(__name__)

# passing config varibales to app
app.config.from_object(__name__)

# method that returns sql connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# decorator method to ensure user is logged in
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to log in first.")
            return redirect(url_for('login'))
    return wrap

# root authentication page. takes you to main if login succcessful.
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code

# main page. displays blog posts by querying sql
@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute("SELECT * FROM posts")
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

# logout page/button
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

# posting page/button
@app.route('/add', methods=["POST"])
@login_required
def add():
    # get user data input from html form
    title = request.form['title']
    post = request.form['post']
    # check if title and post is filled in. if not reload page
    if not title or not post:
        flash("Title and post fields are required. Please try again.")
        return redirect(url_for('main'))
    # insert title and post into sql
    else:
        g.db = connect_db()
        g.db.execute("INSERT INTO posts (title, post) VALUES(?,?)", 
        [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted")
        return redirect(url_for('main'))

# run app / debug on
if __name__ == '__main__':
    app.run(debug=True)