from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure database (SQLite for now)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Many-to-Many relationship table for roles and users
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# Create User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

# Create Role model
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

# Create Products table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Create Cart table
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

@app.route('/')
def home():
     return render_template('home.html')

from werkzeug.security import generate_password_hash
from flask import redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Sign Up Route
from werkzeug.security import generate_password_hash
from flask import render_template, request, redirect, url_for

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered. Please log in."

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user and add to the session
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()  # Commit the transaction to save to the database

        # After signing up, redirect to the login page
        return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Logs the user out
    return redirect(url_for('home'))  # Redirects back to home page


from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Log the user in (store in session)
            return redirect(url_for('home'))  # Redirect to home page

        return "Invalid email or password"  # Invalid login message

    return render_template('login.html')

@app.route('/products')
def products():
    return render_template('products.html')  # You will create a products page template next

# Just a quick way to check the data in the User table
@app.route('/check_users')
def check_users():
    users = User.query.all()  # Retrieve all users from the database
    users_list = [user.email for user in users]  # Get a list of emails
    return f"Users in the database: {', '.join(users_list)}"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates database and tables if not exist
    app.run(debug=True)
