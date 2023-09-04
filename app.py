from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    farm_name = db.Column(db.String(200), nullable=True)
    farm_size = db.Column(db.Float, nullable=True)
    farm_location = db.Column(db.String(500), nullable=True)
    crops_grown = db.Column(db.String(500), nullable=True)
    livestock_details = db.Column(db.String(500), nullable=True)
    


@app.route('/')
def home():
    return render_template('index.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']
        address = request.form['address']
        farm_name = request.form['farm_name']
        farm_size = float(request.form['farm_size'])
        farm_location = request.form['farm_location']
        crops_grown = request.form['crops_grown']
        livestock_details = request.form['livestock_details']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(
            full_name=full_name, 
            email=email,
            password=hashed_password,  # Hash the password before saving in a real app!
            phone_number=phone_number, 
            address=address, 
            farm_name=farm_name, 
            farm_size=farm_size, 
            farm_location=farm_location, 
            crops_grown=crops_grown, 
            livestock_details=livestock_details
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return "User registered successfully!"
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint failed: user.email' in str(e):
                return "Email already registered. Please use a different email."
            else:
                return "An error occurred. Please try again."

        return redirect(url_for('home'))  # Redirect user back to the home page after signing up.

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']


        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=email).first()
        print(user)
        print(password)
        print(user.password)
        # The function check_password_hash() verifies the password.
        if user.password and password:
            return redirect(url_for('home'))  # or some other page, like a dashboard
        else:
            return "Invalid email or password. Please try again.", 400  # HTTP 400 Bad Request

    return render_template('signin.html')

import requests

from flask import request

@app.route('/daily_forecast', methods=['GET', 'POST'])
def daily_forecast():
    # Your OpenWeatherMap API Key
    API_KEY = 'ce2720ce5d5521bb14c99bb16dda0201'
    
    # Default city
    CITY_NAME = "New York"
    
    # If form is submitted, update the CITY_NAME
    if request.method == 'POST':
        CITY_NAME = request.form.get('city', CITY_NAME)
    
    BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=imperial"

    # Making a GET request to fetch the raw weather data
    try:
        weather_data = requests.get(BASE_URL).json()
        forecast_data = {
            "location": CITY_NAME,
            "forecast": weather_data["weather"][0]["description"],
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
        }
    except Exception as e:
        print("Error:", e)
        forecast_data = {
            "location": "Error",
            "forecast": "Unable to fetch weather data at the moment."
        }

    return render_template('daily_forecast.html', forecast=forecast_data)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables.
    app.run(host='0.0.0.0',port=8000, debug=True)

