# Sovereign CrewAI - Autonomous Business Validation Agents

> **The AI Brain** behind the Sovereign Business Engine v3.0
> 8 specialized agents across 3 validation layers, powered by CrewAI.

## Architecture

```
+----------------------------------------------------------+
|              SOVEREIGN ECOSYSTEM                          |
+----------------------------------------------------------+
|                                                           |
|  [CrewAI Studio]  -->  [CrewAI AMP]  <-->  [Sovereign Web]
|  (Design & Test)      (Deploy & Run)      (Monitor & Control)
|                                                           |
|  Agents:                                                  |
|  Layer 1 (Demand):  demand_analyst, revenue_tracker       |
|  Layer 2 (System):  lead_scout, system_validator, closer  |
|  Layer 3 (Trust):   trust_auditor, content_strategist     |
|  Meta:              sovereign_orchestrator                |
|                                                           |
+----------------------------------------------------------+
```

## Integration Flow

```
Sovereign Web Dashboard
  |
  | POST /api/ai/crew/kickoff
  v
CrewAI AMP (API Endpoint)
  |
  | Execute crew with inputs
  v
8 AI Agents (via LLM)
  |
  | Query/Write
  v
Supabase Database  +  External APIs (Fonnte, ScraperAPI)
  |
  | Webhook / API response
  v
Sovereign Web Dashboard (results displayed)
```

## Project Structure

```
sovereign-crewai/
|-- main.py                         # Entry point
|-- requirements.txt                # Python dependencies
|-- pyproject.toml                  # Project metadata
|-- .env.example                    # Environment variables template
|-- .gitignore
|
|-- config/
|   |-- agents.yaml                 # 8 agent definitions
|   |-- tasks.yaml                  # 8 task definitions
|
|-- knowledge/                      # AI Knowledge Base (SOP)
|   |-- sovereign_engine_overview.md    # Full engine documentation
|   |-- demand_validation_sop.md        # Layer 1 rules & thresholds
|   |-- system_validation_sop.md        # Layer 2 rules & thresholds
|   |-- trust_validation_sop.md         # Layer 3 rules & thresholds
|   |-- outreach_templates.md           # WhatsApp message templates
|
|-- src/
|   |-- sovereign_crew/
|       |-- __init__.py
|       |-- crew.py                 # Main crew definition
|
|-- tools/                          # Custom CrewAI tools
|   |-- __init__.py
|   |-- supabase_tool.py           # Supabase database queries
|   |-- fonnte_tool.py             # WhatsApp send & status
|   |-- sovereign_api_tool.py      # Sovereign Web API interaction
|
|-- tests/
    |-- (test files)
```

## Agents

| # | Agent | Layer | Role |
|---|-------|-------|------|
| 1 | `demand_analyst` | Demand | Analyze product-market fit data |
| 2 | `revenue_tracker` | Demand | Monitor revenue streams |
| 3 | `lead_scout` | System | Discover & score Instagram leads |
| 4 | `system_validator` | System | Validate automation health |
| 5 | `closer_agent` | System | Compose WhatsApp outreach |
| 6 | `trust_auditor` | Trust | Audit brand authority |
| 7 | `content_strategist` | Trust | Plan Instagram content |
| 8 | `sovereign_orchestrator` | Meta | Coordinate all layers |

## Tasks

| Task | Agent | Output |
|------|-------|--------|
| `analyze_demand` | demand_analyst | Demand score + evidence |
| `track_revenue` | revenue_tracker | Revenue intelligence report |
| `scout_leads` | lead_scout | New leads + scores |
| `validate_system` | system_validator | System health report |
| `compose_outreach` | closer_agent | Personalized WA messages |
| `audit_trust` | trust_auditor | Trust score + social proof |
| `plan_content` | content_strategist | 7-day content calendar |
| `generate_validation_report` | sovereign_orchestrator | Unified validation report |

## Knowledge Base

The `knowledge/` folder is the AI's "brain" - it contains SOPs and rules:

- **sovereign_engine_overview.md** - Full business context, schema, metrics
- **demand_validation_sop.md** - Scoring algorithm, thresholds, queries
- **system_validation_sop.md** - System health checks, conversion funnel
- **trust_validation_sop.md** - Trust scoring, content calendar rules
- **outreach_templates.md** - WhatsApp templates Day 0/3/7/14

## Setup

### 1. Clone & Install
```bash
git clone https://github.com/ganihypha/Crew.ai.sovereign.orchest.git
cd Crew.ai.sovereign.orchest
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 3. Run Locally
```bash
# Full validation run
python main.py

# Single layer
python main.py --layer demand
python main.py --layer system
python main.py --layer trust

# Dry run (config check)
python main.py --dry-run
```

### 4. Deploy to CrewAI AMP
1. Go to [app.crewai.com](https://app.crewai.com)
2. Connect this GitHub repository
3. Set environment variables (from .env.example)
4. Click Deploy
5. Get your API endpoint + Bearer token

### 5. Connect to Sovereign Web
Use the AMP API endpoint in your Sovereign Web:
```
POST https://your-amp-endpoint.crewai.com/kickoff
Authorization: Bearer <your-amp-token>
Content-Type: application/json

{
  "crew_name": "SovereignValidationCrew",
  "inputs": {
    "total_products": 8,
    "target_platform": "instagram",
    "min_lead_score": 70,
    "outreach_day": 0
  }
}
```

## CrewAI Studio Project
- Studio URL: https://app.crewai.com/studio/v2/projects/1975e35d-5b36-4b73-a4c4-2d4d249a2905/editor
- Import this repo's config/ files into Studio for visual editing

## Connected Services

| Service | Purpose | Status |
|---------|---------|--------|
| Sovereign Web | Dashboard & monitoring | LIVE |
| Supabase | Database (8 tables) | LIVE |
| Fonnte API | WhatsApp messaging | PENDING |
| ScraperAPI | Instagram scraping | CONFIGURED |
| SerpAPI | Web search | CONFIGURED |
| OpenAI | LLM (GPT-4o-mini) | CONFIGURED |

## URLs

| Resource | URL |
|----------|-----|
| Sovereign Web | https://sovereign-orchestrator.pages.dev |
| CrewAI Studio | https://app.crewai.com/studio/v2/projects/1975e35d-5b36-4b73-a4c4-2d4d249a2905/editor |
| GitHub (Web) | https://github.com/ganihypha/Sovereign.private.real.busines.orchest |
| GitHub (CrewAI) | https://github.com/ganihypha/Crew.ai.sovereign.orchest |
| Supabase | https://lfohzibcsafqthupcvdg.supabase.co |

## License
Private & Confidential - Founder Access Only
