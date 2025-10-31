from flask import request, session, jsonify
from db import get_connection

def register_user():
    username = request.form["username"]
    password = request.form["password"]
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"status": "Registro exitoso"})
    except:
        return jsonify({"status": "Error: usuario ya existe"})

def login_user():
    username = request.form["username"]
    password = request.form["password"]
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM usuarios WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    conn.close()
    if row:
        session["user_id"] = row[0]
        return jsonify({"status": "Login exitoso"})
    else:
        return jsonify({"status": "Credenciales incorrectas"})
