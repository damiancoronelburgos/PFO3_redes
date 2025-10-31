import sqlite3
import os

DB_NAME = "app.db"

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                operation TEXT NOT NULL,
                result TEXT,
                FOREIGN KEY(user_id) REFERENCES usuarios(id)
            )
        ''')
        conn.commit()
        conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
