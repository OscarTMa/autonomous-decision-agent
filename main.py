import datetime

class AutonomousAgent:
    def __init__(self, agent_name: str):
        self.name = agent_name
        self.memory = []

    def perceive(self, message: str, user_tier: str = "standard") -> dict:
        """Paso 1: Captura entrada y contexto."""
        return {
            "message": message,
            "user_tier": user_tier,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def reason(self, perception: dict) -> dict:
        """Paso 2: Clasifica intención y elige estrategia."""
        msg = perception["message"].lower()
        
        if "caido" in msg or "sin internet" in msg:
            intent = "service_outage"
            strategy = "full_autonomous_resolution"
        else:
            intent = "general_query"
            strategy = "guided_autonomous_resolution"

        return {
            "intent": intent,
            "strategy": strategy,
            "perception": perception
        }

    def act(self, decision: dict) -> list:
        """Paso 3: Genera y ejecuta un plan de acción."""
        strategy = decision["strategy"]
        if strategy == "full_autonomous_resolution":
            plan = ["1. Diagnosticar red", "2. Reiniciar puerto", "3. Confirmar estado"]
        else:
            plan = ["1. Buscar en base de conocimiento", "2. Enviar respuesta"]
        
        # Simulación de ejecución
        results = [f"Ejecutado: {step}" for step in plan]
        return results

    def run(self, user_message: str):
        p = self.perceive(user_message)
        r = self.reason(p)
        a = self.act(r)
        
        # Paso 4: Guardar en memoria de sesión
        self.memory.append({"decision": r, "action_results": a})
        return a

if __name__ == "__main__":
    agent = AutonomousAgent("SupportBot")
    response = agent.run("Mi internet está caído desde la mañana")
    print("Respuesta del Agente:", response)