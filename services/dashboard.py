from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx, os

FILMES_URL    = os.getenv("FILMES_URL",  "http://127.0.0.1:3001")
INGRESSOS_URL = os.getenv("INGRESSOS_URL", "http://127.0.0.1:3002")
SALAS_URL     = os.getenv("SALAS_URL",  "http://127.0.0.1:3003")
SESSOES_URL   = os.getenv("SESSOES_URL",  "http://127.0.0.1:3004")

app = FastAPI(title="dashboard")

