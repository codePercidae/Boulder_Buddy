from flask import Flask
from flask import render_template, request, redirect, session, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
import db
import config
import seed
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

def require_login():
    if "user_id" not in session:
        abort(403)

def check_token():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    latest = []
    if "user_id" in session.keys():
        res = r.get_routes_by_climber(session["user_id"])
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
    del session["user_id"]
    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("Salasanat eivät täsmää!")
        return redirect("/signup")
    
    elif len(password1) < 4 or len(username) < 4:
        flash("Salasana tai käyttäjätunnus liian lyhyt!")
        return redirect("/signup")
    elif len(username) > 20 or len(password1) > 20:
        flash("Salasana tai käyttäjätunnus liian pitkä!")
        return redirect("/signup")
    else:
        phash = generate_password_hash(password1)
        try:
            u.create_user(username, phash)
            flash("Käyttäjätunnus luotu, ole hyvä ja kirjaudu sisään.")
            return redirect("/")
        except:
            flash("Käyttäjätunnus varattu!")
            return redirect("/signup")
        
@app.route("/verify", methods=["POST"])
def verify():
    username = request.form["username"]
    password = request.form["password"]

    try:
        phash = u.get_password(username)
        id = u.get_user_id(username)
        if phash and check_password_hash(phash, password):
            session['user'] = username
            session['user_id'] = id
            session['csrf_token'] = token_hex(16)
            return redirect("/")
    except:
        flash("Virheelliset käyttäjätunnukset!")
        return redirect("/signin")
    
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
    require_login()
    route_id = request.form["route"]
    r.mark_route_as_climbed(session["user_id"], route_id)
    flash("Reitti merkitty kiivetyksi!")
    return redirect("/")

@app.route("/stats")
def stats():
    require_login()
    user_routes = r.get_routes_by_climber(session["user_id"])
    total = r.total_routes_by_user(session["user_id"])
    if total > 0:
        average_float = r.average_grade_by_user(session["user_id"])
        average = m.int_to_grade[round(average_float)]

        #Palauttaa salin id:n, ei nimeä
        favourite = g.get_favourite_gym(session["user_id"])
        
    return render_template("stats.html", total=total,
                        average=average, favourite=favourite, routes=user_routes)

@app.route("/delete", methods=["POST"])
def delete():
    require_login()
    route_id = request.form["route_id"]
    r.delete_from_climbed(session["user_id"], route_id)
    flash("Reitti poistettu kiivetyistä!")
    return redirect("/stats")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    name = u.get_username(user_id)
    routes = r.get_routes_by_climber(user_id)
    return render_template("/user.html", routes=routes, username=name)

@app.route("/search_user", methods=["GET", "POST"])
def search_user():
    query = request.args.get("query")
    res = u.search_users(query) if query else []
    return render_template("search_user.html", users = res)
