from datetime import datetime, time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="sessao")

SESSOES = []

class Sessao(BaseModel):
    sessao_id: str
    filme_id: str
    sala_id: str
    hora_inicio: datetime
    hora_fim: datetime
    preco: float
    assentos_livres: int
    assentos_total: int
    disponivel: bool = True

@app.get("/check")
def check():
    return{"status": "ok"}

@app.get("/lista-sessoes")
def buscaSessoes():
    return{ "sessoes": SESSOES}