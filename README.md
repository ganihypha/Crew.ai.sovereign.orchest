# Sovereign CrewAI - Autonomous Business Validation Agents

> The AI Brain behind the Sovereign Business Engine v3.0
> 8 agents, 3 validation layers, powered by Groq Llama 3.3 70B

## Quick Deploy to CrewAI AMP

1. Connect this repo at [app.crewai.com](https://app.crewai.com)
2. Set environment variable: `GROQ_API_KEY`
3. Click Deploy

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
| `GROQ_API_KEY` | Yes | Groq Console API key |
| `SERPER_API_KEY` | Optional | Web search capability |

## URLs

| Resource | URL |
|----------|-----|
| Sovereign Web | https://sovereign-orchestrator.pages.dev |
| CrewAI Studio | https://app.crewai.com/studio/v2/projects/1975e35d-5b36-4b73-a4c4-2d4d249a2905/editor |
| CrewAI AMP | https://app.crewai.com/crewai_plus/deployments/119445 |
| GitHub (Web) | https://github.com/ganihypha/Sovereign.private.real.busines.orchest |
| GitHub (CrewAI) | https://github.com/ganihypha/Crew.ai.sovereign.orchest |
