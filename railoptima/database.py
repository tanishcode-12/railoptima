import sqlite3
import bcrypt

def create_connection():
    conn = sqlite3.connect("railoptima_users.db", check_same_thread=False)
    return conn

conn = create_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    train_number TEXT,
    train_name TEXT
)
""")

conn.commit()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def create_user(username, password):
    try:
        hashed_pw = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        return check_password(password, result[0])
    return False

def save_favorite(username, train_number, train_name):
    cursor.execute("INSERT INTO favorites (username, train_number, train_name) VALUES (?, ?, ?)", (username, train_number, train_name))
    conn.commit()

def get_favorites(username):
    cursor.execute("SELECT train_number, train_name FROM favorites WHERE username = ?", (username,))
    return cursor.fetchall()

def remove_favorite(username, train_number):
    cursor.execute("DELETE FROM favorites WHERE username = ? AND train_number = ?", (username, train_number))
    conn.commit()
