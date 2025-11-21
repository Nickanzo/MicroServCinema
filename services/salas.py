from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="salas")

SALAS = []

class TipoCadeira(str, Enum):
    PADRAO: "padrao"
    VIP: "vip"

class Assento(BaseModel):
    fila: str
    numero: int
    tipo: TipoCadeira
    disponivel: bool = True

class Sala(BaseModel):
    numero: int
    capacidade: int
    assentos: List[Assento]
    disponivel: bool = True

@app.get("/check")
def check():
    return{"status": "ok"}

@app.get("/lista-salas")
def listaSalas():
    return{ "salas": SALAS}

@app.post("/cria-sala")
def criaSala(s : Sala):
    SALAS.append({"numero": len(SALAS), "capacidade": s.capacidade, "assentos": _assenta_sala()})    

def _assenta_sala(self) -> List[Assento]:
    assentos = []
    for fila_idx in range(10):
        fila_letra = chr(65 + fila_idx)
        for num_assento in range(1, 10 + 1):
            tipo = TipoCadeira.PADRAO
            if fila_idx == 0 or fila_idx == 1:
                tipo = TipoCadeira.VIP
            
            assentos.append(Assento(
                fila=fila_letra,
                numero=num_assento,
                tipo=tipo
            ))
    return assentos
