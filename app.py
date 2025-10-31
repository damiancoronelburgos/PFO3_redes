from flask import Flask
from db import init_db
from routes import register_routes

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Inicializar DB
init_db()

# Registrar rutas
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
