# 1️⃣ Importaciones
from flask import Flask, request, g, redirect, url_for, render_template, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import webbrowser
from init_db import init_db


# 2️⃣ Configuración de la app
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678Damian'
DATABASE = 'app.db'

# 3️⃣ Función para conectarse a la base de datos
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

# 4️⃣ Función para cerrar la base de datos automáticamente
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
        
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

        if not usuario or not contrasena:
            flash("Todos los campos son obligatorios")
            return redirect(url_for('registro'))

        db = get_db()
        existing = db.execute('SELECT id FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
        if existing:
            flash("El usuario ya existe")
            return redirect(url_for('registro'))

        password_hash = generate_password_hash(contrasena)
        db.execute('INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)',
                    (usuario, password_hash))
        db.commit()
        flash("Usuario registrado con éxito")
        return redirect(url_for('login'))

    # Esto maneja GET
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

        db = get_db()
        user = db.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()

        if user and check_password_hash(user['password_hash'], contrasena):
            session['user_id'] = user['id']
            flash("Inicio de sesión exitoso")
            return redirect(url_for('tareas'))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for('login'))

    # Esto maneja GET
    return render_template('login.html')


@app.route('/tareas')
def tareas():
    if 'user_id' not in session:
        flash("Debes iniciar sesión primero")
        return redirect(url_for('login'))

    db = get_db()
    user = db.execute('SELECT usuario FROM usuarios WHERE id = ?', (session['user_id'],)).fetchone()
    return render_template('tareas.html', usuario=user['usuario'])


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/index")
    app.run(debug=True, host='0.0.0.0', port=5000)



