# SOVEREIGN BUSINESS ENGINE
# MASTER SESSION HANDOFF DOCUMENT
### Classification: CONFIDENTIAL | Founder Access Only
### Generated: 2026-04-01 | For: Claude Sonnet (claude.ai) / Genspark AI

---

## 🧠 KONTEKS WAJIB DIBACA SEBELUM MULAI SETIAP SESSION

Ini adalah **private AI-powered business orchestration platform** untuk Haidar Faras.
Platform ini menggabungkan Hono.js (Cloudflare Workers), LangGraph.js, CrewAI AMP, dan Supabase.

**JANGAN BUAT APP BARU. LANJUTKAN DARI REPO YANG SUDAH ADA.**

---

## ⚙️ SETUP WAJIB SETIAP SESSION BARU

```bash
# 1. Clone repo main
git clone https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git webapp
cd webapp && npm install

# 2. Setup Cloudflare credentials
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"
echo "export CLOUDFLARE_API_TOKEN=\"<CF_API_TOKEN>\"" >> ~/.bashrc
echo "export CLOUDFLARE_ACCOUNT_ID=\"618d52f63c689422eacf6638436c3e8b\"" >> ~/.bashrc

# 3. Buat .dev.vars (JANGAN commit file ini)
cat > .dev.vars << 'EOF'
SUPABASE_URL=https://lfohzibcsafqthupcvdg.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxmb2h6aWJjc2FmcXRodXBjdmRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4Nzg4NzIsImV4cCI6MjA5MDQ1NDg3Mn0.0lLWyuT6qh5dib0KfN7aTcQ1WmBoKLj3xIsBaWcaVEE
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxmb2h6aWJjc2FmcXRodXBjdmRnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDg3ODg3MiwiZXhwIjoyMDkwNDU0ODcyfQ.tiJEtJLqtJfsUirArdrsVW5KUO1DjQ0xnKXaRTa90x4
JWT_SECRET=cCZ/O5whNhPyoiyZKZ7fowEalGrGpNXmlLC+MoYNrpvpK6weEWgyz5ADepILzQrc4DmyT+xVz7d6PR3JHBpuVw==
MASTER_PIN=1945
SCRAPER_API_KEY=<SCRAPER_API_KEY>
LANGCHAIN_API_KEY=<LANGCHAIN_PAT_KEY>
LANGCHAIN_SERVICE_KEY=<LANGCHAIN_SERVICE_KEY>
CREWAI_ORG_ID=9878e40e-ad44-45e2-8d29-da0b3ee92511
CREWAI_PAT=<CREWAI_PAT>
CREWAI_ENTERPRISE_TOKEN=<CREWAI_ENTERPRISE_TOKEN>
CREWAI_AMP_URL=https://crew-ai-sovereign-orchest-ef50eb91-6c9d-4fc-f916c3e6.crewai.com
CREWAI_AMP_TOKEN=<CREWAI_AMP_TOKEN>
SERPAPI_KEY=<SERPAPI_KEY>
GROQ_API_KEY=<GROQ_API_KEY>
FONNTE_TOKEN=<PASTE_FONNTE_TOKEN_HERE>
OPENAI_API_KEY=<PASTE_OPENAI_KEY_HERE>
EOF

# 4. Build & start local
npm run build
pm2 start ecosystem.config.cjs

# 5. Verify
curl http://localhost:3000/api/health
```

---

## 📊 ESTIMASI CREDIT/TOKEN PER SESSION (Claude Sonnet)

**Basis Estimasi:**
- 1 "session" = 1 percakapan Claude Sonnet dengan context window penuh
- Budget per session: ~100.000 tokens input + output
- Claude Sonnet harga: ~$3/1M input, ~$15/1M output
- Estimasi cost Claude: **~$0.5-1.5 per session** (tergantung file size & complexity)

**Untuk Genspark AI:**
- Budget per session: ~109 credits
- 1 credit ≈ ~1 tool call atau ~500 tokens
- Estimasi per session: **80-109 credits consumed**

### Context yang dibawa tiap session:
| Item | Est. Tokens |
|------|------------|
| Dokumen ini (handoff) | ~3.000 |
| CURRENT-STATE.md | ~4.000 |
| Kode src/index.tsx | ~2.500 |
| Kode route yang relevan (1-2 file) | ~3.000 |
| Build output info | ~500 |
| **Total konteks per session** | **~13.000 tokens** |

---

## 🗓️ BREAKDOWN SESSIONS (8 Sessions Total)

---

### ═══════════════════════════════════════
### SESSION 1 — Foundation DB & Fonnte Setup
### ═══════════════════════════════════════

**Estimasi durasi**: 45-60 menit
**Estimasi credit**: 80-95 credits / ~60K tokens
**Prerequisites**:
- [ ] Fonnte token sudah didapat dari fonnte.com (jika belum, skip Fonnte tasks)

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Kamu adalah developer yang melanjutkan project Sovereign Business Engine v3.2.
Project ini sudah LIVE di https://sovereign-orchestrator.pages.dev

Setup session dulu:
1. Clone repo: git clone https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git webapp
2. cd webapp && npm install
3. Buat .dev.vars dengan credentials dari SESSION-HANDOFF-MASTER.md
4. npm run build && pm2 start ecosystem.config.cjs

TUGAS SESSION INI:
Task 1: Buat 4 tabel baru di Supabase via REST API (gunakan SUPABASE_SERVICE_KEY):
- wa_logs: id, lead_id, phone, direction, message_type, message, fonnte_response, status, sent_at, created_at
- ai_tasks: id, agent_type, task_type, crew_name, input_data (jsonb), output_data (jsonb), status (pending/running/completed/failed), started_at, completed_at, created_at
- ai_insights: id, layer (demand/system/trust/general), insight_type, title, content, confidence, actionable (bool), created_at
- order_items: id, order_id (FK→orders), product_id (FK→products), qty, unit_price, subtotal, created_at

Task 2: Update route /api/dashboard/ai-insights untuk query ai_insights table
Task 3: Update route /api/ai/tasks untuk CRUD ai_tasks table
Task 4: Jika Fonnte token sudah ada → Test POST /api/wa/send dengan token

Setelah selesai:
- npm run build
- Deploy: npx wrangler pages deploy dist --project-name sovereign-orchestrator
- git add -A && git commit -m "feat: Phase 1 - Foundation DB tables + Fonnte ready"
- git push origin main

JANGAN buat app baru. JANGAN ubah UI yang sudah ada. Fokus backend only.
```

**Deliverables Session 1:**
- [ ] 4 tabel baru created di Supabase
- [ ] /api/dashboard/ai-insights returns data from table
- [ ] /api/ai/tasks CRUD berfungsi
- [ ] Fonnte test (jika token ada)
- [ ] Deployed ke production

---

### ═══════════════════════════════════════
### SESSION 2 — pgvector + v4.0 DB Schema
### ═══════════════════════════════════════

**Estimasi durasi**: 45-60 menit
**Estimasi credit**: 85-100 credits
**Prerequisites**:
- [ ] Session 1 selesai
- [ ] OpenAI API Key sudah ada (untuk embeddings)

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine v3.2. Session 1 sudah selesai (4 tabel baru ada).

Setup: clone repo, npm install, buat .dev.vars, npm run build, pm2 start

TUGAS SESSION INI (v4.0 Database Infrastructure):

Task 1: Enable pgvector di Supabase
- Execute di Supabase SQL Editor: CREATE EXTENSION IF NOT EXISTS vector;

Task 2: Buat 5 tabel v4.0 baru:

-- embeddings table (LangChain RAG memory)
CREATE TABLE embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL,
  embedding vector(1536),
  metadata jsonb,
  created_at timestamptz DEFAULT timezone('utc', now())
);
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);

-- agent_memory (short-term state cache)
CREATE TABLE agent_memory (
  session_id text PRIMARY KEY,
  framework varchar(50),
  state_json jsonb,
  updated_at timestamptz DEFAULT timezone('utc', now())
);

-- agent_handoffs (inter-framework message bus)
CREATE TABLE agent_handoffs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_agent varchar(100),
  target_agent varchar(100),
  payload jsonb,
  status varchar(20) DEFAULT 'pending',
  created_at timestamptz DEFAULT timezone('utc', now())
);

-- pricing_history
CREATE TABLE pricing_history (
  id serial PRIMARY KEY,
  product_id int REFERENCES products(id),
  old_price numeric,
  new_price numeric,
  ai_reasoning text,
  created_at timestamptz DEFAULT timezone('utc', now())
);

-- competitor_intel
CREATE TABLE competitor_intel (
  id serial PRIMARY KEY,
  source varchar(100),
  data jsonb,
  scraped_at timestamptz DEFAULT timezone('utc', now())
);

-- match_documents SQL function untuk pgvector similarity search
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_count int,
  filter jsonb DEFAULT '{}'
) RETURNS TABLE (id uuid, content text, metadata jsonb, similarity float)
LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT e.id, e.content, e.metadata, 1 - (e.embedding <=> query_embedding) AS similarity
  FROM embeddings e
  ORDER BY e.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

Task 3: Buat API routes baru:
- GET /api/ai/memory/:sessionId → get agent_memory
- PUT /api/ai/memory/sync → upsert agent_memory
- POST /api/agent/handoff → create handoff task
- GET /api/agent/handoffs → list pending handoffs
- GET /api/competitor/intel → list competitor intel
- POST /api/competitor/scan → trigger competitor scan via SerpAPI

Task 4: Deploy + push

JANGAN ubah UI. Fokus backend only.
```

**Deliverables Session 2:**
- [ ] pgvector enabled di Supabase
- [ ] 5 tabel v4.0 baru + match_documents function
- [ ] 6 API routes baru
- [ ] Deployed

---

### ═══════════════════════════════════════
### SESSION 3 — LangGraph.js v2 (RAG Memory)
### ═══════════════════════════════════════

**Estimasi durasi**: 60-90 menit
**Estimasi credit**: 95-109 credits
**Prerequisites**:
- [ ] Session 2 selesai (pgvector + embeddings table)
- [ ] OpenAI API Key ada (untuk text-embedding-3-small)

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine. Sessions 1 & 2 selesai.
pgvector enabled, embeddings table exists, agent_memory table exists.

Setup: clone repo, npm install, buat .dev.vars (dengan OPENAI_API_KEY), build, pm2 start

TUGAS SESSION INI (LangGraph.js v2 dengan RAG):

Requirement:
- Install: npm install @langchain/community @langchain/openai

Task 1: Upgrade MessageComposer → v2 di src/agents/messageComposer.ts (atau buat file baru)
- Node 1: fetch_memory → query embeddings table via SupabaseVectorStore similarity search
  - Search: "customer_id: {lead_id} whatsapp_history"
  - Gunakan text-embedding-3-small (OpenAI)
- Node 2: compose → gunakan memory_context dari node 1 untuk compose pesan yang kontekstual
- Node 3: check_escalate → jika lead_score > 85, set requires_human = true
- Conditional edge: jika requires_human → "human_review" node, else END
- Export: MessageComposerV2

Task 2: Buat PricingOptimizer agent di src/agents/pricingOptimizer.ts
- Node 1: fetch_product_data → query products + order_items + competitor_intel
- Node 2: calculate_price → GPT-4o-mini menghitung optimal price (margin min 30%)
- Node 3: persist_decision → insert ke pricing_history
- Response JSON: {new_price, reasoning, confidence}
- Export: PricingOptimizer

Task 3: Update routes:
- PUT POST /api/closer/ai-compose → gunakan MessageComposerV2 bukan MessageComposer lama
- GET /api/pricing/suggest/:productId → panggil PricingOptimizer
- POST /api/ai/resume-thread → untuk human-in-loop approval dari dashboard

Task 4: Buat route POST /api/ai/rag/query:
- Receive: { query: string, limit?: number }
- Call SupabaseVectorStore.similaritySearch(query, limit || 5)
- Return: relevant docs

Task 5: Build, test, deploy, push git

CATATAN: Gunakan @langchain/langgraph/web (bukan node version) untuk CF Workers compatibility.
```

**Deliverables Session 3:**
- [ ] MessageComposerV2 dengan RAG memory
- [ ] PricingOptimizer agent
- [ ] /api/pricing/suggest/:id
- [ ] /api/ai/rag/query
- [ ] /api/ai/resume-thread (human-in-loop)
- [ ] Deployed

---

### ═══════════════════════════════════════
### SESSION 4 — CrewAI v4.0 + New Agents
### ═══════════════════════════════════════

**Estimasi durasi**: 60-90 menit
**Estimasi credit**: 95-109 credits
**Prerequisites**:
- [ ] Session 3 selesai
- [ ] Fonnte token ada (untuk churn_detector agent)

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine v4.0.
Sessions 1-3 selesai. LangGraph v2 + RAG berfungsi.

Setup: clone CREWAI repo dulu:
git clone https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Crew.ai.sovereign.orchest.git crewai-sovereign
cd crewai-sovereign

TUGAS SESSION INI (CrewAI v4.0 Upgrade):

Task 1: Update config/agents.yaml - tambah 4 agen baru:

1. churn_detector:
   role: "Customer Retention Specialist"
   goal: "Identify customers showing churn risk (no order > 30 days) and send retention WA"
   backstory: "Expert in behavioral analysis. Analyzes order frequency, last purchase, response rates."
   llm: "groq/llama-3.3-70b-versatile"
   tools: [supabase_tool, rag_memory_tool, fonnte_tool]

2. upsell_advisor:
   role: "Revenue Maximization Architect"
   goal: "Recommend cross-sell/upsell based on order history and basket analysis"
   llm: "openai/gpt-4o-mini"
   tools: [supabase_tool, rag_memory_tool]

3. engagement_analyzer:
   role: "Instagram Performance Auditor"
   goal: "Analyze IG content performance from @fashionkas.official and @resellerkas.official"
   llm: "groq/llama-3.3-70b-versatile"
   tools: [scraper_tool, supabase_tool]

4. competitor_watch:
   role: "Market Intelligence Specialist"
   goal: "Monitor competitor brands using SerpAPI and identify market opportunities"
   llm: "groq/llama-3.3-70b-versatile"
   tools: [serpapi_tool, supabase_tool]

Task 2: Update config/tasks.yaml - tambah 4 tasks baru:
1. detect_churn_task → agent: churn_detector
2. find_upsell_task → agent: upsell_advisor
3. analyze_content_task → agent: engagement_analyzer
4. competitor_scan_task → agent: competitor_watch

Task 3: Buat tools/rag_memory_tool.py:
- RAGMemoryTool: query pgvector embeddings table di Supabase
- Input: query string
- Output: relevant text from embeddings
- Gunakan OPENAI_API_KEY untuk text-embedding-3-small

Task 4: Buat tools/scraper_tool.py:
- IGScraperTool: fetch IG profile data via ScraperAPI
- Input: username string
- Output: profile data JSON (followers, engagement, posts)

Task 5: Update src/sovereign_crew/crew.py:
- Tambah RetentionCrew (churn_detector + upsell_advisor)
- Tambah ContentAnalysisCrew (engagement_analyzer)
- Tambah CompetitorIntelCrew (competitor_watch)

Task 6: Update requirements.txt dengan deps baru

Task 7: Git commit & push ke GitHub:
git add -A
git commit -m "feat: CrewAI v4.0 - 4 new agents (churn, upsell, engagement, competitor)"
git push origin main

CATATAN: Jangan deploy ke AMP sekarang. Cukup push ke GitHub.
Koneksi ke AMP Studio dilakukan manual oleh Founder via UI.
```

**Deliverables Session 4:**
- [ ] 4 agen baru di agents.yaml
- [ ] 4 tasks baru di tasks.yaml
- [ ] rag_memory_tool.py
- [ ] scraper_tool.py
- [ ] RetentionCrew, ContentAnalysisCrew, CompetitorIntelCrew
- [ ] Pushed ke GitHub (Crew.ai.sovereign.orchest)

---

### ═══════════════════════════════════════
### SESSION 5 — AI Intelligence Page UI
### ═══════════════════════════════════════

**Estimasi durasi**: 60-90 menit
**Estimasi credit**: 90-109 credits
**Prerequisites**:
- [ ] Session 1-4 selesai
- [ ] /api/ai/tasks, /api/ai/insights berfungsi

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine v4.0.
Sessions 1-4 selesai. Backend lengkap. Sekarang fokus UI.

Setup: clone main repo, npm install, buat .dev.vars, build, pm2 start

TUGAS SESSION INI (AI Intelligence Center Page):

Task 1: Buat halaman /app/ai di src/pages/aiPage.ts (atau inline di index.tsx)
Gunakan design system yang sudah ada: Terminal-Chic Glassmorphism
Colors: #0a0a0f background, #7C3AED purple, #22C55E green, #F59E0B gold
Font: Inter + JetBrains Mono

Layout AI Intelligence Page:
┌─────────────────────────────────────────────────┐
│  AI INTELLIGENCE CENTER                         │
│  ─────────────────────────────────────────────  │
│  ENGINE STATUS                                  │
│  ┌────────────────┐ ┌────────────────┐          │
│  │ LangGraph.js   │ │ CrewAI AMP     │          │
│  │ ONLINE ● 6     │ │ ONLINE ● 12    │          │
│  │ agents         │ │ agents         │          │
│  └────────────────┘ └────────────────┘          │
│                                                 │
│  RECENT AI INSIGHTS                             │
│  (cards grid, fetch /api/ai/insights)           │
│                                                 │
│  AI TASK QUEUE                                  │
│  (table: task, agent, status, time)             │
│  (fetch /api/ai/tasks)                          │
│                                                 │
│  ACTIONS                                        │
│  [Generate Insights] [Run Market Analysis]      │
│  [Churn Detection] [Pricing Optimizer]          │
│                                                 │
│  HUMAN REVIEW QUEUE (if any pending)            │
│  (list tasks that require_human = true)         │
│  [Approve] [Reject] [Edit & Send]               │
└─────────────────────────────────────────────────┘

Task 2: Tambahkan "AI" item ke sidebar navigation
Task 3: Route handler sudah ada di /app/ai, connect ke aiPage()
Task 4: Test semua button actions panggil API yang benar
Task 5: Build, deploy, push git

Gunakan Tailwind CSS via CDN (sudah ada). Jangan install framework baru.
Ikuti pattern yang sama dengan halaman Scout dan Closer yang sudah ada.
```

**Deliverables Session 5:**
- [ ] /app/ai page lengkap
- [ ] Engine status widget
- [ ] AI Insights cards
- [ ] Task Queue table
- [ ] Human Review Queue
- [ ] Action buttons functional
- [ ] Deployed

---

### ═══════════════════════════════════════
### SESSION 6 — Fonnte Live + Auto-Sequence
### ═══════════════════════════════════════

**Estimasi durasi**: 45-60 menit
**Estimasi credit**: 80-95 credits
**Prerequisites**:
- [ ] **Fonnte token WAJIB ada** — tanpa ini session tidak bisa dijalankan
- [ ] Session 1-5 selesai

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine v4.0.
Sessions 1-5 selesai. Sekarang fokus Fonnte WhatsApp integration.

FONNTE_TOKEN sudah ada: <PASTE_TOKEN_DI_SINI>

Setup: clone, install, .dev.vars (dengan FONNTE_TOKEN), build, pm2 start

TUGAS SESSION INI (Fonnte Live Integration):

Task 1: Test dan fix route POST /api/wa/send:
- Verify Fonnte API: POST https://api.fonnte.com/send
- Headers: { Authorization: FONNTE_TOKEN }
- Body: { target: "628123456789", message: "Test dari Sovereign Engine", countryCode: "62" }
- Test dengan nomor WhatsApp Founder sendiri

Task 2: Test dan fix route GET /api/wa/status:
- GET https://api.fonnte.com/device
- Return: device status, connected, battery

Task 3: Implement auto-sequence (Closer Agent Day 0/3/7/14):
- POST /api/closer/sequence:
  - Receive: { lead_id, sequence_day: 0|3|7|14 }
  - Fetch lead data dari Supabase
  - Pilih template sesuai sequence_day
  - Compose via LangGraph MessageComposerV2 (RAG-aware)
  - Send via Fonnte
  - Log ke wa_logs table
  - Update leads.status

Task 4: Update Closer page UI:
- Tambah "Send via Fonnte" button (live, bukan template saja)
- Tambah sequence planner: pilih lead → pilih day → send
- Show wa_logs terbaru di send log section

Task 5: Test full flow:
- Select hot lead (score > 70)
- AI compose message
- Send via Fonnte
- Verify di wa_logs table
- Verify delivered di WhatsApp

Task 6: Deploy + push

JANGAN kirim pesan massal. Test dengan 1-2 nomor saja dulu.
```

**Deliverables Session 6:**
- [ ] Fonnte send tested & working
- [ ] Device status endpoint working
- [ ] Auto-sequence Day 0 functional
- [ ] wa_logs populated
- [ ] Closer UI with live send

---

### ═══════════════════════════════════════
### SESSION 7 — Dashboard Upgrade + Reports
### ═══════════════════════════════════════

**Estimasi durasi**: 45-60 menit
**Estimasi credit**: 75-90 credits
**Prerequisites**:
- [ ] Session 1-6 selesai

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine v4.0. Sessions 1-6 selesai.

Setup: clone, install, .dev.vars, build, pm2 start

TUGAS SESSION INI (Real-Money Dashboard Upgrade):

Task 1: Upgrade /api/dashboard/stats dengan metrics baru:
- Unpaid invoices: orders WHERE status IN ('pending', 'processing')
- Revenue by channel: GROUP BY source (IG/WA/catalog/reseller)
- Average Order Value: SUM(total_amount)/COUNT(orders)
- Customer LTV: SUM per customer (query customers.total_spent)
- Weekly revenue trend: last 7 days grouped by date
- Lead funnel: total → scored → contacted → converted (per stage)

Task 2: Upgrade Dashboard UI:
- Tambah "Unpaid Invoices" stat card
- Tambah "Revenue by Channel" mini bar chart (pakai inline SVG atau minimal chart)
- Tambah "Weekly Trend" sparkline
- Tambah "Lead Funnel" compact visualization

Task 3: Upgrade Reports Page:
- Revenue breakdown by channel
- Lead conversion funnel chart
- Customer tier distribution
- Product performance ranking (GMV per product)

Task 4: Buat /api/dashboard/ai-insights yang benar-benar generate insights via LangGraph:
- Fetch stats
- Call InsightGenerator agent
- Return 3-5 actionable insights
- Cache di ai_insights table (1 hour TTL)

Task 5: Build, test, deploy, push

Gunakan hanya data yang ada di Supabase. Jangan buat mock data.
```

**Deliverables Session 7:**
- [ ] Enhanced dashboard stats
- [ ] Revenue by channel
- [ ] Weekly trend
- [ ] Lead funnel
- [ ] Real AI insights generation
- [ ] Deployed

---

### ═══════════════════════════════════════
### SESSION 8 — Polish, Security & Final Deploy
### ═══════════════════════════════════════

**Estimasi durasi**: 45-60 menit
**Estimasi credit**: 80-100 credits
**Prerequisites**:
- [ ] Session 1-7 selesai

**COPY-PASTE prompt ini ke Claude/Genspark:**

```
Melanjutkan Sovereign Business Engine v4.0. Sessions 1-7 selesai.
Ini adalah SESSION FINAL — polish, security hardening, dan deployment lengkap.

Setup: clone, install, .dev.vars, build, pm2 start

TUGAS SESSION INI (Final Polish & Security):

Task 1: Security Hardening:
- Implementasi Device ID Locking di auth flow:
  - Saat login, generate device fingerprint dari user agent + screen + timezone
  - Simpan fingerprint hash di localStorage
  - Saat verify token, bandingkan fingerprint
  - Jika tidak match → force logout
- Pastikan robots.txt ada di public/ dengan noindex

Task 2: LangGraph Rate Limiting & Safety:
- Tambahkan recursion_limit: 5 di semua StateGraph configs
- Tambahkan timeout handling (3s untuk edge, 10s untuk compose)
- Error fallback: jika AI gagal → gunakan template default

Task 3: Monitoring Setup:
- Enable LANGCHAIN_TRACING_V2=true di .dev.vars
- Verify LangSmith traces working di langsmith.com
- Tambah /api/system/metrics endpoint:
  - Agent success rate dari ai_tasks
  - Last 24h: tasks created, completed, failed
  - Avg latency per agent type

Task 4: Mobile Optimization:
- Audit semua halaman di mobile viewport (375px)
- Fix sidebar collapse behavior
- Ensure all cards stack properly
- Test PIN input on mobile

Task 5: Update semua docs (docs/ folder):
- docs/01-PRD.md → update versi ke v4.0, update KPIs
- docs/02-ARCHITECTURE.md → update agent inventory (21 agents)
- docs/04-TODO-ROADMAP.md → update phase completion status

Task 6: Final Deploy:
- npm run build (verify semua 0 errors)
- npx wrangler pages deploy dist --project-name sovereign-orchestrator
- Verify ALL endpoints:
  curl https://sovereign-orchestrator.pages.dev/api/health
  curl https://sovereign-orchestrator.pages.dev/api/ai/status
  curl https://sovereign-orchestrator.pages.dev/api/validation/stats

Task 7: Final Git:
- git add -A
- git commit -m "feat: v4.0 COMPLETE - 21 agents, RAG memory, full automation"
- git push origin main

Task 8: Backup project (ProjectBackup tool)

DELIVERABLE: Project v4.0 fully deployed dan documented.
```

**Deliverables Session 8:**
- [ ] Device ID locking
- [ ] robots.txt
- [ ] LangGraph safety limits
- [ ] Monitoring endpoint
- [ ] Mobile optimized
- [ ] Docs updated
- [ ] Final production deploy verified
- [ ] Git pushed + backup

---

## 📊 RINGKASAN TOTAL SESSIONS

| Session | Fokus | Estimasi Credit | Estimasi Durasi | Blocker |
|---------|-------|-----------------|-----------------|---------|
| S1 | Foundation DB + Fonnte Route | 80-95 | 45-60 mnt | Fonnte token (opsional) |
| S2 | pgvector + v4.0 DB Schema | 85-100 | 45-60 mnt | OpenAI key (untuk embeddings) |
| S3 | LangGraph v2 + RAG | 95-109 | 60-90 mnt | S2 + OpenAI key |
| S4 | CrewAI v4.0 Agents | 95-109 | 60-90 mnt | S3 |
| S5 | AI Intelligence UI | 90-109 | 60-90 mnt | S1 (API routes) |
| S6 | Fonnte Live + Auto-Sequence | 80-95 | 45-60 mnt | **FONNTE TOKEN WAJIB** |
| S7 | Dashboard Upgrade + Reports | 75-90 | 45-60 mnt | S1 |
| S8 | Polish + Security + Final Deploy | 80-100 | 45-60 mnt | S1-S7 |
| **TOTAL** | | **~700-807 credits** | **~7-10 jam** | |

**Estimasi total budget**: ~700-807 credits (Genspark) atau ~$5-12 (Claude.ai)

---

## 🔄 DEPENDENCY GRAPH SESSION

```
S1 (DB Tables) ──┬── S5 (AI UI)
                 ├── S6 (Fonnte Live)  [BUTUH FONNTE TOKEN]
                 └── S7 (Dashboard)

S2 (pgvector) ──── S3 (LangGraph v2 RAG)  [BUTUH OPENAI KEY]
                              │
                              └── S4 (CrewAI v4.0)

S4 ──────────── S6 (untuk churn detection via WA)

S1+S2+S3+S4+S5+S6+S7 ──── S8 (Final Polish)
```

---

## ⚡ QUICK REFERENCE COMMANDS

```bash
# Standard start sequence (setiap session)
git clone https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git webapp
cd webapp && npm install
# [buat .dev.vars]
npm run build
fuser -k 3000/tcp 2>/dev/null || true
pm2 start ecosystem.config.cjs
sleep 3 && curl http://localhost:3000/api/health

# Deploy ke production
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"
npm run build
npx wrangler pages deploy dist --project-name sovereign-orchestrator

# Push ke GitHub
git add -A
git commit -m "feat: [deskripsi]"
git push origin main

# Clone CrewAI repo
git clone https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Crew.ai.sovereign.orchest.git crewai-sovereign
```

---

## 🎯 PRIORITAS SEBELUM MULAI SESSION

**Sebelum Session 1:**
- [ ] Daftar Fonnte di fonnte.com → scan QR WhatsApp → copy Bearer token
- [ ] Siapkan OpenAI API Key di platform.openai.com

**Minimal untuk jalankan Session 1:**
- Hanya butuh credentials yang sudah ada di .dev.vars template di atas
- Fonnte & OpenAI bisa menyusul di session berikutnya

---

## 📋 CHECKLIST VERIFIKASI TIAP AKHIR SESSION

```
□ npm run build → exit 0, 0 errors
□ curl http://localhost:3000/api/health → status: "ok"
□ curl https://sovereign-orchestrator.pages.dev/api/health → deployed version match
□ git log --oneline -3 → commit terbaru ada
□ git push berhasil ke GitHub
□ pm2 logs --nostream → tidak ada critical errors
□ Backup jika banyak perubahan besar
```

---

*Master Session Handoff v1.0 | Sovereign Business Engine | 2026-04-01 | CONFIDENTIAL*
