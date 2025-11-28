import sqlite3
from os import system
from flask import g #why tho?

def init_db():
    system('touch boulder.db')
    system("sqlite3 boulder.db < schema.sql")
    
def get_connection():
    db = sqlite3.connect("boulder.db")
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db

def exec(sql, params=[]):
    db = get_connection()
    res = db.execute(sql, params)
    db.commit()
    g.last_insert_id = res.lastrowid
    db.close()

def query_all(sql, params=[]):
    db = get_connection()
    res = db.execute(sql, params).fetchall()
    db.close()
    return res

def query_some(sql, amount, params=[]):
    db = get_connection()
    res = db.execute(sql, params).fetchmany(amount)
    db.close()
    return res

def delete_all():
    db = get_connection()
    db.execute('DELETE FROM climbed')
    db.execute('DELETE FROM users')
    db.execute('DELETE FROM routes')
    db.execute('DELETE FROM gyms')
    db.commit()
    db.close()