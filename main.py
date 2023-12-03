from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_caching import Cache 
from datetime import timedelta


app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = '93422'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
cache = Cache(app)
app.permanent_session_lifetime = timedelta(days=30)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    goal = db.Column(db.String(20))
    preferences = db.relationship('Preference', backref='user', lazy=True)
    #allergy=db.relationship('Allergy', backref='user', lazy=True)

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    preference_name = db.Column(db.String(50))

class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    allergy_name = db.Column(db.String(50))




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('start1.html')
@app.route('/start2')
def index1():
    return render_template('start2.html')  

@app.route('/allergy', methods=['GET', 'POST'])
@login_required
def allergy():
    if request.method == 'POST':
        selected_allergies = request.form.getlist('allergy')
        current_user.allergies = []  # Измените 'allergy' на 'allergies'

        for allergy_name in selected_allergies:
            allergy = Allergy.query.filter_by(user_id=current_user.id, allergy_name=allergy_name).first()
            if not allergy:
                allergy = Allergy(user_id=current_user.id, allergy_name=allergy_name)
                db.session.add(allergy)
            current_user.allergies.append(allergy)  # Измените 'allergy' на 'allergies'

        db.session.commit()
        flash('Allergies saved.', 'success')
        return redirect(url_for('main'))


    return render_template('allergy.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        
        if not username or not password or not email:
            flash('Both username and password are required!', 'error')
            return redirect(url_for('register'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password,email = email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('userinfo'))
    
    return render_template('register.html')

@app.route('/indpref', methods=['GET', 'POST'])
def indpref():
    if request.method == 'POST':
        selected_preferences = request.form.getlist('preferences')
        current_user.preferences = []

        for preference_name in selected_preferences:
            preference = Preference.query.filter_by(user_id=current_user.id, preference_name=preference_name).first()
            if not preference:
                preference = Preference(user_id=current_user.id, preference_name=preference_name)
                db.session.add(preference)
            current_user.preferences.append(preference)

        db.session.commit()
        flash('Preferences saved.', 'success')
        return redirect(url_for('choose'))

    return render_template('indpref.html')
   

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    return render_template('choose.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Login failed. Check your username and password.', 'error')
    
    return render_template('login.html')


    
@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if request.method == 'POST':
        current_user.gender = request.form.get('gender')
        current_user.weight = float(request.form.get('weight'))
        current_user.height = float(request.form.get('height'))
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.age = int(request.form.get('age'))
        current_user.goal = request.form.get('goal')
        db.session.commit()
        flash('User information saved.', 'success')
        return redirect(url_for('indpref'))
    
    return render_template('userinfo.html')
@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/calendar')

def calendar():
    return render_template('calendar.html')
@app.route('/products')
def products():
    return render_template('products.html')
@app.route('/etc')
def etc():
    return render_template('etc.html')



if __name__ == '__main__':
    app.run(debug=True)
