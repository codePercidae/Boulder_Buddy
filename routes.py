import db
from datetime import date

def get_routes_by_gym(gym_id):
    return db.query_all("SELECT id, name, grade FROM routes WHERE gym_id = (?)", [gym_id])

def get_routes_by_climber(user_id):
    return db.query_some("""SELECT routes.id, routes.name, routes.grade, gyms.name AS gym
        FROM routes, climbed, gyms
        WHERE climbed.user_id = (?)
        AND routes.id = climbed.route_id
        AND gyms.id = routes.gym_id
        ORDER BY climbed.date DESC""", 10, [user_id])

def mark_route_as_climbed(user_id, route_id, comment):
    db.exec("INSERT INTO climbed (user_id, route_id, date, comment) VALUES (?, ?, ?, ?)",
        [user_id, route_id, date.today(), comment])
      
def total_routes_by_user(user_id):
    return db.query_all("SELECT COUNT(route_id) FROM climbed WHERE user_id = (?)",
        [user_id])[0]["COUNT(route_id)"]

def average_grade_by_user(user_id):
    return db.query_all("""SELECT AVG(routes.grade_int)
        FROM climbed, routes 
        WHERE routes.id = climbed.route_id
        AND climbed.user_id = (?)""", [user_id])[0]["AVG(routes.grade_int)"]

def delete_from_climbed(user_id, route_id):
    db.exec("DELETE FROM climbed WHERE user_id = (?) AND route_id = (?)",
        [user_id, route_id])