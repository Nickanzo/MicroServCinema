from datetime import date, time, timedelta, datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI(title="sessao")

SESSOES = []

FILMES_SERVICE_URL = "http://localhost:8001"
SALAS_SERVICE_URL = "http://localhost:8003"

class ReservaAssentoRequest(BaseModel):
    fila: Optional[str] = None
    numero: Optional[int] = None

class Sessao(BaseModel):
    sessao_id: str
    filme_id: str
    sala_numero: int
    data_sessao: date
    hora_inicio: time
    hora_fim: time
    preco: float
    assentos_disponiveis: int
    disponivel: bool = True

class SessaoCreate(BaseModel):
    filme_id: str
    sala_numero: int
    data_sessao: date
    hora_inicio: time
    preco: float

class ReservaSessaoResponse(BaseModel):
    ok: bool
    sessao_id: str
    assento_reservado: dict
    assentos_disponiveis: int

def verificar_filme_existe(filme_id: str) -> bool:
    try:
        response = requests.get(f"{FILMES_SERVICE_URL}/busca-filme/{filme_id}")
        return response.status_code == 200
    except:
        return False

def verificar_sala_existe(sala_numero: int) -> bool:
    try:
        response = requests.get(f"{SALAS_SERVICE_URL}/salas/{sala_numero}/capacidade")
        return response.status_code == 200
    except:
        return False

def obter_capacidade_sala(sala_numero: int) -> int:
    try:
        response = requests.get(f"{SALAS_SERVICE_URL}/salas/{sala_numero}/capacidade")
        return response.json().get("capacidade", 0) if response.status_code == 200 else 0
    except:
        return 0

def calcular_hora_fim(hora_inicio: time) -> time:
    datetime_inicio = datetime.combine(date.today(), hora_inicio)
    datetime_fim = datetime_inicio + timedelta(minutes=120)
    return datetime_fim.time()

@app.get("/check")
def check():
    return {"status": "ok"}

@app.get("/sessoes")
def listar_sessoes():
    return {"sessoes": SESSOES}

@app.get("/sessoes/{sessao_id}")
def buscar_sessao(sessao_id: str):
    for sessao in SESSOES:
        if sessao["sessao_id"] == sessao_id:
            return {"sessao": sessao}
    raise HTTPException(404, "Sessão não encontrada")

@app.post("/sessoes")
def criar_sessao(sessao_data: SessaoCreate):
    if not verificar_filme_existe(sessao_data.filme_id):
        raise HTTPException(404, "Filme não encontrado")
    
    if not verificar_sala_existe(sessao_data.sala_numero):
        raise HTTPException(404, "Sala não encontrada")
    
    capacidade = obter_capacidade_sala(sessao_data.sala_numero)
    if capacidade == 0:
        raise HTTPException(400, "Sala não possui assentos")
    
    hora_fim = calcular_hora_fim(sessao_data.hora_inicio)
    
    nova_sessao = Sessao(
        sessao_id=f"sessao_{len(SESSOES) + 1}",
        filme_id=sessao_data.filme_id,
        sala_numero=sessao_data.sala_numero,
        data_sessao=sessao_data.data_sessao,
        hora_inicio=sessao_data.hora_inicio,
        hora_fim=hora_fim,
        preco=sessao_data.preco,
        assentos_disponiveis=capacidade
    )
    
    SESSOES.append(nova_sessao.dict())
    return {"ok": True, "sessao": nova_sessao.dict()}

@app.put("/sessoes/{sessao_id}/reservar-assento")
def reservar_assento_sessao(sessao_id: str, reserva: ReservaAssentoRequest):
    sessao = None
    for s in SESSOES:
        if s["sessao_id"] == sessao_id:
            sessao = s
            break
    
    if not sessao:
        raise HTTPException(404, "Sessão não encontrada")
    
    if sessao["assentos_disponiveis"] <= 0:
        raise HTTPException(409, "Não há assentos disponíveis nesta sessão")
    
    sala_numero = sessao["sala_numero"]
    
    try:        
        if reserva.fila and reserva.numero:
            response = requests.put(
                f"{SALAS_SERVICE_URL}/salas/{sala_numero}/reservar-assento",
                json={"fila": reserva.fila, "numero": reserva.numero}
            )
        else:
            response = requests.put(
                f"{SALAS_SERVICE_URL}/salas/{sala_numero}/reservar-proximo-assento"
            )
        
        if response.status_code == 200:
            resultado = response.json()
            sessao["assentos_disponiveis"] -= 1
            
            return ReservaSessaoResponse(
                ok=True,
                sessao_id=sessao_id,
                assento_reservado=resultado["assento_reservado"],
                assentos_disponiveis=sessao["assentos_disponiveis"]
            )
        else:
            raise HTTPException(response.status_code, response.json().get("detail", "Erro ao reservar assento"))
            
    except requests.RequestException:
        raise HTTPException(503, "Serviço de salas indisponível")

@app.put("/sessoes/{sessao_id}/liberar-assento")
def liberar_assento_sessao(sessao_id: str, reserva: ReservaAssentoRequest):
    if not reserva.fila or not reserva.numero:
        raise HTTPException(400, "Fila e número do assento são obrigatórios para liberação")
    
    sessao = None
    for s in SESSOES:
        if s["sessao_id"] == sessao_id:
            sessao = s
            break
    
    if not sessao:
        raise HTTPException(404, "Sessão não encontrada")
    
    sala_numero = sessao["sala_numero"]
    capacidade = obter_capacidade_sala(sala_numero)
    
    if sessao["assentos_disponiveis"] >= capacidade:
        raise HTTPException(409, "Todos os assentos já estão disponíveis")
    
    try:
        response = requests.put(
            f"{SALAS_SERVICE_URL}/salas/{sala_numero}/liberar-assento",
            json={"fila": reserva.fila, "numero": reserva.numero}
        )
        
        if response.status_code == 200:
            sessao["assentos_disponiveis"] += 1
            
            return {
                "ok": True,
                "sessao_id": sessao_id,
                "assento_liberado": response.json()["assento_liberado"],
                "assentos_disponiveis": sessao["assentos_disponiveis"]
            }
        else:
            raise HTTPException(response.status_code, response.json().get("detail", "Erro ao liberar assento"))
            
    except requests.RequestException:
        raise HTTPException(503, "Serviço de salas indisponível")

@app.get("/sessoes/{sessao_id}/assentos-disponiveis")
def listar_assentos_disponiveis_sessao(sessao_id: str):
    sessao = None
    for s in SESSOES:
        if s["sessao_id"] == sessao_id:
            sessao = s
            break
    
    if not sessao:
        raise HTTPException(404, "Sessão não encontrada")
    
    try:
        response = requests.get(
            f"{SALAS_SERVICE_URL}/salas/{sessao['sala_numero']}/assentos",
            params={"apenas_disponiveis": True}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(response.status_code, "Erro ao buscar assentos")
            
    except requests.RequestException:
        raise HTTPException(503, "Serviço de salas indisponível")