from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Upewnij się, że ten klucz jest bezpieczny!

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Many-to-Many relationship table for roles and users (jeśli będzie potrzebna)
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# Model użytkownika – dodana kolumna username
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Dodana kolumna
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    cart_items = db.relationship('Cart', backref='user', lazy=True)

# Model roli
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

# Model produktu
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cart_items = db.relationship('Cart', backref='product', lazy=True)

# Model koszyka
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

# Główna strona – użytkownik zalogowany widzi index.html, w przeciwnym razie następuje przekierowanie na login
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

# Rejestracja – pobiera username, email, password oraz zapisuje użytkownika w bazie
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            # Sprawdzenie, czy email jest już zarejestrowany
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash("Email już zarejestrowany. Proszę się zalogować.")
                return redirect(url_for('signup'))

            # Sprawdzenie, czy nazwa użytkownika jest już zajęta
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                flash("Nazwa użytkownika jest już zajęta.")
                return redirect(url_for('signup'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash("Rejestracja zakończona powodzeniem. Proszę się zalogować!")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Wystąpił błąd: {e}")
            return redirect(url_for('signup'))
    return render_template('signup.html')

# Logowanie – weryfikacja danych, ustawienie sesji i przekierowanie do index
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash("Nieprawidłowy email lub hasło")
        return redirect(url_for('login'))
    return render_template('login.html')

# Wylogowanie – usunięcie danych sesji i przekierowanie na login
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Wylogowano.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabele, jeśli nie istnieją
    app.run(debug=True)




