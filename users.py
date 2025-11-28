import db

def create_user(username, phash):
    db.exec("INSERT INTO users (username, password) VALUES (?, ?)",
        [username, phash])

def get_user_id(username):
    return db.query_all("SELECT id FROM users WHERE username = (?)",
        [username])[0]["id"]

def get_password(username):
    return db.query_all("SELECT id, password FROM users WHERE username = (?)",
        [username])[0]["password"]

def get_username(user_id):
    return db.query_all("SELECT username FROM users WHERE id = (?)",
        [user_id])[0]["username"]

def search_users(key):
    return db.query_all("SELECT id, username FROM users WHERE username LIKE (?)",
        ["%" + key + "%"])