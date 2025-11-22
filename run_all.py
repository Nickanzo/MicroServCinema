from fastapi import FastAPI, HTTPException
import uvicorn
import threading, time
from pydantic import BaseModel
import httpx, os

from services.filmes import app as filmes_app
from services.ingresso import app as ingresso_app
from services.salas import app as salas_app
from services.sessao import app as sessao_app

FILMES_URL    = os.getenv("FILMES_URL",  "http://127.0.0.1:8001/docs")
INGRESSOS_URL = os.getenv("INGRESSOS_URL", "http://127.0.0.1:8002/docs")
SALAS_URL     = os.getenv("SALAS_URL",  "http://127.0.0.1:8003/docs")
SESSOES_URL   = os.getenv("SESSOES_URL",  "http://127.0.0.1:8004/docs")

app = FastAPI(title="dashboard")

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port = port, log_level = "info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(filmes_app, 8001), daemon=True),
        threading.Thread(target=run, args=(ingresso_app, 8002), daemon=True),
        threading.Thread(target=run, args=(salas_app, 8003), daemon=True),
        threading.Thread(target=run, args=(sessao_app, 8004), daemon=True),
    ]
    for t in threads: t.start()
    print("Services up: filmes:3001, ingresso:3002, salas:3003, sessoes:3004")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")