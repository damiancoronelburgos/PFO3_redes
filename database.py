import sqlite3
from datetime import datetime 

def setup_db(): # definimos la creacion de base de datos  
    conexion = sqlite3.connect("mensajes.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contenido TEXT NOT NULL,
        fecha_envio TEXT NOT NULL,
        ip_cliente TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()
    
print("Tabla 'messages' creada correctamente.")


def save_message(contenido, ip_cliente): #en este punto definimos la funcion guardar mensaje
    try:
        conexion = sqlite3.connect("mensajes.db")
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO messages(contenido, fecha_envio, ip_cliente) VALUES (?,?,?)",
            (contenido, str(datetime.now()), ip_cliente)
        )
        #hasta este punto lo que hicimos es guardar el contenido, fecha de envio e ip 
        
        conexion.commit()
        conexion.close()
        print((f"Se guardo el mensaje con exito"))
        
    except sqlite3.Error as errorExcepcion:
        print((f"No se pudo guardar el mensaje: {errorExcepcion}")) # manejo de errores
        