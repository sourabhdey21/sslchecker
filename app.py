from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from models import db, User, SSLCheck

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ssl_checker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'dea6eeebf1mshb3d907739bceaeap12fcb0jsnba726620ee8e')
RAPIDAPI_HOST = "check-ssl.p.rapidapi.com"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/check_ssl', methods=['POST'])
@login_required
def check_ssl():
    domain = request.form.get('domain', '')
    
    # Remove http:// or https:// if present
    domain = domain.replace('http://', '').replace('https://', '')
    
    url = f"https://check-ssl.p.rapidapi.com/sslcheck"
    
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    
    params = {
        'domain': f'https://{domain}'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if not data.get('error', True):
            # Store the check in database
            check = SSLCheck(
                domain=domain,
                is_valid=data.get('isvalidCertificate', False),
                expiry_date=datetime.strptime(data.get('expiry', ''), '%Y-%m-%d') if data.get('expiry') else None,
                issuer=data.get('issuer', ''),
                user_id=current_user.id
            )
            db.session.add(check)
            db.session.commit()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)})

@app.route('/history')
@login_required
def history():
    checks = SSLCheck.query.filter_by(user_id=current_user.id).order_by(SSLCheck.check_date.desc()).all()
    return jsonify([check.to_dict() for check in checks])

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0') 