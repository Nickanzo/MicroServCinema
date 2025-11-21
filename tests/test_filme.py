from fastapi import FastAPI, HTTPException
import uvicorn
import threading, time
from pydantic import BaseModel
import httpx, os

from services.filmes import app as filmes_app

FILMES_URL    = os.getenv("FILMES_URL",  "http://127.0.0.1:3001")

app = FastAPI(title="Teste")

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port = port, log_level = "info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(filmes_app, 8001), daemon=True)
    ]
    for t in threads: t.start()
    print("Services up: filmes:3001")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")