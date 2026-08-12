import os
from dotenv import load_dotenv
from src.agent import AutonomousAgent

load_dotenv()

def main():
    # Inicializa el agente conectado a Gemini y ChromaDB
    agent = AutonomousAgent()
    
    # 1. Primera interacción
    query_1 = "Mi conexión de red falla intermitentemente desde hace dos días."
    print(f"--- INTERACCIÓN 1 ---")
    print(f"Usuario: {query_1}\n")
    
    result_1 = agent.run(user_message=query_1, interaction_id="session_001", user_tier="premium")
    
    print("Decisión:", result_1["decision"]["strategy"])
    print("Razonamiento:", result_1["decision"]["reasoning"])
    print("Ejecución:", result_1["execution"]["execution_logs"])
    
    print("\n" + "="*50 + "\n")

    # 2. Segunda interacción (Recupera la memoria previa)
    query_2 = "Sigo sin señal, ¿pudieron revisar el estado del puerto?"
    print(f"--- INTERACCIÓN 2 (Con consulta a Memoria Episódica) ---")
    print(f"Usuario: {query_2}\n")
    
    result_2 = agent.run(user_message=query_2, interaction_id="session_002", user_tier="premium")
    
    print("Decisión:", result_2["decision"]["strategy"])
    print("Razonamiento:", result_2["decision"]["reasoning"])
    print("Ejecución:", result_2["execution"]["execution_logs"])

if __name__ == "__main__":
    main()