from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import re

import os
import json
import MySQLdb.cursors

from config import config

# Models
from models.ModelUser import ModelUser
from models.ModelSong import ModelSong
from models.ModelFavorite import ModelFavorite

# Entities
from models.entities.user import User

app = Flask(__name__)

app.config.from_object(config['development'])
app.secret_key = app.config['SECRET_KEY']
db = MySQL(app)
db.cursorclass = MySQLdb.cursors.DictCursor

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)




# Ruta de HOME - renderiza index.html
@app.route("/home")
def home():
    return render_template("index.html")






# Ruta de canciones favoritas
@app.route('/favoritos')
def favoritos():
    try:
        if not current_user or not current_user.is_authenticated:
            return render_template('fav.html', favorites=[], open_login_modal=True)

        cursor = db.connection.cursor()
        sql = """
            SELECT s.id, s.title, s.artist
            FROM favorites f
            JOIN songs s ON f.song_id = s.id
            WHERE f.user_id = %s
            ORDER BY f.created_at DESC
        """
        cursor.execute(sql, (current_user.id,))
        rows = cursor.fetchall()
        favorites = []
        for r in rows:
            if isinstance(r, dict):
                favorites.append({'id': r.get('id'), 'title': r.get('title'), 'artist': r.get('artist')})
            else:
                favorites.append({'id': r[0], 'title': r[1], 'artist': r[2]})

        return render_template('fav.html', favorites=favorites, open_login_modal=False)
    except Exception as ex:
        return render_template('fav.html', favorites=[], open_login_modal=(not current_user.is_authenticated if current_user else True))






# Ruta dinámica que obtiene los datos de una canción del archivo JSON correspondiente
@app.route("/song/<title>")
def song(title):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM songs WHERE LOWER(title) = LOWER(%s)", (title,))
    song = cursor.fetchone()

    if not song:
        return ('Song not found', 404)

    json_path = os.path.join("static", "tablatures", song["json_file"])

    with open(json_path, "r", encoding="utf-8") as f:
        tab_data = json.load(f)

    # `tab_data` es un diccionario Python con la tablatura (parsed JSON).
    # La plantilla debe inyectar este objeto en la página (p. ej. como
    # variable JavaScript `TAB_DATA`) para que `static/js/render.js`
    # pueda transformar la estructura JSON en objetos de Vex.Flow y
    # renderizar la tablatura en el cliente.

    is_favorite = False
    try:
        if current_user and current_user.is_authenticated:
            try:
                is_favorite = ModelFavorite.is_favorite(db, current_user.id, song['id'])
            except Exception:
                is_favorite = False
    except Exception:
        is_favorite = False

    return render_template("songs.html", song=song, tab_data=tab_data, json_file=song["json_file"], is_favorite=is_favorite)


@app.route('/toggle_favorite/<int:song_id>', methods=['POST'])
def toggle_favorite(song_id):
    try:
        if not current_user or not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401

        user_id = current_user.id
        if ModelFavorite.is_favorite(db, user_id, song_id):
            ModelFavorite.remove_favorite(db, user_id, song_id)
            return jsonify({'favorite': False})
        else:
            ModelFavorite.add_favorite(db, user_id, song_id)
            return jsonify({'favorite': True})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@app.route("/api/search")
def search_songs():
    """API endpoint for searching songs"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 1:
            results = ModelSong.get_all_songs(db, limit=100)
        else:
            results = ModelSong.search_songs(db, query, limit=10)
        
        return jsonify({'songs': results})
    except Exception as ex:
        return jsonify({'error': str(ex), 'songs': []}), 500



# Ruta de REGISTER - gestiona el registro de nuevos usuarios
# Valida los datos del formulario, verifica que no existan usuarios con el mismo username o email
# y crea el nuevo usuario si todo es correcto
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username:
            flash("El nombre de usuario es requerido")
            return render_template("auth/register.html")
        
        if not email:
            flash("El correo electrónico es requerido")
            return render_template("auth/register.html")
        
        if not password:
            flash("La contraseña es requerida")
            return render_template("auth/register.html")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash("El formato del correo electrónico no es válido")
            return render_template("auth/register.html")
        
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres")
            return render_template("auth/register.html")
        
        try:
            if ModelUser.user_exists(db, username=username):
                flash("El nombre de usuario ya está en uso")
                return render_template("auth/register.html")
            
            if ModelUser.user_exists(db, email=email):
                flash("El correo electrónico ya está registrado")
                return render_template("auth/register.html")
            
            ModelUser.create_user(db, username, email, password)
            return redirect(url_for("login") + "?registered=success")
            
        except Exception as ex:
            flash(f"Error al registrar usuario: {str(ex)}")
            return render_template("auth/register.html")
    else:
        return render_template("auth/register.html")





# Ruta de LOGIN - obtiene las credenciales del formulario y valida con la BD
# Si son correctas, inicia la sesión del usuario
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
    


# Ruta de LOGOUT - cierra la sesión del usuario
# Si es una petición AJAX retorna JSON, sino redirige al home
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({'success': True, 'message': 'Se cerro sesion correctamente'})
    return redirect(url_for("home"))




# Manejadores de errores
@app.errorhandler(401)
def status_401(error):
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.register_error_handler(401, status_401)
    app.run()