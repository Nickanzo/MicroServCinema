import subprocess
import time
import sys

def run_service(module_name, port):
    try:
        cmd = [sys.executable, "-m", "uvicorn", f"services.{module_name}:app", "--port", str(port), "--reload"]
        process = subprocess.Popen(cmd)
        print(f"{module_name} rodando na porta {port}")
        return process
    except Exception as e:
        print(f"Erro ao iniciar {module_name}: {e}")
        return None

if __name__ == "__main__":
    services = [
        #("dashboard", 8000)
        ("filmes", 8001),
        ("salas", 8002),
        ("sessao", 8003),        
        ("ingresso", 8004),        
    ]
    
    processes = []
    
    for service, port in services:
        process = run_service(service, port)
        if process:
            processes.append(process)
        time.sleep(2)
    
    print("\n Todos os serviços estão rodando!")
    print("Dashboard: http://localhost:8000/docs")
    print("Sessões: http://localhost:8002/docs")    
    print("Filmes: http://localhost:8001/docs")
    print("Salas: http://localhost:8003/docs")
    print("Ingresso: http://localhost:8004/docs")
    
    try:        
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        print("Fechando CINESCO...")
        for process in processes:
            process.terminate()