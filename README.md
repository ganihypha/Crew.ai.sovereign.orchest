# Sovereign CrewAI - Autonomous Business Validation Agents

> The AI Brain behind the Sovereign Business Engine v3.0
> 8 agents, 3 validation layers, powered by Groq Llama 3.3 70B

## Quick Deploy to CrewAI AMP

1. Connect this repo at [app.crewai.com](https://app.crewai.com)
2. Set environment variables:
   - `GROQ_API_KEY` (required) - from [Groq Console](https://console.groq.com)
   - `SERPER_API_KEY` (optional) - for web search tools
3. Click Deploy

## What Was Fixed (v3.2.0)

### Root Cause Analysis
The deployment was failing with `CrashLoopBackOff` (exit code 10) due to:

1. **Missing `crewai-tools` dependency**: `crewai[tools]` extras did NOT auto-install `crewai-tools` package in CrewAI AMP's `uv` environment. The `from crewai_tools import SerperDevTool` import in `crew.py` would crash during AMP's "Testing automation..." phase.

2. **Missing `litellm` dependency**: CrewAI 1.12.2 requires `litellm` for non-native LLM providers (like Groq). Without it, agent initialization fails with `ImportError: model did not match any supported native provider`.

3. **Unnecessary `langchain-groq`**: Was listed as dependency but not used - CrewAI routes Groq through LiteLLM, not LangChain.

### Fix Applied
```toml
# BEFORE (broken)
dependencies = [
    "crewai[tools]>=0.102.0",
    "langchain-groq>=0.3.0",
]

# AFTER (fixed)
dependencies = [
    "crewai[tools,litellm]>=1.12.0,<2.0.0",
    "crewai-tools>=1.12.0,<2.0.0",
]
```

## Architecture

```
CrewAI AMP (This Repo)          Sovereign Web (Dashboard)
========================        ========================
8 AI Agents                     API Gateway (Hono.js)
  - demand_analyst               /api/ai/crew/kickoff
  - revenue_tracker              /api/ai/crew/status
  - lead_scout                   /api/ai/insights
  - system_validator             /api/ai/webhook
  - closer_agent
  - trust_auditor              Supabase (Database)
  - content_strategist           8 tables, 14 indexes
  - sovereign_orchestrator       Products, Orders, Leads
```

## Agents

| Agent | Layer | LLM |
|-------|-------|-----|
| demand_analyst | Demand | groq/llama-3.3-70b |
| revenue_tracker | Demand | groq/llama-3.3-70b |
| lead_scout | System | groq/llama-3.3-70b |
| system_validator | System | groq/llama-3.3-70b |
| closer_agent | System | groq/llama-3.3-70b |
| trust_auditor | Trust | groq/llama-3.3-70b |
| content_strategist | Trust | groq/llama-3.3-70b |
| sovereign_orchestrator | Meta | groq/llama-3.3-70b |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | **Yes** | Groq Console API key |
| `SERPER_API_KEY` | Optional | Web search capability |

## Project Structure (CrewAI AMP Compatible)

```
sovereign-crewai/
├── pyproject.toml                        # [tool.crewai] type = "crew"
├── uv.lock                              # Required for AMP deployment
├── src/
│   └── sovereign_crewai/
│       ├── __init__.py
│       ├── main.py                      # Entry point: run()
│       ├── crew.py                      # @CrewBase class
│       ├── config/
│       │   ├── agents.yaml              # 8 agent definitions
│       │   └── tasks.yaml               # 8 task definitions
│       ├── knowledge/                   # AI Knowledge Base
│       │   ├── sovereign_engine_overview.md
│       │   ├── demand_validation_sop.md
│       │   ├── system_validation_sop.md
│       │   ├── trust_validation_sop.md
│       │   └── outreach_templates.md
│       └── tools/
│           └── __init__.py
└── README.md
```

## URLs

| Resource | URL |
|----------|-----|
| Sovereign Web | https://sovereign-orchestrator.pages.dev |
| CrewAI Studio | https://app.crewai.com/studio/v2/projects/1975e35d-5b36-4b73-a4c4-2d4d249a2905/editor |
| CrewAI AMP | https://app.crewai.com/crewai_plus/deployments/119445 |
| GitHub (Web) | https://github.com/ganihypha/Sovereign.private.real.busines.orchest |
| GitHub (CrewAI) | https://github.com/ganihypha/Crew.ai.sovereign.orchest |
