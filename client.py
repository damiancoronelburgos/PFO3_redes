import socket

#definimos el main 
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creamos el socket 
    client_socket.connect(('localhost', 5000)) # configuramos la conexion del socket 
    print("Conectado al servidor. Escribí tus mensajes (escribí 'exito' para salir).")

    while True:
        mensaje = input("Tu mensaje: ")
        if mensaje.lower() == "exito": # traducimos todo a minuscula y si el usuario coloca exito  ... 
            print("Cerrando conexión...") # cierra conexion 
            break
        client_socket.send(mensaje.encode())
        respuesta = client_socket.recv(1024).decode()
        print(f"Servidor: {respuesta}")

    client_socket.close()

if __name__ == "__main__":
    main()