from datetime import datetime, time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="ingresso")

class StatusIngresso(BaseModel):
    RESERVADO = "reservado"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    USADO = "usado"

class Ingresso(BaseModel):
    id: str
    id_sessao: str
    fila_asento: str
    num_assento: str
    nome_cliente: str
    meia_entrada: bool = False
    status: StatusIngresso
