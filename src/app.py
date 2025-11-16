from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
import re

import os
import json
import MySQLdb.cursors

from config import config

# Models
from models.ModelUser import ModelUser
from models.ModelSong import ModelSong

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




# Esta ruta renderiza la plantilla "index.html" cuando se accede a la ruta "/home".
# Ruta de HOME
@app.route("/home")
def home():
    return render_template("index.html")






# Esta ruta renderiza la plantilla "fav.html" cuando se accede a la ruta "/fav".
# Ruta de pagina de canciones favoritas
@app.route("/fav")
def fav():
    return render_template("fav.html")






# Ruta dinamica de canciones
@app.route("/song/<title>")
def song(title):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM songs WHERE title = %s", (title,))
    song = cursor.fetchone()

    if not song:
        return 404

    json_path = os.path.join("static", "tablatures", song["json_file"])

    with open(json_path, "r", encoding="utf-8") as f:
        tab_data = json.load(f)

    return render_template("songs.html", song=song, tab_data=tab_data)




'''
Esta ruta gestiona el registro de nuevos usuarios.  
Cuando se envía el formulario mediante una petición POST, primero se obtienen y normalizan los datos ingresados: nombre de usuario, correo electrónico y contraseña.  
Luego se realizan varias validaciones: verificar que los campos obligatorios no estén vacíos, comprobar que el correo tenga un formato válido y asegurar que la contraseña cumpla con la longitud mínima requerida.  

Después de validar los datos, se revisa si el nombre de usuario o el correo ya están registrados en la base de datos mediante ModelUser.user_exists().  
Si ninguno está en uso, se crea un nuevo usuario con ModelUser.create_user() y se redirige a la página de inicio de sesión with un mensaje de éxito.  

Si ocurre algún error durante el proceso, se captura la excepción y se muestra un mensaje explicando el problema.  
Para solicitudes GET (cuando simplemente se accede a la página), la ruta únicamente renderiza el formulario de registro.
'''
# Rutas de REGISTER y LOGIN
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





'''
En esta ruta se obtienen los datos enviados desde el formulario y se crean con ellos los atributos del objeto "user". Luego, dichos datos se verifican mediante la función ModelUser.login(), que valida las credenciales en la base de datos. Si la autenticación es exitosa, se inicia la sesión del usuario y se redirige a la página principal. En caso contrario, se muestra un mensaje indicando que el usuario o la contraseña son incorrectos.
'''
# Ruta LOGIN y LOGOUT
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
    


'''
Esta ruta se encarga de cerrar la sesión del usuario autenticado.  
Primero ejecuta logout_user() para finalizar la sesión manejada por Flask-Login y luego limpia por completo la sesión con session.clear().  

Si la petición proviene de AJAX (verificada mediante el encabezado 'X-Requested-With' o si el contenido es JSON), la ruta responde con un JSON indicando que el cierre de sesión fue exitoso.  
En caso contrario, realiza una redirección hacia la página principal.
'''
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({'success': True, 'message': 'Se cerro sesion correctamente'})
    return redirect(url_for("home"))




# Manejo de errores
def status_401(error):
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.register_error_handler(401, status_401)
    app.run()