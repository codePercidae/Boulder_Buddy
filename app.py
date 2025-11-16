from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import seed

app = Flask(__name__)
app.secret_key = config.secret_key

@app.cli.command("create-test-data")
def create_test_data():
    seed.test()
    print("Test data created")

@app.cli.command("delete-all")
def delete_all():
    db.delete_all()
    print("Database deleted!")

@app.cli.command("init-database")
def init_db():
    db.init_db()
    print("Database initiated!")

@app.route("/")
def index():
    latest = []
    if "user" in session.keys():
        res = db.query_some(
            """SELECT routes.name, routes.grade 
            FROM routes, climbed 
            WHERE climbed.user_id = (SELECT id FROM users WHERE username = (?))
            AND routes.id = climbed.route_id""",
            10, [session['user']])
        latest = [f'{r["name"]} {r["grade"]}' for r in res]
    return render_template("index.html", latest=latest)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/logout")
def logout():
    del session["user"]
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
    user_id = db.query_all("SELECT id FROM users WHERE username = (?)", [session['user']])[0]['id']
    print(user_id, route_id)
    db.exec("INSERT INTO climbed (user_id, route_id) VALUES (?, ?)", [user_id, route_id])
    return redirect("/")