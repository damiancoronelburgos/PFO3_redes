from flask import render_template, request, jsonify, session, redirect, url_for
from auth import register_user, login_user
from tasks import task_queue, start_workers
from db import get_connection

def register_routes(app):
    start_workers()  # Inicializar workers

    @app.route("/")
    def home():
        return redirect(url_for("login_page"))

    @app.route("/register", methods=["GET", "POST"])
    def register_page():
        if request.method == "POST":
            return register_user()
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login_page():
        if request.method == "POST":
            return login_user()
        return render_template("login.html")

    @app.route("/task", methods=["GET", "POST"])
    def task_page():
        if "user_id" not in session:
            return redirect(url_for("login_page"))
        if request.method == "POST":
            operation = request.form["operation"]
            user_id = session["user_id"]
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO tareas (user_id, operation) VALUES (?, ?)", (user_id, operation))
            task_id = c.lastrowid
            conn.commit()
            conn.close()
            task_queue.put((task_id, operation))
            return jsonify({"status": "Tarea enviada"})
        return render_template("task.html")

    @app.route("/results")
    def get_results():
        if "user_id" not in session:
            return jsonify([])
        user_id = session["user_id"]
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT operation, result FROM tareas WHERE user_id=? ORDER BY id", (user_id,))
        rows = c.fetchall()
        conn.close()
        results = [f"{op} = {res if res else 'procesando...'}" for op, res in rows]
        return jsonify(results)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login_page"))
