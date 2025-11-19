import db
from datetime import date

def get_routes_by_gym(gym_id):
    db.query_all("SELECT id, name, grade FROM routes WHERE gym_id = (?)", [gym_id])

def get_routes_by_climber(username):
    db.query_some( """SELECT routes.name, routes.grade 
        FROM routes, climbed 
        WHERE climbed.user_id = (SELECT id FROM users WHERE username = (?))
        AND routes.id = climbed.route_id
        ORDER BY climbed.date DESC""", [username])

def mark_route_as_climbed(user_id, route_id):
    db.exec("INSERT INTO climbed (user_id, route_id, date) VALUES (?, ?, ?)",
        [user_id, route_id, date.today()])
      
def total_routes_by_user(user_id):
    db.query_all("SELECT COUNT(*) FROM climbed WHERE user_id = (?)", [user_id])[0]["COUNT(*)"]

def average_grade_by_user(user_id):
    db.query_all("""SELECT AVG(routes.grade)
        FROM climbed, routes 
        WHERE routes.id = climbed.route_id
        AND climbed.user_id = (?)""", [user_id])[0]["AVG(routes.grade)"]