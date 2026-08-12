# autonomous-decision-agent
# Autonomous Decision-Making Agent (Google Gemini)

Este repositorio contiene la implementación práctica del **Agente Autónomo de Toma de Decisiones** basado en la arquitectura cognitiva descrita en el Capítulo 5 de *30 Agents Every AI Engineer Must Build*.

El agente implementa el bucle continuo de **Percepción → Cognición → Acción**, utilizando modelos de la familia **Google Gemini** para la toma de decisiones estructurada.

## 🏗️ Arquitectura Cognitiva

1. **Percepción (`Perceive`)**: Captura el mensaje entrante del usuario y lo enriquece con metadatos del entorno (nivel de usuario, estado de servicios).
2. **Cognición (`Reason`)**: Procesa el contexto utilizando `gemini-2.5-flash` con garantías de salida JSON estrictas (`Pydantic`) para determinar la intención, urgencia y estrategia de resolución.
3. **Acción (`Act`)**: Ejecuta el plan de tareas generado por la fase de cognición.

## 🚀 Requisitos Previos

- Python 3.10+
- Una clave de API de Google AI Studio (`GEMINI_API_KEY`)

## 📦 Instalación

```bash
# 1. Clonar el repositorio
git clone [https://github.com/TU_USUARIO/autonomous-decision-agent.git](https://github.com/oscartma/autonomous-decision-agent.git)
cd autonomous-decision-agent

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita el archivo .env y agrega tu GEMINI_API_KEY
```

## 🛠️ Archivo `requirements.txt`

```text
google-genai>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

## 💻 Uso

Ejecuta el flujo principal con:

```bash
python main.py
```