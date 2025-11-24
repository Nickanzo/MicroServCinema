from fastapi import FastAPI
import uvicorn
import threading, time, os, sys
import requests, json
from datetime import date, time as time_type

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.filmes import app as filmes_app
from services.salas import app as salas_app
from services.sessao import app as sessao_app

SERVICES = {
    "filmes": "http://127.0.0.1:8001",
    "salas": "http://127.0.0.1:8002", 
    "sessao": "http://127.0.0.1:8003"
}

FILMES_FICTICIOS = [
    {
        "filme_id": 1,
        "nome": "Matrix - Ressurrections",
        "genero": "acao",
        "data_lancamento": "2021-12-22",
        "emCartaz": True
    },
    {
        "filme_id": 2,
        "nome": "Toy Story 5",
        "genero": "infantil", 
        "data_lancamento": "2024-06-15",
        "emCartaz": True
    },
    {
        "filme_id": 3,
        "nome": "O Poderoso Chefão - Edição Especial",
        "genero": "suspense",
        "data_lancamento": "2024-03-10",
        "emCartaz": True
    },
    {
        "filme_id": 4,
        "nome": "A Noite do Terror",
        "genero": "terror",
        "data_lancamento": "2024-10-31", 
        "emCartaz": False
    }
]

SALAS_FICTICIAS = [
    {
        "numero": 1,
        "assentos": [],
        "disponivel": True
    },
    {
        "numero": 2, 
        "assentos": [],
        "disponivel": True
    },
    {
        "numero": 3,
        "assentos": [],
        "disponivel": True
    },
    {
        "numero": 4,
        "assentos": [],
        "disponivel": False
    }
]

SESSOES_FICTICIAS = [
    {
        "filme_id": "1",
        "sala_numero": 1,
        "data_sessao": "2024-12-20",
        "hora_inicio": "14:30:00",
        "preco": 25.50
    },
    {
        "filme_id": "1",
        "sala_numero": 1,
        "data_sessao": "2024-12-20",
        "hora_inicio": "19:00:00",
        "preco": 28.00
    },
    {
        "filme_id": "2",
        "sala_numero": 2,
        "data_sessao": "2024-12-20",
        "hora_inicio": "15:00:00",
        "preco": 22.00
    },
    {
        "filme_id": "2",
        "sala_numero": 2,
        "data_sessao": "2024-12-21",  # Dia diferente
        "hora_inicio": "16:30:00",
        "preco": 24.00
    },
    {
        "filme_id": "3",
        "sala_numero": 3,
        "data_sessao": "2024-12-20",
        "hora_inicio": "18:00:00",
        "preco": 30.00
    },
    {
        "filme_id": "3",
        "sala_numero": 3,
        "data_sessao": "2024-12-21",
        "hora_inicio": "21:00:00",
        "preco": 32.00
    },
    {
        "filme_id": "4",
        "sala_numero": 4,
        "data_sessao": "2024-12-20",
        "hora_inicio": "22:00:00",
        "preco": 35.00
    },
    {
        "filme_id": "4",
        "sala_numero": 4,
        "data_sessao": "2024-12-21",
        "hora_inicio": "22:30:00",
        "preco": 35.00
    }
]


def wait_for_service(service_name, url, max_retries=30, delay=1):

    print(f"Aguardando {service_name} ficar disponível...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/check", timeout=2)
            if response.status_code == 200:
                print(f"{service_name} está disponível!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            time.sleep(delay)
    
    print(f"{service_name} não ficou disponível após {max_retries} tentativas")
    return False

def criar_filmes_ficticios():

    for filme in FILMES_FICTICIOS:
        try:
            response = requests.post(
                f"{SERVICES['filmes']}/novo-filme",
                json=filme
            )
            if response.status_code == 200:
                print(f"Filme criado: {filme['nome']}")
            else:
                print(f"Erro ao criar filme {filme['nome']}: {response.text}")
        except Exception as e:
            print(f"Erro ao criar filme {filme['nome']}: {e}")

def criar_salas_ficticias():
    
    for sala in SALAS_FICTICIAS:
        try:
            response = requests.post(
                f"{SERVICES['salas']}/cria-sala",
                json=sala
            )
            if response.status_code == 200:
                print(f"Sala {sala['numero']} criada")
            else:
                print(f"Erro ao criar sala {sala['numero']}: {response.text}")
        except Exception as e:
            print(f"Erro ao criar sala {sala['numero']}: {e}")

def criar_sessoes_ficticias():
    
    for sessao in SESSOES_FICTICIAS:
        try:
            response = requests.post(
                f"{SERVICES['sessao']}/sessoes",
                json=sessao
            )
            if response.status_code == 200:
                print(f"Sessão criada: Filme {sessao['filme_id']} - Sala {sessao['sala_numero']}")
            else:
                print(f"Erro ao criar sessão: {response.text}")
        except Exception as e:
            print(f"Erro ao criar sessão: {e}")

def popular_dados_teste():
    services_ready = all([
        wait_for_service("Filmes", SERVICES["filmes"]),
        wait_for_service("Salas", SERVICES["salas"]),
        wait_for_service("Sessões", SERVICES["sessao"])
    ])
    
    if not services_ready:
        print("Alguns serviços não ficaram disponíveis. Dados de teste não serão criados.")
        return
    
    criar_filmes_ficticios()
    time.sleep(1)  
    
    criar_salas_ficticias() 
    time.sleep(1)
    
    criar_sessoes_ficticias()
    
    print("\nURLs para teste:")
    print(f"Filmes: {SERVICES['filmes']}/docs")
    print(f"Salas: {SERVICES['salas']}/docs") 
    print(f"Sessões: {SERVICES['sessao']}/docs")

app = FastAPI(title="dashboard")

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port = port, log_level = "info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(filmes_app, 8001), daemon=True),
        threading.Thread(target=run, args=(salas_app, 8002), daemon=True),
        threading.Thread(target=run, args=(sessao_app, 8003), daemon=True),
    ]
    for t in threads: t.start()
    print("Rodando: filmes:8001, salas:8002, sessoes:8003")

    time.sleep(2)
    data_thread = threading.Thread(target=popular_dados_teste, daemon=True)
    data_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")