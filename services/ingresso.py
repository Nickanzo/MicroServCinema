from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import requests

app = FastAPI(title="ingresso")

INGRESSOS = []

FILMES_SERVICE_URL = "http://localhost:8001"
SALAS_SERVICE_URL = "http://localhost:8002"
SESSAO_SERVICE_URL = "http://localhost:8003"

class StatusIngresso(BaseModel):
    RESERVADO = "reservado"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    USADO = "usado"

class Ingresso(BaseModel):
    ingresso_id: str
    sessao_id: str
    fila_asento: str
    num_assento: int
    nome_cliente: str
    meia_entrada: bool = False
    status: StatusIngresso = StatusIngresso.RESERVADO
    data_compra: datetime
    preco_pago: float

class IngressoCreate(BaseModel):
    sessao_id: str
    fila_assento: str
    num_assento: int
    nome_cliente: str
    meia_entrada: bool = False

class IngressoUpdate(BaseModel):
    nome_cliente: Optional[str] = None
    meia_entrada: Optional[bool] = None
    status: Optional[StatusIngresso] = None

def verificar_sessao_existe(sessao_id: str) -> bool:
    try:
        response = requests.get(f"{SESSAO_SERVICE_URL}/sessoes/{sessao_id}")
        return response.status_code == 200
    except:
        return False    
    
def obter_detalhes_sessao(sessao_id: str) -> dict:
    try:
        response = requests.get(f"{SESSAO_SERVICE_URL}/sessoes/{sessao_id}")
        return response.json().get("sessao") if response.status_code == 200 else None
    except:
        return None
    
def obter_detalhes_filme(filme_id: str) -> dict:
    try:
        response = requests.get(f"{FILMES_SERVICE_URL}/busca-filme/{filme_id}")
        return response.json().get("filme") if response.status_code == 200 else None
    except:
        return None
    
def reservar_assento_na_sessao(sessao_id: str, fila: str, numero: int) -> bool:
    try:
        response = requests.put(
            f"{SESSAO_SERVICE_URL}/sessoes/{sessao_id}/reservar-assento",
            json={"fila": fila, "numero": numero}
        )
        return response.status_code == 200
    except:
        return False    
    
def liberar_assento_na_sessao(sessao_id: str, fila: str, numero: int) -> bool:
    try:
        response = requests.put(
            f"{SESSAO_SERVICE_URL}/sessoes/{sessao_id}/liberar-assento",
            json={"fila": fila, "numero": numero}
        )
        return response.status_code == 200
    except:
        return False    

def verificar_assento_disponivel(sessao_id: str, fila: str, numero: int) -> bool:
    try:
        response = requests.get(f"{SESSAO_SERVICE_URL}/sessoes/{sessao_id}/assentos-disponiveis")
        if response.status_code == 200:
            assentos_disponiveis = response.json().get("assentos", [])
            return any(
                assento["fila"] == fila and assento["numero"] == numero 
                for assento in assentos_disponiveis
            )
        return False
    except:
        return False
    
def calcular_preco(sessao_id: str, meia_entrada: bool) -> float:
    try:
        sessao = obter_detalhes_sessao(sessao_id)
        if sessao:
            preco_base = sessao.get("preco", 0)
            return preco_base * 0.5 if meia_entrada else preco_base
        return 0
    except:
        return 0    

@app.get("/")
def redireciona_docs():
    return RedirectResponse(url="/docs")

@app.get("/check")
def check():
    return{"status": "ok"}

@app.get("/ingressos")
def listar_ingressos():
    return {"ingressos": INGRESSOS}

@app.get("/ingressos/{ingresso_id}")
def buscar_ingresso(ingresso_id: str):
    for ingresso in INGRESSOS:
        if ingresso["ingresso_id"] == ingresso_id:
            return {"ingresso": ingresso}
    raise HTTPException(404, "Ingresso não encontrado")

@app.post("/ingressos")
def criar_ingresso(ingresso_data: IngressoCreate):
    if not verificar_sessao_existe(ingresso_data.sessao_id):
        raise HTTPException(404, "Sessão não encontrada")
    
    if not verificar_assento_disponivel(ingresso_data.sessao_id, ingresso_data.fila_assento, ingresso_data.num_assento):
        raise HTTPException(409, "Assento já ocupado ou não disponível")
    
    if not reservar_assento_na_sessao(ingresso_data.sessao_id, ingresso_data.fila_assento, ingresso_data.num_assento):
        raise HTTPException(409, "Não foi possível reservar o assento")
    
    preco_pago = calcular_preco(ingresso_data.sessao_id, ingresso_data.meia_entrada)
    
    novo_ingresso = Ingresso(
        ingresso_id=f"ingresso_{len(INGRESSOS) + 1}",
        sessao_id=ingresso_data.sessao_id,
        fila_assento=ingresso_data.fila_assento,
        num_assento=ingresso_data.num_assento,
        nome_cliente=ingresso_data.nome_cliente,
        meia_entrada=ingresso_data.meia_entrada,
        status=StatusIngresso.RESERVADO,
        data_compra=datetime.now(),
        preco_pago=preco_pago
    )
    
    INGRESSOS.append(novo_ingresso.dict())
    return {"ok": True, "ingresso": novo_ingresso.dict()}

@app.put("/ingressos/{ingresso_id}/confirmar")
def confirmar_ingresso(ingresso_id: str):
    for ingresso in INGRESSOS:
        if ingresso["ingresso_id"] == ingresso_id:
            if ingresso["status"] != StatusIngresso.RESERVADO:
                raise HTTPException(409, f"Ingresso não pode ser confirmado. Status atual: {ingresso['status']}")
            
            ingresso["status"] = StatusIngresso.CONFIRMADO
            return {"ok": True, "ingresso": ingresso}
    
    raise HTTPException(404, "Ingresso não encontrado")
    
@app.put("/ingressos/{ingresso_id}/usar")
def usar_ingresso(ingresso_id: str):
    for ingresso in INGRESSOS:
        if ingresso["ingresso_id"] == ingresso_id:
            if ingresso["status"] not in [StatusIngresso.CONFIRMADO, StatusIngresso.RESERVADO]:
                raise HTTPException(409, f"Ingresso não pode ser usado. Status atual: {ingresso['status']}")
            
            ingresso["status"] = StatusIngresso.USADO
            return {"ok": True, "ingresso": ingresso}
    
    raise HTTPException(404, "Ingresso não encontrado")

@app.put("/ingressos/{ingresso_id}/cancelar")
def cancelar_ingresso(ingresso_id: str):
    for ingresso in INGRESSOS:
        if ingresso["ingresso_id"] == ingresso_id:
            if ingresso["status"] == StatusIngresso.USADO:
                raise HTTPException(409, "Ingresso já utilizado não pode ser cancelado")
            
            if liberar_assento_na_sessao(ingresso["sessao_id"], ingresso["fila_assento"], ingresso["num_assento"]):
                ingresso["status"] = StatusIngresso.CANCELADO
                return {"ok": True, "ingresso": ingresso}
            else:
                raise HTTPException(500, "Erro ao liberar assento")
    
    raise HTTPException(404, "Ingresso não encontrado")

@app.get("/ingressos/sessao/{sessao_id}")
def listar_ingressos_por_sessao(sessao_id: str):
    ingressos_sessao = [ingresso for ingresso in INGRESSOS if ingresso["sessao_id"] == sessao_id]
    return {"ingressos": ingressos_sessao, "total": len(ingressos_sessao)}

@app.get("/ingressos/cliente/{nome_cliente}")
def listar_ingressos_por_cliente(nome_cliente: str):
    ingressos_cliente = [ingresso for ingresso in INGRESSOS if ingresso["nome_cliente"].lower() == nome_cliente.lower()]
    return {"ingressos": ingressos_cliente, "total": len(ingressos_cliente)}

@app.get("/ingressos/status/{status}")
def listar_ingressos_por_status(status: StatusIngresso):
    ingressos_status = [ingresso for ingresso in INGRESSOS if ingresso["status"] == status]
    return {"ingressos": ingressos_status, "total": len(ingressos_status)}

@app.get("/ingressos/{ingresso_id}/detalhes")
def detalhes_completos_ingresso(ingresso_id: str):
    for ingresso in INGRESSOS:
        if ingresso["ingresso_id"] == ingresso_id:
            sessao = obter_detalhes_sessao(ingresso["sessao_id"])
            if sessao:
                filme = obter_detalhes_filme(sessao["filme_id"])
                
                return {
                    "ingresso": ingresso,
                    "sessao": sessao,
                    "filme": filme
                }
    
    raise HTTPException(404, "Ingresso não encontrado")