from queue import Queue
import threading
import re
from db import get_connection

task_queue = Queue()

def parse_operation(operation):
    match = re.match(r"\s*([-+]?\d*\.?\d+)\s*([\+\-\*/])\s*([-+]?\d*\.?\d+)\s*$", operation)
    if match:
        a, op, b = match.groups()
        return float(a), op, float(b)
    return None

def worker():
    while True:
        task_id, operation = task_queue.get()
        try:
            parsed = parse_operation(operation)
            if not parsed:
                result = "Error: formato inválido"
            else:
                a, op, b = parsed
                if op == '+': result = a + b
                elif op == '-': result = a - b
                elif op == '*': result = a * b
                elif op == '/': result = a / b if b != 0 else "Error: división por 0"
        except Exception:
            result = "Error: formato inválido"

        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE tareas SET result=? WHERE id=?", (str(result), task_id))
        conn.commit()
        conn.close()
        task_queue.task_done()

def start_workers(num_workers=3):
    for _ in range(num_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
