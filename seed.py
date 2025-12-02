from random import randint
import sqlite3

def test():

    int_to_grade = { 1:"4", 2:"4+", 3:"5", 4:"5+", 5:"6A", 6:"6A+",
                    7:"6B", 8:"6B+", 9:"6C", 10:"6C+", 11:"7A",
                    12:"7A+", 13:"7B", 14:"7B+", 15:"7C", 16:"7C+"}

    db = sqlite3.connect('boulder.db')

    db.execute('DELETE FROM users')
    db.execute('DELETE FROM routes')
    db.execute('DELETE FROM gyms')
    db.execute('DELETE FROM climbed')

    user_count = 1000
    gym_count = 10
    route_count = 800

    for i in range(1, user_count + 1):
        db.execute("INSERT INTO users (username) VALUES (?)", ["user" + str(i)])

    for i in range(1, gym_count + 1):
        db.execute("INSERT INTO gyms (name) VALUES (?)", ["gym" + str(i)])

    for i in range(1, route_count + 1):
        route_int = randint(1, 16)
        db.execute("INSERT INTO routes (name, grade, grade_int, gym_id) VALUES (?, ?, ?, ?)",
                ["route" + str(i), int_to_grade[route_int], route_int, randint(1, gym_count)])
        
    for i in range(10000):
        try:
            db.execute("INSERT INTO climbed (route_id, user_id) VALUES (?, ?)",
                    [randint(1, route_count), randint(1, user_count)])
        except:
            pass
        
    db.commit()
    db.close()