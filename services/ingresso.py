from datetime import datetime, time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="ingresso")

INGRESSOS = []

class StatusIngresso(BaseModel):
    RESERVADO: "reservado"
    CONFIRMADO: "confirmado"
    CANCELADO: "cancelado"
    USADO: "usado"

class Ingresso(BaseModel):
    ingresso_id: str
    sessao_id: str
    fila_asento: str
    num_assento: str
    nome_cliente: str
    meia_entrada: bool = False
    status: StatusIngresso

@app.get("/check")
def check():
    return{"status": "ok"}

@app.get("/verifica-ingresso/{ingresso_id}")
def statusIngresso(ingresso_id: str):
    ingresso = INGRESSOS.get(ingresso_id)
    