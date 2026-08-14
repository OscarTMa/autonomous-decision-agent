## Architecture Overview

The system models autonomous behavior through a cyclic cognitive loop. Rather than treating queries as stateless text exchanges, the agent captures contextual signals, retrieves relevant historical embeddings, performs constrained reasoning via schema-enforced JSON generation, executes targeted actions, and indexes the outcome for long-term memory continuity.

### Cognitive Loop Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as Client / User
    participant Perc as Perception Layer
    participant Chroma as Episodic Memory (ChromaDB)
    participant Core as Cognitive Engine (Gemini 2.5)
    participant Act as Action Execution Engine

    User->>Perc: Dispatch message + context metadata
    Perc->>Chroma: Vector similarity search (Query embedding)
    Chroma-->>Perc: Return k-nearest episodic interactions
    Perc->>Core: Forward enriched payload (State + History + Schema)
    Note over Core: Pydantic constrained inference<br/>(Deterministic JSON schema)
    Core-->>Act: Output DecisionContext (Intent, Strategy, Plan)
    Act->>Act: Dispatch action plan execution pipeline
    Act->>Chroma: Ingest episode (Interaction text + Vector embedding)
    Act-->>User: Return structured execution telemetry
```

---

## Core Cognitive Primitives

```mermaid
flowchart LR
    subgraph Perception [1. Perception]
        direction TB
        RAW[User Input] --> NORM[Context Enrichment]
        HIST[(Episodic Memory)] -.->|Recall| NORM
    end

    subgraph Cognition [2. Cognition]
        direction TB
        NORM --> PROMPT[Contextual Prompt Builder]
        PROMPT --> LLM[Google Gemini 2.5 Flash]
        LLM --> SCHEMA[Pydantic Schema Validation]
    end

    subgraph Action [3. Action & Feedback]
        direction TB
        SCHEMA --> PLAN[Action Plan Pipeline]
        PLAN --> EXEC[Tool / Mock Execution]
        EXEC --> STORE[(Memory Ingestion)]
    end

    Perception --> Cognition --> Action
```
