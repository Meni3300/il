from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret-key'

USER_DB = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB) as f:
            return json.load(f)
    else:
        return {"admin": {"password": "admin123", "is_admin": True}}


def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['is_admin'] = user.get('is_admin', False)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'], is_admin=session.get('is_admin', False))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        is_admin = 'is_admin' in request.form
        users = load_users()
        if username in users:
            return render_template('add_user.html', error='User already exists')
        users[username] = {'password': password, 'is_admin': is_admin}
        save_users(users)
        return render_template('add_user.html', message='User added successfully')
    return render_template('add_user.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
