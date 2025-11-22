from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel
from enum import Enum
from typing import Dict

app = FastAPI(title="filmes")

FILMES: Dict[int, Filme] = {}

class GeneroFilme(str, Enum):
    ACAO = "acao"
    COMEDIA = "comedia"
    TERROR = "terror"
    ROMANCE = "romance"
    SUSPENSE = "suspense"
    INFANTIL = "infantil"
    NACIONAL = "nacional"

class Filme(BaseModel):
    filme_id: int
    nome: str
    genero: GeneroFilme
    data_lancamento: date
    emCartaz: bool = True

@app.get("/check")
def check():
    return{"status": "ok"}

@app.post("/novo-filme")
def criaFilme(f : Filme):
    if f.filme_id in FILMES:
        raise HTTPException(409, "Filme já cadastrado")
    
    FILMES[f.filme_id] = f
    return {"ok": True}

@app.get("/lista-filmes")
def listaFilmes():    
    return {"filmes": list(FILMES.values())}
        

@app.get("/busca-filme/{filme_id}")
def buscaFilme(filme_id: int):
    try:
        filme_id_int = int(filme_id)
    except ValueError:
        raise HTTPException(400, "ID do filme deve ser um número")
    if filme_id_int not in FILMES:
        raise HTTPException(404, "Filme não encontrado...")
    return {"filme": FILMES[filme_id_int]}