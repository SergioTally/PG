from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow 
from numpy import array
from keras.models import load_model 
import os

#Direccion de la Base de datos
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

#Caracteristicas Base de datos
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Diagramacion BD
class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), unique=True, nullable=False)
    Observacion = db.Column(db.String(80))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    Cargo_id = db.Column(db.Integer, nullable=False)

class Trabajador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), unique=True, nullable=False)
    DPI = db.Column(db.String(20))
    InicioLaboral = db.Column(db.String(20))

class Credito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Monto = db.Column(db.String(50), unique=True, nullable=False)
    Plazo = db.Column(db.String(20))
    FechaEntrega = db.Column(db.String(20))
    Trabajador_id = db.Column(db.Integer)
    User_id = db.Column(db.Integer)

class Estimacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Resultado = db.Column(db.String(50), unique=True, nullable=False)
    Credito_id = db.Column(db.Integer, nullable=False)

class Incumplimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Fecha = db.Column(db.String(50), unique=True, nullable=False)
    Mora = db.Column(db.String(80))
    Credito_id = db.Column(db.Integer, nullable=False)

# Product Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'Nombre', 'password', 'Cargo_id')

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Creating simple Routes 
@app.route('/test')
def test():
    return "Home Page"

@app.route('/test/about/')
def about_test():
    return "About Page"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = User(Nombre=request.form["username"], password=hashed_pw, Cargo_id="1")
        db.session.add(new_user)
        db.session.commit()

        return "You've registered successfully."

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(Nombre=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            return render_template("home.html")
        return "Your credentials are invalid, check and try again."

    return render_template("login.html")

# Routes to Render Something
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about', strict_slashes=False)
def about():
    return render_template("about.html")

@app.route("/usuarios")
def search():
    X="2"
    #Px = array([[2,2.89337,2,1]])

#model2=load_model('ModeloCredit')

#Prueba=model2.predict(Px)
    return X

# Make sure this we are executing this file
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
