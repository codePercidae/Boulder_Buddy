from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import create_test_data

app = Flask(__name__)
app.secret_key = config.secret_key

@app.cli.command("create-test-data")
def test():
    create_test_data
    print("Test data created")

@app.cli.command("delete-all")
def delete_all():
    db.delete_all()
    print("Database deleted!")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/logout")
def logout():
    del session["user"]
    del session["id"]
    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "Salasanat eivät täsmää!"

    else:
        phash = generate_password_hash(password1)
        try:
            db.exec("INSERT INTO users (username, password) VALUES (?, ?)", [username, phash])
            return "Käyttäjätunnus luotu, ole hyvä ja kirjaudu sisään."
        except:
            return "Käyttäjätunnus varattu!"
        
@app.route("/verify", methods=["POST"])
def verify():
    username = request.form["username"]
    password = request.form["password"]

    res = db.query_all("SELECT id, password FROM users WHERE username = ?", [username])
    if res and check_password_hash(res[0]['password'], password):
        session['user'] = username
        session['id'] = res[0]['id']
        #session['latest_routes'] = db.query_some("SELECT route_id FROM users WHERE user_id = ?", [session['id']], 10)
        return redirect("/")
    else:
        return "Virheelliset käyttäjätunnukset!"
    
@app.route("/choose_gym")
def choose_gym():
    gyms = db.query_all("SELECT * FROM gyms")
    return render_template("choose_gym.html", gyms=gyms)

@app.route("/choose_route", methods=["POST"])
def choose_route():
    gym_id = request.form["gym"]
    print(gym_id)
    routes = db.query_all("SELECT id, name, grade FROM routes WHERE gym_id = (?)", [gym_id])
    return render_template("choose_route.html", routes=routes)

@app.route("/route_climbed", methods=["POST"])
def route_climbed():
    route_id = request.form["route"]
    db.exec("INSERT INTO climbed (user_id, route_id) VALUES (?, ?)", [route_id, session['id']])
    return "Reitti lisätty"