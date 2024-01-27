from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_wtf.csrf import CSRFProtect
import requests
from datetime import datetime
import uuid
import psycopg2
from bcrypt import hashpw, gensalt

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your_secret_key'


# PostgreSQL Configuration
DB_HOST = 'xxxxxx'  # Replace with the IP address of your GCP VM
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'xxxxxx'
DB_NAME = 'users'


def create_tables():
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscriptionId SERIAL PRIMARY KEY,
                userId INTEGER,
                paidSubscriber TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (userId) REFERENCES users (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                session_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        connection.commit()


# Function to check if a user with given email and password exists in db
def authenticate_user(email, password):
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email=%s', (email,))
        user = cursor.fetchone()

        if user and hashpw(password.encode('utf-8'), user[4].encode('utf-8')) == user[4].encode('utf-8'):
            # Passwords match
            return user
        else:
            # Invalid credentials
            return None


# Function to add a new user to the database
def add_user(first_name, last_name, email, password):
    # Hash the password before storing it
    hashed_password = hashpw(password.encode(
        'utf-8'), gensalt()).decode('utf-8')

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
            (first_name, last_name, email, hashed_password)
        )
        connection.commit()


# Function to get user_id based on first name, last name, and email
def get_user_id(first_name, last_name, email):
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id FROM users
            WHERE first_name = %s AND last_name = %s AND email = %s
        ''', (first_name, last_name, email))

        user_id = cursor.fetchone()

    return user_id[0] if user_id else None


# Function to generate a random session ID
def generate_session_id():
    return str(uuid.uuid4())


# Function to add a new session to the sessions table
def add_session(user_id, session_id):
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO sessions (user_id, session_id) VALUES (%s, %s)',
            (user_id, session_id)
        )
        connection.commit()


# Function to subscribe the user based on the chosen tier
def subscribe(user_id, subscription_choice):
    if subscription_choice == 'ad-tier':
        # For Ad-tier, set paidSubscriber to NO and amount to 0
        with psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO subscriptions (userId, paidSubscriber, amount) VALUES (%s, %s, %s)',
                (user_id, 'NO', 0)
            )
            connection.commit()
        # Redirect to login page after successful signup for ad-tier
        return "login"

    elif subscription_choice == 'paid-tier':
        # For Paid-tier, set paidSubscriber to YES and amount to 5
        with psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO subscriptions (userId, paidSubscriber, amount) VALUES (%s, %s, %s)',
                (user_id, 'PENDING', 5)
            )
            connection.commit()
        # Redirect to subscribe page after successful signup for paid-tier
        return "subscribe"

    else:
        return jsonify({'error': 'Invalid subscription choice'})


def get_user_tier(user_id):
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    ) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT paidSubscriber FROM subscriptions
            WHERE userId = %s
        ''', (user_id,))

        user_tier = cursor.fetchone()

    return user_tier[0] if user_tier else None


# Load homepage
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = authenticate_user(email, password)

        if user:
            # Generate a session ID and add the session to the sessions table
            session_id = generate_session_id()
            add_session(user[0], session_id)
            session['session_id'] = session_id

            # Tier check: Get the user's tier from the subscriptions table
            user_id = user[0]
            user_tier = get_user_tier(user_id)

            if user_tier == 'paid-tier':
                # Redirect to the appropriate page for paid-tier users
                return redirect('https://myflix.world/paid-tier')
            else:
                # Redirect to ad-tier for non-paid-tier users
                return redirect('https://myflix.world/ad-tier')

        return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password and confirm_password match on the client side
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        # Add user to the database without assignment
        add_user(first_name, last_name, email, password)

        # Get user_id after adding the user
        user_id = get_user_id(first_name, last_name, email)

        # Subscribe the user based on the chosen tier
        subscription_choice = request.form.get('subscription')
        # print(subscription_choice)
        choice = subscribe(user_id, subscription_choice)
        if choice == "subscribe":
            return redirect ('https//myflix.world/subscribe')
        else:
            return render_template("login.html")    

    return render_template('signup.html')


if __name__ == '__main__':
    create_tables()  # creates table first
    # will listen to all ports on production
    app.run(host="0.0.0.0", debug=True, port=5000)
