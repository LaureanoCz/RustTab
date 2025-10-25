from flask import Flask, render_template


app = Flask(__name__)

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

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

    
if __name__ == "__main__":
    app.run(debug=True)