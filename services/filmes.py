from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Dict

app = FastAPI(title="filmes")

FILMES: Dict[str, dict] = {}

class GeneroFilme(str, Enum):
    ACAO = "acao"
    COMEDIA = "comedia"
    TERROR = "terror"
    ROMANCE = "romance"
    SUSPENSE = "suspense"
    INFANTIL = "infantil"
    NACIONAL = "nacional"

class Filme(BaseModel):
    id: str
    nome: str
    genero: GeneroFilme
    data_lancamento: datetime
    emCartaz: bool

@app.GET("/check")
def check():
    return{"status": "ok"}

@app.POST("/novo-filme")
def criaFilme(f : Filme):

@app.GET("/lista-filmes")
def listaFilmes():

@app.GET("/busca-filme/{filme_id}")
def buscaFilme():
