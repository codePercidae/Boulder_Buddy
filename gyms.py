import db

def get_gyms():
    return db.query_all("SELECT * FROM gyms")

def get_favourite_gym(user_id):
    return db.query_all("""SELECT MAX(route_by_gym) 
        FROM (SELECT COUNT(*) route_by_gym FROM routes, climbed 
        WHERE routes.id = climbed.route_id 
        AND climbed.user_id = (?) GROUP BY routes.gym_id)""",
        [user_id])[0]["MAX(route_by_gym)"]