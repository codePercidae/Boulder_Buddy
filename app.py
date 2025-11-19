from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import seed
from datetime import date
import users as u
import misc as m
import routes as r
import gyms as g

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
        res = r.get_routes_by_climber(session["user"])
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
            u.create_user(username, phash)
            return "Käyttäjätunnus luotu, ole hyvä ja kirjaudu sisään."
        except:
            return "Käyttäjätunnus varattu!"
        
@app.route("/verify", methods=["POST"])
def verify():
    username = request.form["username"]
    password = request.form["password"]

    res = u.get_password(username)
    if res and check_password_hash(res, password):
        session['user'] = username
        return redirect("/")
    else:
        return "Virheelliset käyttäjätunnukset!"
    
@app.route("/choose_gym")
def choose_gym():
    gyms = g.get_gyms()
    return render_template("choose_gym.html", gyms=gyms)

@app.route("/choose_route", methods=["POST"])
def choose_route():
    gym_id = request.form["gym"]
    routes = r.get_routes_by_gym(gym_id)
    return render_template("choose_route.html", routes=routes)

@app.route("/route_climbed", methods=["POST"])
def route_climbed():
    route_id = request.form["route"]
    user_id = u.get_user_id(session["user"])
    r.mark_route_as_climbed(user_id, route_id)
    return redirect("/")

@app.route("/stats")
def stats():
    user_id = u.get_user_id(session["user"])
    total = r.total_routes_by_user(user_id)

    average_float = r.average_grade_by_user(user_id)
    average = m.int_to_grade[round(average_float)]

    #Palauttaa salin id:n, ei 
    favourite = g.get_favourite_gym(user_id)
    return render_template("stats.html", total=total, average=average, favourite=favourite)