from flask import Flask, render_template, request, redirect, url_for, flash
from config import config
from flask_mysqldb import MySQL
import cx_Oracle
from config import config

# models:
from models.modeluser import ModelUser

# entities:
from models.entities.user import User

app = Flask(__name__)
db = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       user = User(0, request.form['username'], request.form['password'])
       logged_user = ModelUser.login(db, user)
       if logged_user != None:
            if logged_user.password:
               return redirect(url_for('home'))
            else:
               flash("Contraseña incorrecta") # requiere secret key
               return render_template('auth/login.html')
       else:
            flash("Usuario no encontrado") # requiere secret key
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/")
def index():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
