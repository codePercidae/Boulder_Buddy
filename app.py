from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import seed
from datetime import date

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

grade_to_int = { "4" : 1, "4+" : 2, "5" : 3, "5+" : 4,
                "6A" : 5, "6A+" : 6, "6B" : 7, "6B+" : 8,
                "6C" : 9, "6C+" : 10, "7A" : 11, "7A+" : 12,
                "7B" : 13, "7B+" : 14, "7C" : 15, "7C+" : 16 }

int_to_grade = { 1:"4", 2:"4+", 3:"5", 4:"5+", 5:"6A", 6:"6A+",
                7:"6B", 8:"6B+", 9:"6C", 10:"6C+", 11:"7A",
                12:"7A+", 13:"7B", 14:"7B+", 15:"7C", 16:"7C+"}


@app.route("/")
def index():
    latest = []
    if "user" in session.keys():
        res = db.query_some(
            """SELECT routes.name, routes.grade 
            FROM routes, climbed 
            WHERE climbed.user_id = (SELECT id FROM users WHERE username = (?))
            AND routes.id = climbed.route_id
            ORDER BY climbed.date DESC""",
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
    routes = db.query_all("SELECT id, name, grade FROM routes WHERE gym_id = (?)", [gym_id])
    return render_template("choose_route.html", routes=routes)

@app.route("/route_climbed", methods=["POST"])
def route_climbed():
    route_id = request.form["route"]
    user_id = db.query_all("SELECT id FROM users WHERE username = (?)", [session['user']])[0]['id']
    db.exec("INSERT INTO climbed (user_id, route_id, date) VALUES (?, ?, ?)", [user_id, route_id, date.today()])
    return redirect("/")

@app.route("/stats")
def stats():
    user_id = db.query_all("SELECT id FROM users WHERE username = (?)", [session['user']])[0]['id']
    total = db.query_all("SELECT COUNT(*) FROM climbed WHERE user_id = (?)", [user_id])[0]["COUNT(*)"]

    average_float = db.query_all("""SELECT AVG(routes.grade)
                            FROM climbed, routes 
                            WHERE routes.id = climbed.route_id
                            AND climbed.user_id = (?)""", [user_id])[0]["AVG(routes.grade)"]
    average = int_to_grade[round(average_float)]
    
    favourite = db.query_all("""SELECT MAX(route_by_gym) 
                            FROM (SELECT COUNT(*) route_by_gym FROM routes, climbed 
                            WHERE routes.id = climbed.route_id 
                            AND climbed.user_id = (?) GROUP BY routes.gym_id)""", [user_id])[0]["MAX(route_by_gym)"]
    return render_template("stats.html", total=total, average=average, favourite=favourite)