#!/usr/bin/env python3
"""
Servidor que acepta conexiones TCP de clientes.
Recibe tareas en JSON por línea, las encola y un pool de workers las procesa.
Los workers devuelven resultado al cliente por el mismo socket.
"""

import socket
import threading
import queue
import json
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 6000
WORKER_COUNT = 4
TASK_QUEUE_MAX = 1000

# Colas y estructuras globales
task_queue = queue.Queue(maxsize=TASK_QUEUE_MAX)

# Guardamos info de cliente: {client_id: {'sock': socket, 'lock': Lock, 'addr': addr}}
clients_lock = threading.Lock()
clients = {}  # client_id -> client_info

def process_task_payload(payload):
    """
    Lógica de procesamiento de tarea.
    Aquí simulamos trabajo (sleep) y devolvemos un resultado.
    Reemplazá por tu lógica real (DB, S3, ML, etc).
    """
    # Simular trabajo
    time.sleep(1)
    result = {
        "processed_at": datetime.utcnow().isoformat() + "Z",
        "input": payload,
        "status": "ok",
        "note": "Procesado por worker"
    }
    return result

def worker_loop(worker_id):
    print(f"[worker-{worker_id}] iniciado")
    while True:
        try:
            task = task_queue.get()
            if task is None:
                # Señal de apagado
                print(f"[worker-{worker_id}] recibiendo señal de cierre")
                break

            client_id, task_id, payload = task
            # Procesar
            print(f"[worker-{worker_id}] procesando task {task_id} de client {client_id}")
            try:
                result = process_task_payload(payload)
            except Exception as e:
                result = {"status": "error", "error": str(e)}

            # Enviar resultado al cliente si sigue conectado
            with clients_lock:
                client_info = clients.get(client_id)

            if client_info:
                resp = {
                    "task_id": task_id,
                    "result": result
                }
                try:
                    msg = json.dumps(resp, ensure_ascii=False) + "\n"
                    with client_info['lock']:
                        client_info['sock'].sendall(msg.encode())
                except Exception as e:
                    print(f"[worker-{worker_id}] Error al enviar resultado a client {client_id}: {e}")
            else:
                print(f"[worker-{worker_id}] client {client_id} ya no está conectado; resultado descartado")

            task_queue.task_done()
        except Exception as e:
            print(f"[worker-{worker_id}] excepción en loop: {e}")

def client_listener(client_sock, addr, client_id):
    """
    Lee líneas JSON desde el socket del cliente y encola tareas.
    Formato esperado por tarea (JSON por línea):
    {"task_id": "abc123", "payload": {...}}
    """
    print(f"[listener] cliente conectado {addr}, id={client_id}")
    buffer = b""
    try:
        while True:
            data = client_sock.recv(4096)
            if not data:
                print(f"[listener] cliente {client_id} desconectó")
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line.decode())
                    task_id = obj.get("task_id") or f"{client_id}-{int(time.time()*1000)}"
                    payload = obj.get("payload") if "payload" in obj else obj
                    # Encolar tarea: (client_id, task_id, payload)
                    try:
                        task_queue.put_nowait((client_id, task_id, payload))
                        ack = {"ack": True, "task_id": task_id}
                        with clients_lock:
                            client_info = clients.get(client_id)
                        if client_info:
                            with client_info['lock']:
                                client_info['sock'].sendall((json.dumps(ack) + "\n").encode())
                    except queue.Full:
                        err = {"ack": False, "error": "queue_full"}
                        with clients_lock:
                            client_info = clients.get(client_id)
                        if client_info:
                            with client_info['lock']:
                                client_info['sock'].sendall((json.dumps(err) + "\n").encode())
                except json.JSONDecodeError:
                    err = {"ack": False, "error": "invalid_json"}
                    with clients_lock:
                        client_info = clients.get(client_id)
                    if client_info:
                        with client_info['lock']:
                            client_info['sock'].sendall((json.dumps(err) + "\n").encode())

    except Exception as e:
        print(f"[listener] excepción con client {client_id}: {e}")
    finally:
        # limpieza al desconectar
        with clients_lock:
            clients.pop(client_id, None)
        try:
            client_sock.close()
        except:
            pass
        print(f"[listener] terminado para client {client_id}")

def accept_loop(server_sock):
    next_client_id = 1
    while True:
        client_sock, addr = server_sock.accept()
        client_id = f"c{next_client_id}"
        next_client_id += 1
        client_info = {
            "sock": client_sock,
            "lock": threading.Lock(),
            "addr": addr
        }
        with clients_lock:
            clients[client_id] = client_info

        t = threading.Thread(target=client_listener, args=(client_sock, addr, client_id), daemon=True)
        t.start()

def main():
    # Iniciar pool de workers
    for i in range(WORKER_COUNT):
        t = threading.Thread(target=worker_loop, args=(i+1,), daemon=True)
        t.start()

    # Iniciar socket servidor
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(100)
    print(f"[main] Servidor escuchando en {HOST}:{PORT}")

    try:
        accept_loop(server_sock)
    except KeyboardInterrupt:
        print("[main] Detenido por teclado, enviando señales de cierre a workers...")
    finally:
        # Enviar señales de apagado a workers
        for _ in range(WORKER_COUNT):
            task_queue.put(None)
        server_sock.close()
        print("[main] servidor cerrado")

if __name__ == "__main__":
    main()
