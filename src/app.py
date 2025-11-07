from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
import re

from config import config

# Models
from models.ModelUser import ModelUser
from models.ModelSong import ModelSong

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
    try:
        # Try to get song by ID first
        song_data = ModelSong.get_by_id(db, id)
        
        # If not found by ID, try by slug/name
        if not song_data:
            song_data = ModelSong.get_by_slug(db, cancion)
        
        if song_data:
            # Parse tablatura data if it exists
            tablatura_data = ModelSong.parse_tablatura_data(song_data.tablatura_data)
            
            return render_template('songs.html', 
                                 song=song_data,
                                 tablatura_data=tablatura_data)
        else:
            flash("Canción no encontrada")
            return redirect(url_for('home'))
    except Exception as ex:
        flash(f"Error al cargar la canción: {str(ex)}")
        return redirect(url_for('home'))

@app.route("/api/search")
def search_songs():
    """API endpoint for searching songs"""
    try:
        query = request.args.get('q', '').strip()
        
        # If query is empty, return all songs
        if not query or len(query) < 1:
            results = ModelSong.get_all_songs(db, limit=100)
        else:
            results = ModelSong.search_songs(db, query, limit=10)
        
        return jsonify({'songs': results})
    except Exception as ex:
        return jsonify({'error': str(ex), 'songs': []}), 500

@app.route("/fav")
def fav():
    return render_template("fav.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation: Check required fields
        if not username:
            flash("El nombre de usuario es requerido")
            return render_template("auth/register.html")
        
        if not email:
            flash("El correo electrónico es requerido")
            return render_template("auth/register.html")
        
        if not password:
            flash("La contraseña es requerida")
            return render_template("auth/register.html")
        
        # Validation: Email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash("El formato del correo electrónico no es válido")
            return render_template("auth/register.html")
        
        # Validation: Password minimum length
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres")
            return render_template("auth/register.html")
        
        try:
            # Check if user already exists
            if ModelUser.user_exists(db, username=username):
                flash("El nombre de usuario ya está en uso")
                return render_template("auth/register.html")
            
            if ModelUser.user_exists(db, email=email):
                flash("El correo electrónico ya está registrado")
                return render_template("auth/register.html")
            
            # Create new user
            ModelUser.create_user(db, username, email, password)
            return redirect(url_for("login") + "?registered=success")
            
        except Exception as ex:
            flash(f"Error al registrar usuario: {str(ex)}")
            return render_template("auth/register.html")
    else:
        return render_template("auth/register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'], '')
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            login_user(logged_user)
            return redirect(url_for("home") + "?login=success")
        else:
            flash("Usuario o contraseña incorrecta")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()  # Clear Flask session
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        # AJAX request - return JSON response
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    # Fallback for non-AJAX requests
    return redirect(url_for("home"))

def status_401(error):
    return redirect(url_for("login"))

@app.route("/home2")
def home2():
    return render_template("index2.html")
    
if __name__ == "__main__":
    app.register_error_handler(401, status_401)
    app.run()