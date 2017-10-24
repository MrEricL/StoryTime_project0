import db_builder
import sqlite3

f = "usersandstories.db"

db = sqlite3.connect(f) #opens f
c = db.cursor() #facilitates db ops


def authenticate(user, passw):
    command = "SELECT username, password FROM user_table WHERE username 
