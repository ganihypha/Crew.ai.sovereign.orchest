# 🎯 MASTER SESSION HANDOFF #004 → #005
## SOVEREIGN BUSINESS ENGINE — Phase 4: CrewAI Python v4.0 Upgrade

**Session**: #004
**Status**: ⏳ PENDING — Dimulai Setelah Session #003 Complete
**Prerequisite**: Session #003 done (RAG memory working, OPENAI_API_KEY configured)
**Next Session Budget**: 100 credits

---

## ♾️ INFINITE GROWTH LOOP STATUS

```yaml
Session #4 Projection:
  Efficiency: 86%
  Knowledge: 1.45 (CrewAI Python + LangGraph synergy)
  Expected Output: ~100 × 0.86 × 1.45 = 124.7 effective credits

Prediction for Session #5:
  Efficiency: 88%
  Knowledge: 1.60 (Full-stack AI UI experience)
  Expected Output: ~100 × 0.88 × 1.60 = 140.8 effective credits
  Improvement: +13% vs Session #4!
```

---

## 📋 SESSION #004 GOALS (CrewAI Python Repo)

### Primary Objectives
1. **Clone CrewAI repo** `Crew.ai.sovereign.orchest`
2. **Add 4 new agents**: ChurnDetector, UpsellAdvisor, EngagementAnalyzer, CompetitorIntelAgent
3. **Add 4 new tasks** YAML untuk agents baru
4. **Update crew.py** dengan agents baru
5. **Test locally** dengan `crewai run`
6. **Push ke GitHub** CrewAI repo
7. **Trigger AMP re-deploy** (jika ada webhook)

### Success Criteria
- [ ] `crewai run` sukses tanpa error
- [ ] ChurnDetector bisa query Supabase
- [ ] UpsellAdvisor return rekomendasi JSON
- [ ] EngagementAnalyzer analyze Instagram metrics
- [ ] CompetitorIntelAgent return competitor data
- [ ] Push ke `ganihypha/Crew.ai.sovereign.orchest` sukses

---

## ✅ VERIFY SESSION #003 COMPLETE

```bash
# Check RAG endpoint di production
curl -s -X POST "https://sovereign-orchestrator.pages.dev/api/ai/rag/query" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"query":"test","limit":1}'
# Expected: {"success":true,"results":[...]}

# Check pricing endpoint
curl -s "https://sovereign-orchestrator.pages.dev/api/pricing/suggest/1" \
  -H "Authorization: Bearer <JWT>"
# Expected: {"success":true,"suggestion":{...}}
```

---

## ⚙️ SESSION #004 SETUP (CrewAI Python Repo)

```bash
# Clone CrewAI repo (BUKAN webapp!)
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Crew.ai.sovereign.orchest.git" crewai-sovereign
cd crewai-sovereign

# Install Python dependencies
pip install crewai crewai-tools langchain-community supabase python-dotenv

# Create .env file
cat > .env << 'EOF'
SUPABASE_URL=https://lfohzibcsafqthupcvdg.supabase.co
SUPABASE_SERVICE_KEY=<SUPABASE_SERVICE_KEY>
OPENAI_API_KEY=<PASTE_OPENAI_KEY_HERE>
LANGCHAIN_API_KEY=<LANGCHAIN_API_KEY>
CREWAI_ORG_ID=9878e40e-ad44-45e2-8d29-da0b3ee92511
FONNTE_TOKEN=<PASTE_FONNTE_TOKEN_HERE>
SERPAPI_KEY=<SERPAPI_KEY>
EOF

# Check current structure
ls src/sovereign_crew/
```

---

## 🛠️ TASK BREAKDOWN SESSION #004

### Task 1 — Review Current CrewAI Structure [~5 credits]

```bash
# Check existing files
cat src/sovereign_crew/crew.py
cat src/sovereign_crew/config/agents.yaml
cat src/sovereign_crew/config/tasks.yaml
```

---

### Task 2 — Add New Agents YAML [~20 credits]

Tambahkan ke `src/sovereign_crew/config/agents.yaml`:

```yaml
# ================================
# NEW AGENTS v4.0 — Added Session #004
# ================================

churn_detector:
  role: "Customer Retention Specialist"
  goal: >
    Detect customers at risk of churning based on purchase patterns,
    last order date, and engagement metrics. Alert founder before churn happens.
  backstory: >
    Kamu adalah retention specialist berpengalaman yang bisa membaca sinyal
    churn dari data. Kamu membantu bisnis fashion Indonesia mempertahankan pelanggan
    terbaik mereka dengan deteksi dini dan action plan yang konkret.
  llm: openai/gpt-4o-mini
  tools:
    - supabase_tool
    - fonnte_tool
  verbose: true
  memory: true
  allow_delegation: false

upsell_advisor:
  role: "Revenue Growth Optimizer"
  goal: >
    Identify upsell and cross-sell opportunities based on customer purchase history.
    Suggest the right products to existing customers to maximize CLV (Customer Lifetime Value).
  backstory: >
    Kamu adalah growth advisor yang memahami psikologi pembeli fashion Indonesia.
    Kamu menganalisis pola pembelian dan merekomendasikan produk yang paling likely
    dibeli next, menggunakan data real dari Supabase.
  llm: openai/gpt-4o-mini
  tools:
    - supabase_tool
  verbose: true
  memory: true
  allow_delegation: false

engagement_analyzer:
  role: "Instagram Engagement Intelligence Analyst"
  goal: >
    Analyze Instagram engagement metrics across all three brand accounts.
    Identify top-performing content types, optimal posting times, and engagement trends.
  backstory: >
    Kamu ahli dalam menganalisis data Instagram untuk bisnis fashion Indonesia.
    Kamu membantu @fashionkas.official, @resellerkas.official, dan @haidar_faras_m
    memaksimalkan reach dan engagement dengan insight berbasis data.
  llm: openai/gpt-4o-mini
  tools:
    - supabase_tool
    - sovereign_api_tool
  verbose: true
  memory: false
  allow_delegation: false

competitor_intel_agent:
  role: "Competitive Intelligence Researcher"
  goal: >
    Research competitor pricing, product range, and market positioning.
    Provide actionable intelligence to maintain competitive advantage.
  backstory: >
    Kamu adalah peneliti kompetitif yang memantau pasar fashion reseller Indonesia.
    Kamu mengumpulkan dan menganalisis data kompetitor dari berbagai sumber untuk
    memberikan keunggulan kompetitif kepada bisnis FashionKas.
  llm: openai/gpt-4o-mini
  tools:
    - sovereign_api_tool
    - supabase_tool
  verbose: true
  memory: true
  allow_delegation: false
```

---

### Task 3 — Add New Tasks YAML [~20 credits]

Tambahkan ke `src/sovereign_crew/config/tasks.yaml`:

```yaml
# ================================
# NEW TASKS v4.0 — Added Session #004
# ================================

detect_churn_task:
  description: >
    Query Supabase untuk mencari customers yang:
    1. Last order > 30 hari yang lalu
    2. Pernah order 3+ kali sebelumnya (loyal customers)
    3. Tidak ada recent engagement
    
    Untuk setiap customer at-risk, buat churn risk score (0-100) dan
    rekomendasi retention action (WhatsApp message, special offer, etc).
    
    Return JSON: {{ "churn_risks": [{{ "customer_id": ..., "name": ..., 
    "last_order_days_ago": ..., "churn_risk_score": ..., 
    "recommended_action": ... }}] }}
  expected_output: >
    JSON object dengan array "churn_risks" berisi customers berisiko churn,
    masing-masing dengan churn_risk_score dan recommended_action yang spesifik.
  agent: churn_detector

identify_upsell_opportunities_task:
  description: >
    Analisis purchase history untuk semua customers dalam 90 hari terakhir.
    Temukan pola: produk apa yang sering dibeli bersama? Customer mana yang
    suka kategori tertentu? Siapa yang sudah lama tidak order produk favoritnya?
    
    Buat list top 10 upsell opportunities dengan:
    - Customer name & ID
    - Suggested product(s)
    - Reasoning berdasarkan data
    - Probability of success (0-1)
    - Suggested WhatsApp message template
  expected_output: >
    JSON dengan top 10 upsell opportunities, masing-masing lengkap dengan
    customer info, product suggestion, reasoning, success probability, dan WA template.
  agent: upsell_advisor

analyze_instagram_engagement_task:
  description: >
    Analisis data engagement Instagram dari tabel analytics_metrics dan leads.
    
    Hitung:
    1. Average engagement rate per brand account
    2. Top content types (video vs foto, produk vs lifestyle)
    3. Best posting days/times berdasarkan data histori
    4. Followers quality score (engagement/followers ratio)
    5. Trend: naik atau turun 30 hari terakhir
    
    Bandingkan ketiga akun: @fashionkas.official, @resellerkas.official, @haidar_faras_m
  expected_output: >
    Laporan engagement analysis dalam format Markdown dengan tabel perbandingan
    ketiga akun, insight actionable, dan 3 rekomendasi spesifik untuk meningkatkan
    engagement dalam 2 minggu ke depan.
  agent: engagement_analyzer

research_competitor_intel_task:
  description: >
    Research kompetitor fashion reseller Indonesia, fokus pada:
    1. Kisaran harga untuk kategori yang sama (hijab, dress, outer)
    2. Strategi promosi yang sedang digunakan
    3. Kualitas engagement rate vs FashionKas
    4. Gap opportunities: apa yang kompetitor tidak offer tapi market butuhkan?
    
    Sources: SerpAPI search, data dari tabel competitor_intel di Supabase.
    Jika tabel competitor_intel kosong, lakukan research fresh.
  expected_output: >
    Laporan competitor intelligence dalam format Markdown berisi:
    - Competitor comparison table (nama, harga range, strengths, weaknesses)
    - 3 market opportunities yang belum dimanfaatkan kompetitor
    - Pricing recommendation untuk FashionKas berdasarkan competitive landscape
    - Action items untuk founder dalam 1 minggu
  agent: competitor_intel_agent
```

---

### Task 4 — Update crew.py [~25 credits]

Update `src/sovereign_crew/crew.py` untuk menambahkan agents dan tasks baru:

```python
# src/sovereign_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools import SupabaseQueryTool, FonnteSendTool, FonnteStatusTool, SovereignAPITool
import os

@CrewBase
class SovereignValidationCrew:
    """Sovereign Business Engine v4.0 - 21-Agent Autonomous Brain"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.supabase_tool = SupabaseQueryTool()
        self.fonnte_tool = FonnteSendTool()
        self.fonnte_status_tool = FonnteStatusTool()
        self.sovereign_api_tool = SovereignAPITool()

    # ============ ORIGINAL AGENTS ============

    @agent
    def market_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['market_validator'],
            tools=[self.supabase_tool],
            verbose=True
        )

    @agent
    def lead_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_researcher'],
            tools=[self.supabase_tool, self.sovereign_api_tool],
            verbose=True
        )

    @agent
    def revenue_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['revenue_analyst'],
            tools=[self.supabase_tool],
            verbose=True
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],
            tools=[self.supabase_tool, self.sovereign_api_tool],
            verbose=True
        )

    # ============ NEW v4.0 AGENTS ============

    @agent
    def churn_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['churn_detector'],
            tools=[self.supabase_tool, self.fonnte_tool],
            verbose=True,
            memory=True
        )

    @agent
    def upsell_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['upsell_advisor'],
            tools=[self.supabase_tool],
            verbose=True,
            memory=True
        )

    @agent
    def engagement_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['engagement_analyzer'],
            tools=[self.supabase_tool, self.sovereign_api_tool],
            verbose=True
        )

    @agent
    def competitor_intel_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['competitor_intel_agent'],
            tools=[self.sovereign_api_tool, self.supabase_tool],
            verbose=True,
            memory=True
        )

    # ============ ORIGINAL TASKS ============

    @task
    def validate_market_task(self) -> Task:
        return Task(config=self.tasks_config['validate_market'])

    @task
    def research_leads_task(self) -> Task:
        return Task(config=self.tasks_config['research_leads'])

    @task
    def analyze_revenue_task(self) -> Task:
        return Task(config=self.tasks_config['analyze_revenue'])

    @task
    def create_content_strategy_task(self) -> Task:
        return Task(config=self.tasks_config['create_content_strategy'])

    # ============ NEW v4.0 TASKS ============

    @task
    def detect_churn_task(self) -> Task:
        return Task(config=self.tasks_config['detect_churn_task'])

    @task
    def identify_upsell_opportunities_task(self) -> Task:
        return Task(config=self.tasks_config['identify_upsell_opportunities_task'])

    @task
    def analyze_instagram_engagement_task(self) -> Task:
        return Task(config=self.tasks_config['analyze_instagram_engagement_task'])

    @task
    def research_competitor_intel_task(self) -> Task:
        return Task(config=self.tasks_config['research_competitor_intel_task'])

    # ============ CREW DEFINITIONS ============

    @crew
    def crew(self) -> Crew:
        """Main Sovereign Validation Crew - runs all agents"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=True
        )

    def run_churn_analysis(self) -> dict:
        """Run only churn detection crew"""
        churn_crew = Crew(
            agents=[self.churn_detector()],
            tasks=[self.detect_churn_task()],
            process=Process.sequential,
            verbose=True
        )
        return churn_crew.kickoff()

    def run_upsell_analysis(self) -> dict:
        """Run only upsell advisor crew"""
        upsell_crew = Crew(
            agents=[self.upsell_advisor()],
            tasks=[self.identify_upsell_opportunities_task()],
            process=Process.sequential,
            verbose=True
        )
        return upsell_crew.kickoff()

    def run_engagement_analysis(self) -> dict:
        """Run only engagement analysis crew"""
        engagement_crew = Crew(
            agents=[self.engagement_analyzer()],
            tasks=[self.analyze_instagram_engagement_task()],
            process=Process.sequential,
            verbose=True
        )
        return engagement_crew.kickoff()

    def run_competitor_intel(self) -> dict:
        """Run only competitor intelligence crew"""
        competitor_crew = Crew(
            agents=[self.competitor_intel_agent()],
            tasks=[self.research_competitor_intel_task()],
            process=Process.sequential,
            verbose=True
        )
        return competitor_crew.kickoff()
```

---

### Task 5 — Add Crew Endpoints to Webapp [~15 credits]

Di `src/routes/crewai.ts`, tambahkan endpoints baru:

```typescript
// POST /api/ai/crew/churn-analysis
router.post('/crew/churn-analysis', jwtMiddleware, async (c) => {
  try {
    const response = await fetch(`${c.env.CREWAI_AMP_URL}/kickoff`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${c.env.CREWAI_AMP_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        inputs: {
          crew_type: 'churn_analysis',
          supabase_url: c.env.SUPABASE_URL,
          timestamp: new Date().toISOString()
        }
      })
    })
    const data = await response.json() as any
    return c.json({ success: true, task_id: data.kickoff_id, status: 'running' })
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500)
  }
})

// POST /api/ai/crew/upsell-analysis
router.post('/crew/upsell-analysis', jwtMiddleware, async (c) => {
  try {
    const response = await fetch(`${c.env.CREWAI_AMP_URL}/kickoff`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${c.env.CREWAI_AMP_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        inputs: { crew_type: 'upsell_analysis', timestamp: new Date().toISOString() }
      })
    })
    const data = await response.json() as any
    return c.json({ success: true, task_id: data.kickoff_id, status: 'running' })
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500)
  }
})
```

---

### Task 6 — Test & Deploy [~10 credits]

```bash
# Test CrewAI locally
cd /home/user/crewai-sovereign
crewai run  # Should run all tasks

# Push to CrewAI repo
git add -A
git commit -m "feat: v4.0 - Add 4 new agents (churn, upsell, engagement, competitor)

New agents:
- ChurnDetector: identifies at-risk customers
- UpsellAdvisor: finds cross-sell opportunities
- EngagementAnalyzer: Instagram metrics analysis
- CompetitorIntelAgent: competitive landscape research

Updated crew.py with run_*_analysis() helper methods
Version: v4.0"
git push origin main

# Update webapp version
cd /home/user/webapp
# Edit src/index.tsx version to "4.0"
npm run build
npx wrangler pages deploy dist --project-name sovereign-orchestrator
git add -A && git commit -m "feat: webapp v4.0 - CrewAI AMP new crew endpoints"
git push origin main
```

---

## 📊 WHAT SHOULD BE DELIVERED

```yaml
New CrewAI Agents (Python):
  ChurnDetector: ✅
  UpsellAdvisor: ✅
  EngagementAnalyzer: ✅
  CompetitorIntelAgent: ✅

New API Endpoints (Webapp):
  POST /api/ai/crew/churn-analysis: ✅
  POST /api/ai/crew/upsell-analysis: ✅

Repos Updated:
  Crew.ai.sovereign.orchest: ✅ v4.0 pushed
  Sovereign.private.real.busines.orchest: ✅ v4.0 pushed

Deployed:
  sovereign-orchestrator.pages.dev: ✅ v4.0 live
```

---

## ⚠️ CRITICAL NOTES

1. **CrewAI AMP vs Local**: Session #004 fokus update Python files di repo. AMP deployment otomatis dari GitHub push (jika terhubung) atau manual re-deploy.

2. **Memory**: Agents dengan `memory=True` butuh storage. Default CrewAI pakai in-memory. Untuk production, perlu custom memory backend (Supabase/SQLite).

3. **API Cost**: Setiap crew run memanggil OpenAI. Estimasi: 1 full crew run ≈ $0.05-0.15 tergantung task complexity.

---

## 💡 NOTES FOR SESSION #005

Session #005 fokus ke **AI Intelligence UI page** di frontend.
Akan menampilkan semua agent status, results, dan task queue.

**Prerequisites untuk Session #005:**
- [ ] Session #004 complete (4 new agents ready)
- [ ] CrewAI AMP responding ke kickoff calls

---

## 🎉 FILL THIS AFTER SESSION #004 COMPLETE

```
SESSION #004 ACTUAL RESULTS:
  Credits Used: __ credits (estimate: 95-109)
  Duration: __ minutes
  
DELIVERABLES:
  ChurnDetector agent: [✅/❌]
  UpsellAdvisor agent: [✅/❌]
  EngagementAnalyzer agent: [✅/❌]
  CompetitorIntelAgent agent: [✅/❌]
  New crew endpoints: [✅/❌]
  Deployed: [✅/❌]
  
BLOCKERS: [describe]
NOTES FOR SESSION #005: [context]

PRODUCTION HEALTH:
  https://sovereign-orchestrator.pages.dev/api/health → Version: v4.0
```

---

*Session Handoff #004 | Sovereign Business Engine | CONFIDENTIAL | Haidar Faras*
