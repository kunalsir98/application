from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            mysql.connection.commit()
            cur.close()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user[3], password):  # user[3] is the hashed password
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials!', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('login.html')

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()

        # Handle task creation
        if request.method == 'POST':
            task = request.form['task']
            cur.execute("INSERT INTO tasks (user_id, task, status) VALUES (%s, %s, %s)", (session['user_id'], task, 'Pending'))
            mysql.connection.commit()

        # Fetch tasks
        cur.execute("SELECT * FROM tasks WHERE user_id = %s", (session['user_id'],))
        tasks = cur.fetchall()
        cur.close()

        return render_template('dashboard.html', tasks=tasks)
    except Exception as e:
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('login'))

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects")

@app.route('/resources')
def resources():
    return render_template('resources.html', title="Resources")


# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have logged out.', 'info')
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
