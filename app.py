from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import random
from flask_migrate import Migrate
import os
from email.mime.base import MIMEBase
from email import encoders
from sqlalchemy.orm import joinedload


# Initialiserer Flask-applikasjonen
app = Flask(__name__)

# Riktig konfigurasjon for database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "database.db")}'
app.config['SECRET_KEY'] = 'Hemmeligpassord'

# Initialiserer databasen
db = SQLAlchemy(app)
# Legg til dette rett etter db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jul123456654@gmail.com'
app.config['MAIL_PASSWORD'] = 'urzg ucei kdzp ftyp'
app.config['MAIL_DEFAULT_SENDER'] = 'jul123456654@gmail.com'
mail = Mail(app)
migrate = Migrate(app, db)
verification_codes = {}

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



# Definer VisitCount-modellen
class VisitCount(db.Model):
    __tablename__ = 'visit_count'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

class Produkt(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    pricetall = db.Column(db.Integer, nullable=False)
    pricetext = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Cart(db.Model):
    __tablename__='cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String, db.ForeignKey('produkt.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Produkt', backref='cart_items')

# Sjekk om 'visit_count'-tabellen finnes, og opprett den hvis ikke
with app.app_context():
    if 'visit_count' not in db.metadata.tables:
        db.create_all()  # Oppretter alle tabeller som ikke finnes




# Definerer en modell for bruker
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)  # E-postadresse
    password = db.Column(db.String(80), nullable=False)
    defeats = db.Column(db.Integer, default=0)


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=6, max=120)], render_kw={"placeholder": "E-post"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Registrer")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("E-posten er allerede i bruk. Velg en annen.")

        
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=6, max=120)], render_kw={"placeholder": "E-post"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")

# Ruter for nettsider
@app.route('/Registrer', methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)  # Bruk e-post her
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template("Registrer.html", form=form)

@app.route('/logginn.html', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Søk etter bruker med e-post
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                code = random.randint(100000, 999999)
                verification_codes[user.email] = code  # Lagre koden i ordboken
                msg = Message("Verifiseringskode", recipients=[user.email])
                msg.body = f"Din verifiseringskode er: {code}"
                mail.send(msg)
                return redirect(url_for('verify', email=user.email))  # Omadresser til verifiseringsrute
    return render_template("logginn.html", form=form)

@app.route('/verifiser/<email>', methods=['GET', 'POST'])
def verify(email):
    if request.method == 'POST':
        code_entered = request.form.get('code')
        if int(code_entered) == verification_codes.get(email):
            user = User.query.filter_by(email=email).first()
            login_user(user)  # Logg inn brukeren hvis koden er riktig
            flash("Velkommen!")
            return redirect(url_for('Loggetinnn'))
        else:
            flash("Feil verifiseringskode, prøv igjen.")
    return render_template('verifiser.html', email=email)

@app.route('/loggetinn', methods=['GET', 'POST'])
@login_required
def Loggetinnn():
    # Hent besøkstelleren fra databasen
    visit_count = VisitCount.query.first()
    
    # Hvis visit_count ikke eksisterer (f.eks. hvis databasen er ny), sett den til 0
    if visit_count:
        count = visit_count.count
    else:
        count = 0  # Hvis ikke opprettet, sett som 0 eller gjør en håndtering her
    visit_count = VisitCount.query.first()
    top_users = User.query.order_by(User.defeats.desc()).limit(10).all()
    return render_template('Loggetinn.html', visit_count=visit_count.count, top_users=top_users)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    return redirect(url_for('login'))
@app.route('/')
def kk():
    return render_template("Index.html")

@app.route('/index.html', methods=['GET', 'POST'])
def H():
    if request.method == 'POST':
        email = request.form.get('nyheter')
        
        if email:
            msg = Message("Våre siste produkter", recipients=[email])
            msg.body = f"Vi har 25% rabatt på rynkefjerner. Gå til http://10.100.10.104:5000 for å få de siste produktene"
            
            image_path = "static/bilder/Rynkefjerner.jpg"  # Bildebane på serveren
            with open(image_path, "rb") as img:
                msg.attach("image.jpg", "image/jpeg", img.read())

            mail.send(msg)
    
    return render_template("Index.html")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = Produkt.query.filter(Produkt.name.ilike(f'%{query}%')).all()
    return render_template('soking.html', results=results)  
            
@app.route('/subscribe_newsletter', methods=['POST'])
def subscribe_newsletter():
    email = request.form.get('nyheter')
    if email:
        msg = Message("Våre siste produkter", recipients=[email])
        msg.body = f"Vi har 25% rabatt på rynkefjerner. Gå til http://10.100.10.104:5000 for å få de siste produktene"
            
        image_path = "static/bilder/Rynkefjerner.jpg"  # Bildebane på serveren
        with open(image_path, "rb") as img:
            msg.attach("image.jpg", "image/jpeg", img.read())

        mail.send(msg)
    
    return redirect(request.referrer)  # Gå tilbake til siden brukeren kom fra

    
    

@app.route('/prudukt.html', methods=['GET', 'POST'])
def hent_produkter():
    product_id = request.args.get('id')  # Henter ID fra spørringsparameter
    produkt = Produkt.query.get(product_id)  # Henter produktet med den spesifikke ID-en
    if produkt is None:
        return "Produkt ikke funnet", 404  # Returner 404 hvis produktet ikke finnes
    
    if request.method == 'POST':
        email = request.form.get('nyheter')
        
        if email:
            msg = Message("Våre siste produkter", recipients=[email])
            msg.body = f"Vi har 25% rabatt på rynkefjerner. Gå til http://10.100.10.104:5000 for å få de siste produktene"
            
            image_path = "static/bilder/Rynkefjerner.jpg"  # Bildebane på serveren
            with open(image_path, "rb") as img:
                msg.attach("image.jpg", "image/jpeg", img.read())

            mail.send(msg)
    return render_template('prudukt.html', produkt=produkt)

@app.route('/detalj.html')
def Detaljer():
    return render_template("detalj.html")

@app.route('/Handlekurv.html')
def Handlekurv():
    cart_items = []

    if current_user.is_authenticated:
        # Hent handlekurvdata fra databasen for innloggede brukere
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    else:
        # Hent handlekurvdata fra session for anonyme brukere
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                produkt = Produkt.query.get(product_id)
                if produkt:
                    cart_items.append({
                        'product': produkt,
                        'quantity': quantity
                    })

    return render_template('Handlekurv.html', cart_items=cart_items)

from flask import session, redirect, url_for, flash
from flask_login import current_user

@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    produkt = Produkt.query.get(product_id)
    if produkt is None:
        return "Produkt ikke funnet", 404

    if current_user.is_authenticated:
        # Håndterer innloggede brukere
        cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            # Hvis produktet allerede finnes, øk antallet
            cart_item.quantity += 1
        else:
            # Hvis ikke, opprett et nytt handlekurv-element
            cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
            db.session.add(cart_item)
        db.session.commit()
        flash("Produktet ble lagt til i handlekurven!")
    else:
        # Håndterer anonyme brukere med session
        if 'cart' not in session:
            session['cart'] = {}

        if product_id in session['cart']:
            session['cart'][product_id] += 1  # Øk antallet
        else:
            session['cart'][product_id] = 1  # Legg til produktet

        session.modified = True  # Marker session som endret
        flash("Produktet ble lagt til i handlekurven (anonym)!")

    return redirect(url_for('Handlekurv'))  # Omdiriger til ønsket side

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Produktet ble fjernet fra handlekurven!")
    else:
        flash("Produktet finnes ikke i handlekurven.")
    return redirect(url_for('Handlekurv'))  # Omdiriger til handlekurvvisning

@app.route('/kvitering.html', methods=['POST'])
def kvitering():
    kviteringting = Cart.query.options(joinedload(Cart.product)).filter_by(user_id=current_user.id).all()
    
    for item in kviteringting:
        db.session.delete(item)
    db.session.commit()
    
    return render_template('kvitering.html', kviteringting=kviteringting)

@app.route('/glemt_passord', methods=['GET', 'POST'])
def glemt_passord():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generer en tilbakestillingskode
            reset_code = random.randint(100000, 999999)
            verification_codes[email] = reset_code  # Lagrer koden midlertidig
            
            msg = Message("Tilbakestilling av passord", recipients=[user.email])
            msg.body = f"Din tilbakestillingskode er: {reset_code}. Gå til /tilbakestill_passord/{email} for å tilbakestille passordet."
            mail.send(msg)
            flash("Tilbakestillingskode sendt til e-post.")
            
            # Omdirigerer direkte til tilbakestillingskode-siden
            return redirect(url_for('tilbakestill_passord', email=email))
        else:
            flash("Ingen bruker med denne e-posten.")
    
    return render_template('glemt_passord.html')

@app.route('/tilbakestill_passord/<email>', methods=['GET', 'POST'])
def tilbakestill_passord(email):
    if request.method == 'POST':
        code_entered = request.form.get('code')
        new_password = request.form.get('new_password')

        if int(code_entered) == verification_codes.get(email):
            user = User.query.filter_by(email=email).first()
            if user:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')  # Husk å dekode hashen
                user.password = hashed_password
                db.session.commit()
                flash("Passordet er tilbakestilt!")
                return redirect(url_for('login'))
            else:
                flash("Ingen bruker med denne e-posten.")
        else:
            flash("Feil tilbakestillingskode, prøv igjen.")

    return render_template('tilbakestill_passord.html', email=email)
@app.route('/Spill')
@login_required
def spill():
    # Hent besøkstelleren fra databasen, eller opprett en ny rad hvis den ikke finnes
    visit_count = VisitCount.query.first()


    # Hvis ingen besøksteller finnes, opprett en
    if not visit_count:
        visit_count = VisitCount(count=0)
        db.session.add(visit_count)
        db.session.commit()

    # Sjekk om brukeren allerede har talt et besøk i denne sesjonen
    if 'has_counted' not in session:
        # Øk antall besøk og lagre det
        visit_count.count += 1
        db.session.commit()  # Commit after making changes

        # Sett sesjonsvariabel for å forhindre flere tellinger
        session['has_counted'] = True

    # Returner Spill.html og send med `visit_count`
    return render_template('Spill.html', visit_count=visit_count.count)

@app.route('/update_defeats', methods=['POST'])
@login_required
def update_defeats():
    try:
        # Initialiser defeats til 0 hvis den er None
        if current_user.defeats is None:
            current_user.defeats = 0
        
        current_user.defeats += 1
        db.session.commit()
        print(f"Defeats updated for user {current_user.email}. New value: {current_user.defeats}")
        return jsonify({"success": True, "new_defeats": current_user.defeats}), 200
    except Exception as e:
        print(f"Error updating defeats: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

   
if __name__ == '__main__':
    app.run(debug=True)
