"""
================================================================================
CINESCO - Sistema de Gerenciamento de Cinema
Desenvolvedor: Nicolas Escobar
Instituição: Instituto Federal de Santa Catarina - IFSC Campus Gaspar
Curso: Tecnologia em Análise e Desenvolvimento de Sistemas
Docente: Simone de Ramos
Disciplina: Programação Concorrente e Distribuida
Versão: 1.0.0
Arquitetura: Microserviços
================================================================================
"""
import requests, os

SERVICES = {
    "filmes": "http://localhost:8001",
    "salas": "http://localhost:8002",
    "sessao": "http://localhost:8003",
    "ingresso": "http://localhost:8004"
}

def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def titulo_menu(title):
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)    

def popup(message, type):    
    match type:
        case "err":
            print(f"\nX ! {message} !")
            pass
        case "info":
            print(f"\n| {message} |")
            pass
        case "ok":
            print(f"\n✔ {message}")
            pass

def make_request(service, endpoint, method="GET", data=None):
    try:
        url = f"{SERVICES[service]}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        return response
    except requests.exceptions.RequestException:
        return None
    
def get_filmes():
    response = make_request("filmes", "/lista-filmes")
    return response.json().get("filmes", []) if response else []

def get_salas():
    response = make_request("salas", "/salas")
    return response.json().get("salas", []) if response else []

def get_sessoes():
    response = make_request("sessao", "/sessoes")
    return response.json().get("sessoes", []) if response else []

def get_ingressos():
    response = make_request("ingresso", "/ingressos")
    return response.json().get("ingressos", []) if response else []

def gerenciar_filmes():
    while True:
        limpa_tela()
        titulo_menu("GERENCIAR FILMES")
        print("1 - Listar Filmes")
        print("2 - Adicionar Filme")
        print("3 - Buscar Filme")
        print("4 - Voltar ao Menu Principal")
        
        opcao = input("\n Escolha uma opção: ")

        match opcao:
            case "1":
                listar_filmes()
                pass
            case "2":
                adicionar_filme()
                pass
            case "3":
                pass
                buscar_filme()
            case "4":
                limpa_tela()
                tela_inicial()
                break
            case _:
                popup("Opção inválida!", "err")
                espera_usuario()
                limpa_tela()

def listar_filmes():
    """Lista todos os filmes"""
    limpa_tela()
    titulo_menu("LISTA DE FILMES")
    
    filmes = get_filmes()
    if not filmes:
        popup("Nenhum filme cadastrado.", "info")
    else:
        for i, filme in enumerate(filmes, 1):
            print(f"{i}. {filme.get('nome', 'N/A')}")
            print(f"ID: {filme.get('filme_id', 'N/A')}")
            print(f"Gênero: {filme.get('genero', 'N/A')}")
            print(f"Lançamento: {filme.get('data_lancamento', 'N/A')}")
            print(f"Em Cartaz: {'Sim' if filme.get('emCartaz') else 'Não'}")
            print()
    
    espera_usuario()


def espera_usuario():
    input("\n Pressione Enter para continuar...\n")

def tela_inicial():

    print()
    print("  ██████  ██ ███    ██ ███████  ██████  ██████   ██████ ")
    print(" ██       ██ ████   ██ ██       ██      ██      ██    ██")
    print(" ██       ██ ██ ██  ██ █████    ██████  ██      ██    ██")
    print(" ██       ██ ██  ██ ██ ██          ███  ██      ██    ██")
    print("  ██████  ██ ██   ████ ███████  ██████  ██████   ██████ ")
    print()
    print("           C I N E M A   S Y S T E M \n")

def menu_principal():

    print(" Selecione uma das opções a seguir: ")
    print("1 - Estatísticas do Cinema")
    print("2 - Gerenciar Filmes")
    print("3 - Gerenciar Salas") 
    print("4 - Gerenciar Sessões")
    print("5 - Gerenciar Ingressos")
    print("6 - Carregar dados no Cinema")
    print("7 - Sair")
    
    usr = input()

    match usr:
        case "2":
            gerenciar_filmes()
            pass    
        case "6":
            pass
        case _:
            popup("Selecione uma opcao valida !", 'err')            
            espera_usuario()
            limpa_tela()

if __name__ == "__main__":

    tela_inicial()

    while True:
        menu_principal()

