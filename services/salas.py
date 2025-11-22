from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum
from typing import Dict

app = FastAPI(title="salas")

SALAS: Dict[int, dict] = {} 

class TipoCadeira(str, Enum):
    PADRAO = "padrao"
    VIP = "vip"

class Assento(BaseModel):
    fila: str
    numero: int
    tipo: TipoCadeira
    disponivel: bool = True

class Sala(BaseModel):
    numero: int
    assentos: List[Assento]
    disponivel: bool = True
    # Propriedade calculada para capacidade
    @property
    def capacidade(self) -> int:
        return len(self.assentos)

@app.get("/check")
def check():
    return {"status": "ok"}

@app.get("/lista-salas")
def listaSalas():
    salas_com_capacidade = []
    for sala in SALAS.values():
        sala_data = sala.copy()
        sala_data['capacidade'] = len(sala_data['assentos'])
        salas_com_capacidade.append(sala_data)
    
    return {"salas": salas_com_capacidade}

@app.post("/cria-sala")
def criaSala(s: Sala):
    if s.numero in SALAS:
        raise HTTPException(409, "Sala já existente")
    
    if not s.assentos:
        s.assentos = _assenta_sala()
    
    SALAS[s.numero] = s.dict()
    return {"ok": True, "capacidade": len(s.assentos)}

def _assenta_sala() -> List[Assento]:  
    assentos = []
    for fila_idx in range(10):
        fila_letra = chr(65 + fila_idx)
        for num_assento in range(1, 11):  
            tipo = TipoCadeira.PADRAO
            if fila_idx == 0 or fila_idx == 1:
                tipo = TipoCadeira.VIP
            
            assentos.append(Assento(
                fila=fila_letra,
                numero=num_assento,
                tipo=tipo
            ))
    return assentos

# Endpoint para obter capacidade específica
@app.get("/sala/{numero_sala}/capacidade")
def get_capacidade_sala(numero_sala: int):
    if numero_sala not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala_data = SALAS[numero_sala]
    capacidade = len(sala_data['assentos'])
    return {"numero_sala": numero_sala, "capacidade": capacidade}