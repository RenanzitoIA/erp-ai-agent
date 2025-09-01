# Arquitetura

```mermaid
flowchart TD
  ERP[(ERP System)] -- Webhooks --> N8N
  N8N -- HTTP --> PY[Python API (FastAPI)]
  PY -- /forecast --> R[Plumber (R Analytics)]
  PY -- LLM --> HF[Hugging Face Models]
  PY -- Notify --> Slack[Slack]
  R --> Dash[Dashboards]
```
