#!/usr/bin/env python3
"""
Cliente de ejemplo que se conecta al servidor, envía tareas y
lee las respuestas (líneas JSON).
"""

import socket
import json
import threading
import time
import uuid

HOST = '127.0.0.1'
PORT = 6000

def reader_loop(sock):
    buffer = b""
    while True:
        data = sock.recv(4096)
        if not data:
            print("[reader] servidor cerró conexión")
            break
        buffer += data
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            if not line.strip():
                continue
            try:
                obj = json.loads(line.decode())
                print("[respuesta]", json.dumps(obj, ensure_ascii=False))
            except Exception as e:
                print("[reader] error parseando respuesta:", e)

def send_task(sock, payload):
    task_id = str(uuid.uuid4())
    msg = {"task_id": task_id, "payload": payload}
    sock.sendall((json.dumps(msg, ensure_ascii=False) + "\n").encode())
    return task_id

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[main] conectado a {HOST}:{PORT}")

    t = threading.Thread(target=reader_loop, args=(sock,), daemon=True)
    t.start()

    # Enviar varias tareas
    for i in range(6):
        payload = {"numero": i, "text": f"hola {i}"}
        tid = send_task(sock, payload)
        print(f"[main] tarea enviada: {tid}")
        time.sleep(0.4)

    print("[main] enviadas todas las tareas, esperando respuestas (CTRL+C para salir)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[main] cerrando socket")
        sock.close()

if __name__ == "__main__":
    main()
