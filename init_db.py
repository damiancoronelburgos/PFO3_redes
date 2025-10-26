import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )          
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tareas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT,
            descripcion TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )          
    ''')
    
    conn.commit()
    conn.close()
    print('Base de datos inicializada en app.db')
    
if __name__ == "__main__":
    init_db()
