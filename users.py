import db

def create_user(username, phash):
    db.exec("INSERT INTO users (username, password) VALUES (?, ?)", [username, phash])

def get_user_id(username):
    return db.query_all("SELECT id FROM users WHERE username = (?)", username)[0]["id"]

def get_password(username):
    return db.query_all("SELECT id, password FROM users WHERE username = ?", username)[0]["password"]