from fastapi import FastAPI
import uvicorn
import threading, time
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.salas import app as salas_app

SALAS_URL    = os.getenv("SALAS_URL",  "http://127.0.0.1:8002/docs")

app = FastAPI(title="dashboard")

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port = port, log_level = "info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(salas_app, 8002), daemon=True),
    ]
    for t in threads: t.start()
    print("Rodando: salas:8002")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")