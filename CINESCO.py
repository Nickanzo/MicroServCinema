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
import requests, os, time

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
    response = make_request("salas", "/lista-salas")
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
                #adicionar_filme()
                pass
            case "3":
                pass
                #buscar_filme()
            case "4":
                limpa_tela()
                tela_inicial()
                break
            case _:
                popup("Opção inválida!", "err")
                espera_usuario()
                limpa_tela()

def listar_filmes():
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

def gerenciar_salas():
    while True:
        limpa_tela()
        titulo_menu("GERENCIAR SALAS")
        print("1 - Listar Salas")
        print("2 - Criar Sala")
        print("3 -  Voltar ao Menu Principal")
        
        opcao = input("\n Escolha uma opção: ")
        
        match opcao:
            case "1":
                listar_salas()
                pass
            case "2":
                #criar_sala()
                pass
            case "3":
                break
            case _:
                popup("Opção inválida!", "err")

def listar_salas():
    limpa_tela()
    titulo_menu("LISTA DE SALAS")
    
    salas = get_salas()
    if not salas:
        popup("Nenhuma sala cadastrada.", "info")
    else:
        for sala in salas:
            print(f"Sala {sala.get('numero')}")
            print(f"Capacidade: {sala.get('capacidade', 'N/A')} assentos")
            print(f"Disponíveis: {sala.get('assentos_disponiveis', 'N/A')}")
            print(f"Status: {'Disponível' if sala.get('disponivel') else 'Indisponível'}")
            print()
    
    espera_usuario()

def gerenciar_sessoes():
    while True:
        limpa_tela()
        titulo_menu("GERENCIAR SESSÕES")
        print("1 - Listar Sessões")
        print("2 - Criar Sessão")
        print("3 - Mostra Assentos de Sessao")        
        print("4 - Voltar ao Menu Principal")
        
        opcao = input("\n Escolha uma opção: ")
        
        match opcao:
            case "1":
                listar_sessoes()
                pass
            case "2":
                #criar_sessao()
                pass
            case "3":
                mostra_assentos()
            case "4":
                break
            case _:
                popup("Opção inválida!", "err")

def listar_sessoes():
    limpa_tela()
    titulo_menu("LISTA DE SESSÕES")
    
    sessoes = get_sessoes()
    if not sessoes:
        popup("Nenhuma sessão agendada.", "info")
    else:
        for sessao in sessoes:
            print(f"{sessao.get('sessao_id')}")
            print(f"Filme ID: {sessao.get('filme_id')}")
            print(f"Sala: {sessao.get('sala_numero')}")
            print(f"Data: {sessao.get('data_sessao')}")
            print(f"Horário: {sessao.get('hora_inicio')} - {sessao.get('hora_fim')}")
            print(f"Preço: R$ {sessao.get('preco', 0):.2f}")
            print(f"Assentos Disponíveis: {sessao.get('assentos_disponiveis')}")
            print()
    
    espera_usuario()

def display_cadeiras_sessao(sessao_id: str):
    limpa_tela()
    titulo_menu(f"MAPEAMENTO DE CADEIRAS - SESSÃO {sessao_id}")
    
    try:
        sessao_response = make_request("sessao", f"/sessoes/{sessao_id}")
        if not sessao_response or sessao_response.status_code != 200:
            popup("Sessão não encontrada", "err")
            espera_usuario()
            return
        
        sessao = sessao_response.json().get("sessao", {})
        sala_numero = sessao.get("sala_numero")
        
        assentos_response = make_request("sessao", f"/sessoes/{sessao_id}/assentos-disponiveis")
        if not assentos_response or assentos_response.status_code != 200:
            popup("Erro ao buscar assentos da sessão", "err")
            espera_usuario()
            return
        
        assentos_data = assentos_response.json()
        assentos_disponiveis = assentos_data.get("assentos", [])
        
        ingressos_response = make_request("ingresso", f"/ingressos/sessao/{sessao_id}")
        ingressos_vendidos = []
        if ingressos_response and ingressos_response.status_code == 200:
            ingressos_vendidos = ingressos_response.json().get("ingressos", [])
        
        assentos_ocupados = {}
        for ingresso in ingressos_vendidos:
            if ingresso.get("status") in ["reservado", "confirmado", "usado"]:
                fila = ingresso.get("fila_assento")
                numero = ingresso.get("num_assento")
                assentos_ocupados[f"{fila}{numero}"] = ingresso
        
        print(f"Sessão: {sessao_id}")
        print(f"Sala: {sala_numero}")
        print(f"Capacidade: {assentos_data.get('total_assentos', 0)} assentos")
        print(f"Disponíveis: {assentos_data.get('assentos_disponiveis', 0)} assentos")
        print(f"Ocupados: {len(assentos_ocupados)} assentos")
        print()
        
        print(" " * 15 + "-" * 10)
        print(" " * 10 + " T E L A  D O  C I N E M A")
        print(" " * 15 + "-" * 10)
        print()
        
        print("     " + "".join(f"{i:2}" for i in range(1, 11)))
        print("    ┌" + "──" * 9 + "───┐")
        
        fileiras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        
        for fileira in fileiras:
            linha = f"  {fileira} │"
            for numero in range(1, 11):
                assento_id = f"{fileira}{numero}"
                
                if assento_id in assentos_ocupados:
                    ingresso = assentos_ocupados[assento_id]
                    if ingresso.get("status") == "confirmado":
                        linha += "🟢"
                    else:
                        linha += "🟡"
                else:
                    disponivel = any(
                        a["fila"] == fileira and a["numero"] == numero 
                        for a in assentos_disponiveis
                    )
                    if disponivel and fileira == "A" or fileira == "B":
                        linha += "🔹"
                    elif disponivel:
                        linha += "🟦"
                    else:
                        linha += "🟥"
            
            linha += " │"
            print(linha)
        
        print("    └" + "──" * 9 + "───┘")
        print()
        
        print(" LEGENDA:")
        print("   🟦 Disponível   🔹 VIP   🟡 Reservado   🟢 Confirmado   🟥 Indisponível")
        print()
        
        if assentos_ocupados:
            print(" ASSENTOS OCUPADOS:")
            for assento_id, ingresso in list(assentos_ocupados.items())[:5]:
                print(f"   {assento_id}: {ingresso.get('nome_cliente')} - {ingresso.get('status')}")
            if len(assentos_ocupados) > 5:
                print(f"   ... e mais {len(assentos_ocupados) - 5} assentos ocupados")
        
    except Exception as e:
        popup(f"Erro ao exibir cadeiras: {e}", "err")
    
    espera_usuario()

def mostrar_estatisticas():
    limpa_tela()
    titulo_menu("ESTATÍSTICAS DO CINEMA")
    
    filmes = get_filmes()
    salas = get_salas()
    sessoes = get_sessoes()
    ingressos = get_ingressos()
    
    receita_total = sum(
        ingresso["preco_pago"] for ingresso in ingressos 
        if ingresso.get("status") != "cancelado"
    )
    
    total_assentos = sum(sala.get("capacidade", 0) for sala in salas)
    assentos_ocupados = len([i for i in ingressos if i.get("status") in ["reservado", "confirmado", "usado"]])
    ocupacao_media = (assentos_ocupados / total_assentos * 100) if total_assentos > 0 else 0
    
    print(f"Filmes em Cartaz: {len(filmes)}")
    print(f"Salas Disponíveis: {len(salas)}")
    print(f"Sessões Agendadas: {len(sessoes)}")
    print(f"Ingressos Vendidos: {len(ingressos)}")
    print(f"Receita Total: R$ {receita_total:.2f}")
    print(f"Ocupação Média: {ocupacao_media:.1f}%")
    
    espera_usuario()    

def mostra_assentos():
    sessao = input("Informe a sessao: ")

    display_cadeiras_sessao(sessao)

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

    while True:
    
        print(" Selecione uma das opções a seguir: ")
        print("1 - Estatísticas do Cinema")
        print("2 - Gerenciar Filmes")
        print("3 - Gerenciar Salas") 
        print("4 - Gerenciar Sessões")
        #print("5 - Gerenciar Ingressos")
        print("5 - Sair")

        usr = input()

        match usr:
            case "1":
                mostrar_estatisticas()
                pass
            case "2":
                gerenciar_filmes()
                pass    
            case "3":
                gerenciar_salas()
                pass
            case "4":
                gerenciar_sessoes()
                pass
            case "5":
                limpa_tela()
                for i in range(6):
                    print(f"\rEncerrando CINESCO {i*20}%", end="",flush=True)
                    time.sleep(0.5)
                print("Obrigado por usar CINESCO !")                                        
                break
            case _:
                popup("Selecione uma opcao valida !", 'err')            
                espera_usuario()

        limpa_tela()                



if __name__ == "__main__":   

    limpa_tela()
    for i in range(6):
        print(f"\rInicializando CINESCO {i*20}%", end="",flush=True)
        time.sleep(0.5)
    limpa_tela()

    tela_inicial()
    
    menu_principal()    

