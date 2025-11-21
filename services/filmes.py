from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Dict

app = FastAPI(title="filmes")

FILMES = []

class GeneroFilme(str, Enum):
    ACAO = "acao"
    COMEDIA = "comedia"
    TERROR = "terror"
    ROMANCE = "romance"
    SUSPENSE = "suspense"
    INFANTIL = "infantil"
    NACIONAL = "nacional"

class Filme(BaseModel):
    filme_id: str
    nome: str
    genero: GeneroFilme
    data_lancamento: datetime
    emCartaz: bool = True

@app.get("/check")
def check():
    return{"status": "ok"}

@app.post("/novo-filme")
def criaFilme(f : Filme):
    if f.filme_id in FILMES:
        raise HTTPException(409, "Filme já cadastrado")
    FILMES[f.filme_id] = {
        "nome": f.nome,
        "genero": f.genero,
        "data_lancamento": f.data_lancamento,
        "emCartaz": f.emCartaz
        }
    return {"ok": True}

@app.get("/lista-filmes")
def listaFilmes():
    return {"filmes": FILMES}
        

@app.get("/busca-filme/{filme_id}")
def buscaFilme(filme_id: str):
    filme = FILMES.get(filme_id)
    if not filme:
        raise HTTPException(404, "Filme não encontrado...")
    return {"filme": filme}