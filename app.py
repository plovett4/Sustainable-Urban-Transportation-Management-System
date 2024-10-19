from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
import MySQLdb.cursors
import secrets
import re
 
 
app = Flask(__name__)
bcrypt = Bcrypt(app)
  

salty_splatoon = secrets.token_hex(16) # Generates 16-byte random salt
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

# Change following info based on local DB for right now, until web-based DB is implemented
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = '0x45'
app.config['MYSQL_PASSWORD'] = 'Ka1iB1tch!!!69421mysql'
app.config['MYSQL_DB'] = 'TrafficBoss_Login'
 

mysql = MySQL(app)
 

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        user_to_check = cursor.fetchone()

        if user_to_check:
            stored_hash = user_to_check['password']
            salt = user_to_check['salt']

            if check_password_hash(stored_hash, password + salt):
                session['loggedin'] = True
                session['id'] = user_to_check['id']
                session['username'] = user_to_check['username']
                msg = 'Logged in successfully !'
                return render_template('index.html', msg = msg)
            else:
                msg = 'Incorrect username / password !'
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 

@app.route('/register', methods =['GET', 'POST'])
def register():

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_pw = generate_password_hash(password + salty_splatoon)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists !'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'

        elif not username or not password or not email:
            msg = 'Please fill out the form !'

        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)', (username, hashed_pw, salty_splatoon, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server
    app.run()
