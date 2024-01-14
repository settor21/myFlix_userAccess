from pymongo import MongoClient
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import requests, uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_SERVICE_URL = 'http://127.0.0.1:6000'


# Initialize MongoDB client
mongo_client = MongoClient(
    'mongodb+srv://amedikusettor:Skaq0084@myflixproject.soxjrzv.mongodb.net/?retryWrites=true&w=majority')
db = mongo_client['userSubscriptions']
subscription_collection = db['subscriptionInit']

# Function to check if a user with given email and password exists in db
def authenticate_user(email, password):
    data = {'email': email, 'password': password}
    response = requests.post(f'{DB_SERVICE_URL}/authenticate', json=data)
    return response.json().get('user')

# Function to add a new user to the database
def add_user(first_name, last_name, email, password):
    data = {'first_name': first_name, 'last_name': last_name,
            'email': email, 'password': password}
    response = requests.post(f'{DB_SERVICE_URL}/add_user', json=data)
    return response

# Function to get user_id based on first name, last name, and email
def get_user_id(first_name, last_name, email):
    data = {'first_name': first_name, 'last_name': last_name, 'email': email}
    response = requests.post(f'{DB_SERVICE_URL}/get_user_id', json=data)
    return response.json().get('user_id', None)


# Function to generate a random session ID
def generate_session_id():
    return str(uuid.uuid4())

# Function to add a new session to the sessions table
def add_session(user_id, session_id):
    data = {'user_id': user_id, 'session_id': session_id}
    requests.post(f'{DB_SERVICE_URL}/add_session', json=data)
    
    
# Function to subscribe the user based on the chosen tier
def subscribe(user_id, subscription_choice):
    if subscription_choice == 'ad-tier':
        # For Ad-tier, set paidSubscriber to NO and amount to 0
        data = {'userId': user_id, 'paidSubscriber': 'NO', 'amount': 0}
        requests.post(f'{DB_SERVICE_URL}/add_subscription', json=data)
        # Redirect to login page after successful signup for ad-tier
        return redirect(url_for('login'))

    elif subscription_choice == 'paid-tier':
        # For Paid-tier, set paidSubscriber to YES and amount to 5, and store in MongoDB
        data = {'userId': user_id, 'paidSubscriber': 'PENDING',
                'amount': 5, 'timestamp': datetime.now()}
        subscription_collection.insert_one(data)
        
        # Send a POST request to /subscribe with the user_id in the JSON payload
        requests.post('http://127.0.0.1:5002/subscribe', json={'user_id': user_id})
        # Redirect to subscribe page after successful signup for paid-tier
        return redirect('http://127.0.0.1:5002/subscribe')

    else:
        return jsonify({'error': 'Invalid subscription choice'})


#load homepage
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
            
            # Redirect to the home page
            return redirect('http://127.0.0.1:5001/home')

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
        new_user = add_user(first_name, last_name, email, password)
        
        if new_user != None:
            # Get user_id after adding the user
            user_id = get_user_id(first_name, last_name, email)

            # Subscribe the user based on the chosen tier
            subscription_choice = request.form.get('subscription')
            print(subscription_choice)
            # subscribe(user_id, subscription_choice)
            if subscription_choice == 'ad-tier':
                # For Ad-tier, set paidSubscriber to NO and amount to 0
                data = {'userId': user_id, 'paidSubscriber': 'NO', 'amount': 0}
                requests.post(f'{DB_SERVICE_URL}/add_subscription', json=data)
                # Redirect to login page after successful signup for ad-tier
                return redirect(url_for('login'))

            elif subscription_choice == 'paid-tier':
                # For Paid-tier, set paidSubscriber to YES and amount to 5, and store in MongoDB
                data = {'userId': user_id, 'paidSubscriber': 'PENDING',
                        'amount': 5, 'timestamp': datetime.now()}
                subscription_collection.insert_one(data)
                
                # Send a POST request to /subscribe with the user_id in the JSON payload
                requests.post('http://127.0.0.1:5002/subscribe', json={'user_id': user_id})
                # Redirect to subscribe page after successful signup for paid-tier
                return redirect('http://127.0.0.1:5002/subscribe')

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host = "0.0.0.0",debug=False,port= 5000) #will listen to all ports on production
