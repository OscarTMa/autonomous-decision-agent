import pytest
from unittest.mock import MagicMock, patch
from src.agent import AutonomousAgent, DecisionContext

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_test_key")

@patch("src.agent.genai.Client")
@patch("src.agent.chromadb.Client")
def test_agent_initialization(mock_chroma, mock_genai_client, mock_env):
    agent = AutonomousAgent()
    assert agent.model_name == "gemini-2.5-flash"
    mock_chroma.return_value.get_or_create_collection.assert_called_once_with(name="episodic_memory")

@patch("src.agent.genai.Client")
@patch("src.agent.chromadb.Client")
def test_reasoning_flow(mock_chroma, mock_genai_client, mock_env):
    # Mock de respuesta del LLM
    fake_json_response = """
    {
        "intent": "service_outage",
        "urgency": "ALTA",
        "strategy": "full_autonomous_resolution",
        "reasoning": "Fallo en el servicio reportado",
        "action_plan": ["Paso 1: Diagnosticar", "Paso 2: Enviar alerta"]
    }
    """
    mock_response = MagicMock()
    mock_response.text = fake_json_response
    
    instance = mock_genai_client.return_value
    instance.models.generate_content.return_value = mock_response

    agent = AutonomousAgent()
    perception = {"message": "Conexión caída", "user_tier": "premium", "relevant_history": []}
    
    decision = agent.reason(perception)
    
    assert isinstance(decision, DecisionContext)
    assert decision.intent == "service_outage"
    assert decision.urgency == "ALTA"
    assert len(decision.action_plan) == 2

def test_action_execution(mock_env):
    with patch("src.agent.genai.Client"), patch("src.agent.chromadb.Client"):
        agent = AutonomousAgent()
        decision = DecisionContext(
            intent="billing_issue",
            urgency="MEDIA",
            strategy="guided_resolution",
            reasoning="Aclaración de pago",
            action_plan=["Verificar factura", "Enviar recibo"]
        )
        
        result = agent.act(decision)
        assert result["status"] == "success"
        assert len(result["execution_logs"]) == 2
        assert "[EJECUTADO] Verificar factura" in result["execution_logs"][0]