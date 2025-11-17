from datetime import datetime, time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

class Sessao(Basemodel):
    id: str
    filme_id: str
    sala_id: str
    hora_inicio: datetime
    hora_fim: datetime
    preco: float
    assentos_livres: int
    assentos_total: int
    disponivel: bool = True