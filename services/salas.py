from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
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
    
    @property
    def capacidade(self) -> int:
        return len(self.assentos)
    
    @property
    def assentos_disponiveis(self) -> int:
        return sum(1 for assento in self.assentos if assento.disponivel)
    
class ReservaAssentoRequest(BaseModel):
    fila: str
    numero: int

@app.get("/")
def redireciona_docs():
    return RedirectResponse(url="/docs")

@app.get("/check")
def check():
    return {"status": "ok"}

@app.get("/lista-salas")
def listaSalas():
    salas_com_info = []
    for sala in SALAS.values():
        sala_data = sala.copy()
        sala_data['capacidade'] = len(sala_data['assentos'])
        sala_data['assentos_disponiveis'] = sum(1 for a in sala_data['assentos'] if a['disponivel'])
        salas_com_info.append(sala_data)
    
    return {"salas": salas_com_info}

@app.get("/salas/{sala_numero}")
def buscaSala(sala_numero: int):
    if sala_numero not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala = SALAS[sala_numero].copy()
    sala['capacidade'] = len(sala['assentos'])
    sala['assentos_disponiveis'] = sum(1 for a in sala['assentos'] if a['disponivel'])
    
    return {"sala": sala}

@app.get("/salas/{sala_numero}/capacidade")
def get_capacidade_sala(sala_numero: int):
    if sala_numero not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala = SALAS[sala_numero]
    capacidade = len(sala['assentos'])
    assentos_disponiveis = sum(1 for a in sala['assentos'] if a['disponivel'])
    
    return {
        "numero_sala": sala_numero, 
        "capacidade": capacidade,
        "assentos_disponiveis": assentos_disponiveis
    }

@app.post("/cria-sala")
def criaSala(s: Sala):
    if s.numero in SALAS:
        raise HTTPException(409, "Sala já existente")
    
    if not s.assentos:
        s.assentos = _assenta_sala()
    
    SALAS[s.numero] = s.dict()
    return {"ok": True, "capacidade": len(s.assentos)}

@app.put("/salas/{sala_numero}/reservar-assento")
def reservar_assento_especifico(sala_numero: int, reserva: ReservaAssentoRequest):
    if sala_numero not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala = SALAS[sala_numero]
    
    for assento in sala['assentos']:
        if assento['fila'] == reserva.fila and assento['numero'] == reserva.numero:
            if not assento['disponivel']:
                raise HTTPException(409, "Assento já está ocupado")
            
            assento['disponivel'] = False
            return {
                "ok": True, 
                "assento_reservado": {
                    "fila": reserva.fila,
                    "numero": reserva.numero,
                    "tipo": assento['tipo']
                },
                "assentos_disponiveis": sum(1 for a in sala['assentos'] if a['disponivel'])
            }
    
    raise HTTPException(404, "Assento não encontrado")

@app.put("/salas/{sala_numero}/reservar-proximo-assento")
def reservar_proximo_assento(sala_numero: int):    
    if sala_numero not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala = SALAS[sala_numero]
    
    for assento in sala['assentos']:
        if assento['disponivel']:
            assento['disponivel'] = False
            
            return {
                "ok": True,
                "assento_reservado": {
                    "fila": assento['fila'],
                    "numero": assento['numero'],
                    "tipo": assento['tipo']
                },
                "assentos_disponiveis": sum(1 for a in sala['assentos'] if a['disponivel'])
            }
    
    raise HTTPException(409, "Não há assentos disponíveis")

@app.put("/salas/{sala_numero}/liberar-assento")
def liberar_assento(sala_numero: int, reserva: ReservaAssentoRequest):
    if sala_numero not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala = SALAS[sala_numero]
    capacidade = len(sala['assentos'])
    
    for assento in sala['assentos']:
        if assento['fila'] == reserva.fila and assento['numero'] == reserva.numero:
            if assento['disponivel']:
                raise HTTPException(409, "Assento já está disponível")
            
            assento['disponivel'] = True
            return {
                "ok": True,
                "assento_liberado": {
                    "fila": reserva.fila,
                    "numero": reserva.numero,
                    "tipo": assento['tipo']
                },
                "assentos_disponiveis": sum(1 for a in sala['assentos'] if a['disponivel'])
            }
    
    raise HTTPException(404, "Assento não encontrado")

@app.get("/salas/{sala_numero}/assentos")  
def lista_assentos_sala(sala_numero: int, apenas_disponiveis: bool = False):
    if sala_numero not in SALAS:
        raise HTTPException(404, "Sala não encontrada")
    
    sala = SALAS[sala_numero]
    
    if apenas_disponiveis:
        assentos = [a for a in sala['assentos'] if a['disponivel']]
    else:
        assentos = sala['assentos']
    
    return {
        "sala_numero": sala_numero,
        "total_assentos": len(sala['assentos']),
        "assentos_disponiveis": sum(1 for a in sala['assentos'] if a['disponivel']),
        "assentos": assentos
    }

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