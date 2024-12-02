from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photostudio.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    service = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    recent_images = [
        {'title': 'Summer Wedding', 'path': 'wedding1.jpg'},
        {'title': 'Sunset Portrait', 'path': 'portrait1.jpg'},
        {'title': 'Corporate Event', 'path': 'event1.jpg'}
    ]
    return render_template('home.html', recent_images=recent_images)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    portfolio_images = [
        {'title': 'Beach Wedding', 'filename': 'wedding1.jpg', 'category': 'wedding'},
        {'title': 'Corporate Team', 'filename': 'corporate1.jpg', 'category': 'event'},
        {'title': 'Family Portrait', 'filename': 'portrait1.jpg', 'category': 'portrait'},
        # Add more images
    ]
    return render_template('portfolio.html', portfolio_images=portfolio_images)


@app.route('/pricing')
def pricing():
    packages = [
        {
            'name': 'Basic Package',
            'price': '$299',
            'features': [
                '2 Hours Shoot',
                '50 Edited Photos',
                'Online Gallery',
                'Digital Download'
            ]
        },
        {
            'name': 'Premium Package',
            'price': '$599',
            'features': [
                '4 Hours Shoot',
                '100 Edited Photos',
                'Album Printing',
                'Online Gallery',
                'Second Photographer',
                'Engagement Session'
            ]
        },
        {
            'name': 'Deluxe Package',
            'price': '$999',
            'features': [
                'Full Day Coverage',
                '200 Edited Photos',
                'Luxury Album',
                'Online Gallery',
                'Two Photographers',
                'Video Highlights',
                'Engagement Shoot',
                'Drone Footage'
            ]
        }
    ]
    return render_template('pricing.html', packages=packages)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Add logic to send email or store message
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # Process booking form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        service = request.form['service']
        
        new_booking = Booking(
            name=name, 
            email=email, 
            phone=phone, 
            date=date, 
            service=service
        )
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Booking submitted successfully!', 'success')
        return redirect(url_for('booking'))
    return render_template('booking.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)