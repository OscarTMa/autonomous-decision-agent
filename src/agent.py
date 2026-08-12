import os
import chromadb
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class DecisionContext(BaseModel):
    intent: str = Field(description="Clasificación de la intención del usuario")
    urgency: str = Field(description="Nivel de urgencia: ALTA, MEDIA o BAJA")
    strategy: str = Field(description="Estrategia seleccionada")
    reasoning: str = Field(description="Justificación detallada")
    action_plan: list[str] = Field(description="Lista de pasos a ejecutar")

class AutonomousAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no configurada en el archivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
        # Inicialización de Memoria Episódica con ChromaDB
        self.chroma_client = chromadb.Client()
        self.memory_collection = self.chroma_client.get_or_create_collection(name="episodic_memory")

    def recall_memories(self, query: str, limit: int = 2) -> list[str]:
        """Recupera contexto histórico relevante utilizando la búsqueda nativa de ChromaDB."""
        if self.memory_collection.count() == 0:
            return []
        
        results = self.memory_collection.query(
            query_texts=[query],
            n_results=limit
        )
        return results["documents"][0] if results["documents"] else []

    def remember(self, user_message: str, outcome: str, interaction_id: str):
        """Guarda la interacción procesada directamente en ChromaDB."""
        record_text = f"Usuario: {user_message} | Resultado: {outcome}"
        
        self.memory_collection.add(
            ids=[interaction_id],
            documents=[record_text]
        )

    def perceive(self, user_message: str, user_tier: str = "standard") -> dict:
        """Paso 1: Captura de entrada + consulta a memoria de largo plazo."""
        past_context = self.recall_memories(user_message)
        return {
            "message": user_message,
            "user_tier": user_tier,
            "relevant_history": past_context
        }

    def reason(self, perception: dict) -> DecisionContext:
        """Paso 2: Cognición impulsada por Gemini."""
        prompt = f"""
        Eres un agente autónomo de soporte técnico.
        - Mensaje actual: {perception['message']}
        - Nivel de usuario: {perception['user_tier']}
        - Historial relevante recuperado: {perception['relevant_history']}

        Analiza la información y genera el contexto de decisión correspondiente.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DecisionContext,
                temperature=0.1,
            ),
        )
        return DecisionContext.model_validate_json(response.text)

    def act(self, decision: DecisionContext) -> dict:
        """Paso 3: Ejecución de acciones."""
        logs = [f"[EJECUTADO] {step}" for step in decision.action_plan]
        return {
            "status": "success",
            "strategy": decision.strategy,
            "execution_logs": logs
        }

    def run(self, user_message: str, interaction_id: str, user_tier: str = "standard") -> dict:
        """Bucle completo (Percepción -> Cognición -> Acción -> Memoria)."""
        perception = self.perceive(user_message, user_tier)
        decision = self.reason(perception)
        execution = self.act(decision)
        
        # Guardar episodio en memoria
        self.remember(user_message, execution["strategy"], interaction_id)

        return {
            "decision": decision.model_dump(),
            "execution": execution
        }