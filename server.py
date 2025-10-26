import socket
from database import setup_db, save_message
from datetime import datetime

def init_socket(): #definimos la funcion de inicio del socket 
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost',5000))
        server_socket.listen()
        print("Servidor escuchando en localhost:5000")
        return server_socket
    except socket.error as errorExcepcion:
        print(f"Error al iniciar el socket: {errorExcepcion}")
        return None
    client_socket.close()
    
def handle_client(client_socket, client_address):
    while True:
        try:
            mensaje = client_socket.recv(1024).decode()
            if not mensaje:
                break
            save_message(mensaje, client_address[0])
            client_socket.send(f"Mensaje recibido: {datetime.now()}".encode())
        except Exception as e:
            print(f"Error con {client_address}: {e}")
            break
    client_socket.close()
    
    
    
setup_db()
server_socket = init_socket()

if server_socket: #en este punto es donde se produce el intercambio cliente-servidor
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"cliente conectado: {client_address}")
        handle_client(client_socket, client_address)