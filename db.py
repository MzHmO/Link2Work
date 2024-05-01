import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE = "database.db"

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (self.username,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return False
        password_hash = data['password']
        return check_password_hash(password_hash, password)

class Database:
    @staticmethod
    def Connect(db_name=DATABASE):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def setup_db():
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(user_id):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        return User(id=data['id'], username=data['username'])

    @staticmethod
    def register_user(username, password):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))

        user = cursor.fetchone()
        
        if user:
            conn.close()
            return 'User already exists', False

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, generate_password_hash(password)))

        conn.commit()
        conn.close()

        user_folder = os.path.join(os.getcwd(), 'files', str(cursor.lastrowid ))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        return 'User successfully registered', True

    @staticmethod
    def get_user_by_username(username):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        return User(id=data['id'], username=data['username'])

    @staticmethod
    def validate_login(username, password):
        user = Database.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
