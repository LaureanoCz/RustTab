from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.user import User

app = Flask(__name__)

app.config.from_object(config['development'])
app.secret_key = app.config['SECRET_KEY']
db=MySQL(app)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/song/<id>/<cancion>')
def song(id, cancion):
    data = {
        'id': id,
        'cancion': cancion
    }
    return render_template('songs.html')

@app.route("/fav")
def fav():
    return render_template("fav.html")

@app.route("/register")
def register():
    return render_template("auth/register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'], '')
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for("home2"))
            else:
                flash("Usuario o contraseña incorrecta")
                return render_template("auth/login.html")
        else:
            flash("Usuario no encontrado...")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route("/home2")
def home2():
    return render_template("index2.html")
    
if __name__ == "__main__":

    app.run()