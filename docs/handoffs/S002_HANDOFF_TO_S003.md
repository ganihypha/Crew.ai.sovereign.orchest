# 🎯 MASTER SESSION HANDOFF #002 → #003
## SOVEREIGN BUSINESS ENGINE — Phase 2: pgvector + v4.0 Database Schema

**Session**: #002
**Status**: ⏳ PENDING — Dimulai Setelah Session #001 Complete
**Prerequisite**: Session #001 done (4 tabel baru exist)
**Next Session Budget**: 100 credits

---

## ♾️ INFINITE GROWTH LOOP STATUS

```yaml
Session #2 Projection (estimate):
  Efficiency: 82% (improving from S1 baseline)
  Knowledge: 1.15 (gained DB expertise from S1)
  Expected Output: ~100 × 0.82 × 1.15 = 94.3 effective credits

Prediction for Session #3:
  Efficiency: 84%
  Knowledge: 1.30 (LangGraph RAG expertise added)
  Expected Output: ~100 × 0.84 × 1.30 = 109.2 effective credits
  Improvement: +16% vs Session #2!
```

---

## 📋 SESSION #002 GOALS

### Primary Objectives
1. **Enable pgvector** extension di Supabase
2. **Buat 5 tabel v4.0** baru (embeddings, agent_memory, agent_handoffs, pricing_history, competitor_intel)
3. **Buat `match_documents` SQL function** untuk similarity search
4. **Buat 6 API routes baru** (memory, handoff, competitor)
5. **Deploy & push**

### Success Criteria
- [ ] pgvector enabled: `SELECT * FROM pg_extension WHERE extname = 'vector'`
- [ ] 5 tabel baru exist di Supabase
- [ ] `match_documents` function callable via RPC
- [ ] 6 API routes responsive
- [ ] Build zero errors
- [ ] Deployed to production
- [ ] GitHub pushed

---

## 🔍 VERIFY SESSION #001 COMPLETE

Sebelum mulai, confirm:
```bash
# Clone dan check tabel ada
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git" webapp
cd webapp && npm install

# Check tabel session 1
curl -s "https://lfohzibcsafqthupcvdg.supabase.co/rest/v1/wa_logs?select=id&limit=1" \
  -H "apikey: <SUPABASE_ANON_KEY>" | python3 -c "import sys,json; print('wa_logs OK' if isinstance(json.load(sys.stdin), list) else 'wa_logs MISSING')"

curl -s "https://lfohzibcsafqthupcvdg.supabase.co/rest/v1/ai_tasks?select=id&limit=1" \
  -H "apikey: <SUPABASE_ANON_KEY>" | python3 -c "import sys,json; print('ai_tasks OK' if isinstance(json.load(sys.stdin), list) else 'ai_tasks MISSING')"
```

Jika tabel dari Session #001 tidak ada → **jalankan SQL dari S001 dulu**.

---

## ⚙️ SESSION #002 SETUP

```bash
# Standard setup (sama setiap session)
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git" webapp
cd webapp && npm install
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"
# buat .dev.vars dengan semua credentials
npm run build
fuser -k 3000/tcp 2>/dev/null || true
pm2 start ecosystem.config.cjs
sleep 3 && curl http://localhost:3000/api/health
```

---

## 🛠️ TASK BREAKDOWN SESSION #002

### Task 1 — Enable pgvector [~5 credits]

Execute di **Supabase SQL Editor** (dashboard.supabase.com):
```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
-- Expected: vector | 0.8.0 (atau versi terbaru)
```

---

### Task 2 — Buat 5 Tabel v4.0 [~15 credits]

```sql
-- 1. embeddings: LangChain RAG long-term memory
CREATE TABLE IF NOT EXISTS embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL,
  embedding vector(1536),
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT timezone('utc', now())
);
CREATE INDEX IF NOT EXISTS idx_embeddings_vector 
  ON embeddings USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- 2. agent_memory: Short-term context cache
CREATE TABLE IF NOT EXISTS agent_memory (
  session_id text PRIMARY KEY,
  framework varchar(50),
  state_json jsonb DEFAULT '{}',
  updated_at timestamptz DEFAULT timezone('utc', now())
);

-- 3. agent_handoffs: Inter-framework message bus (LangGraph ↔ CrewAI)
CREATE TABLE IF NOT EXISTS agent_handoffs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_agent varchar(100) NOT NULL,
  target_agent varchar(100) NOT NULL,
  payload jsonb DEFAULT '{}',
  status varchar(20) DEFAULT 'pending',
  created_at timestamptz DEFAULT timezone('utc', now()),
  processed_at timestamptz
);
CREATE INDEX IF NOT EXISTS idx_agent_handoffs_status ON agent_handoffs(status);
CREATE INDEX IF NOT EXISTS idx_agent_handoffs_target ON agent_handoffs(target_agent);

-- 4. pricing_history: AI pricing decisions audit log
CREATE TABLE IF NOT EXISTS pricing_history (
  id serial PRIMARY KEY,
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  old_price numeric NOT NULL,
  new_price numeric NOT NULL,
  ai_reasoning text,
  confidence numeric DEFAULT 0.0,
  approved boolean DEFAULT false,
  created_at timestamptz DEFAULT timezone('utc', now())
);

-- 5. competitor_intel: Market intelligence data
CREATE TABLE IF NOT EXISTS competitor_intel (
  id serial PRIMARY KEY,
  source varchar(100) NOT NULL,
  brand_name varchar(100),
  data jsonb DEFAULT '{}',
  scraped_at timestamptz DEFAULT timezone('utc', now())
);
CREATE INDEX IF NOT EXISTS idx_competitor_intel_source ON competitor_intel(source);

-- match_documents function untuk RAG similarity search
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_count int DEFAULT 5,
  filter jsonb DEFAULT '{}'
)
RETURNS TABLE (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.content,
    e.metadata,
    1 - (e.embedding <=> query_embedding) AS similarity
  FROM embeddings e
  ORDER BY e.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

---

### Task 3 — Buat 6 API Routes Baru [~20 credits]

Tambahkan ke `src/routes/ai.ts` atau file routes yang relevan:

```typescript
// GET /api/ai/memory/:sessionId
app.get('/api/ai/memory/:sessionId', jwtMiddleware, async (c) => {
  const sessionId = c.req.param('sessionId')
  const { data } = await supabase(c.env).from('agent_memory')
    .select('*').eq('session_id', sessionId).single()
  return c.json({ success: true, data: data || null })
})

// PUT /api/ai/memory/sync
app.put('/api/ai/memory/sync', jwtMiddleware, async (c) => {
  const body = await c.req.json()
  const { sessionId, framework, stateJson } = body
  const { data, error } = await supabase(c.env).from('agent_memory')
    .upsert({ session_id: sessionId, framework, state_json: stateJson, updated_at: new Date().toISOString() })
    .select().single()
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, data })
})

// POST /api/agent/handoff
app.post('/api/agent/handoff', jwtMiddleware, async (c) => {
  const body = await c.req.json()
  const { source_agent, target_agent, payload } = body
  const { data, error } = await supabase(c.env).from('agent_handoffs')
    .insert({ source_agent, target_agent, payload })
    .select().single()
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, data })
})

// GET /api/agent/handoffs (list pending)
app.get('/api/agent/handoffs', jwtMiddleware, async (c) => {
  const status = c.req.query('status') || 'pending'
  const { data } = await supabase(c.env).from('agent_handoffs')
    .select('*').eq('status', status).order('created_at', { ascending: true })
  return c.json({ success: true, data: data || [], count: data?.length || 0 })
})

// GET /api/competitor/intel
app.get('/api/competitor/intel', jwtMiddleware, async (c) => {
  const { data } = await supabase(c.env).from('competitor_intel')
    .select('*').order('scraped_at', { ascending: false }).limit(20)
  return c.json({ success: true, data: data || [], count: data?.length || 0 })
})

// POST /api/competitor/scan → trigger SerpAPI scan
app.post('/api/competitor/scan', jwtMiddleware, async (c) => {
  const { keywords } = await c.req.json()
  const serpApiKey = c.env.SERPAPI_KEY
  if (!serpApiKey) return c.json({ success: false, error: 'SerpAPI key not configured' }, 503)
  
  const searchUrl = `https://serpapi.com/search.json?q=${encodeURIComponent(keywords || 'fashion reseller Indonesia')}&api_key=${serpApiKey}&num=10`
  const response = await fetch(searchUrl)
  const data = await response.json() as any
  
  const intel = {
    source: 'serpapi',
    brand_name: keywords,
    data: { results: data.organic_results?.slice(0, 5) || [] }
  }
  
  await supabase(c.env).from('competitor_intel').insert(intel)
  return c.json({ success: true, message: 'Competitor scan complete', results: intel.data.results?.length || 0 })
})
```

---

### Task 4 — Deploy & Verify [~10 credits]

```bash
npm run build

# Check build output
ls -la dist/

# Deploy
npx wrangler pages deploy dist --project-name sovereign-orchestrator

# Verify new endpoints
curl -H "Authorization: Bearer <JWT>" https://sovereign-orchestrator.pages.dev/api/agent/handoffs
curl -H "Authorization: Bearer <JWT>" https://sovereign-orchestrator.pages.dev/api/competitor/intel

# Git push
git add -A
git commit -m "feat: Session 2 - pgvector + v4.0 DB schema + 6 new API routes

- Enabled pgvector extension in Supabase
- Created 5 new v4.0 tables: embeddings, agent_memory, agent_handoffs, pricing_history, competitor_intel
- Created match_documents RPC function for RAG similarity search
- Added 6 new API routes: memory sync, agent handoff, competitor intel
- Version bump to v3.7"
git push origin main
```

---

## 📊 WHAT SHOULD BE DELIVERED

```yaml
Database (Supabase):
  pgvector extension: ✅ Enabled
  embeddings table: ✅ Created (vector(1536))
  agent_memory table: ✅ Created
  agent_handoffs table: ✅ Created
  pricing_history table: ✅ Created
  competitor_intel table: ✅ Created
  match_documents function: ✅ Created (RPC callable)

API Routes (6 new):
  GET /api/ai/memory/:sessionId: ✅
  PUT /api/ai/memory/sync: ✅
  POST /api/agent/handoff: ✅
  GET /api/agent/handoffs: ✅
  GET /api/competitor/intel: ✅
  POST /api/competitor/scan: ✅

Deployment:
  Build: zero errors
  Production: deployed (v3.7)
  GitHub: pushed
```

---

## 🛠️ KNOWN ISSUES / POTENTIAL BLOCKERS

| # | Issue | Probability | Resolution |
|---|-------|-------------|-----------|
| B1 | pgvector tidak available di Supabase free tier | LOW | Supabase free tier support pgvector sejak 2023 |
| B2 | ivfflat index butuh minimal 100 rows | MEDIUM | Buat index tanpa ivfflat dulu, tambah setelah ada data |
| B3 | OpenAI key belum ada (untuk embedding generation) | MEDIUM | Buat tabel dulu, embedding function di Session #3 |

---

## 💡 NOTES FOR SESSION #003

Setelah Session #002 selesai, **Session #003** fokus ke:
- Install `@langchain/community` + `@langchain/openai`
- Upgrade MessageComposer → v2 dengan RAG memory
- Buat PricingOptimizer LangGraph agent
- RAG query endpoint (`/api/ai/rag/query`)
- Human-in-loop resume endpoint

**Prerequisites untuk Session #003:**
- [ ] **OpenAI API Key WAJIB ada** (untuk text-embedding-3-small)
- [ ] Session #002 complete (embeddings table + match_documents)

---

## 🎉 FILL THIS AFTER SESSION #002 COMPLETE

```
SESSION #002 ACTUAL RESULTS:
  Credits Used: __ credits (estimate: 85-100)
  Duration: __ minutes
  Efficiency: __% 
  
DELIVERABLES STATUS:
  pgvector enabled: [✅/❌]
  embeddings table: [✅/❌]
  agent_memory table: [✅/❌]
  agent_handoffs table: [✅/❌]
  pricing_history table: [✅/❌]
  competitor_intel table: [✅/❌]
  match_documents function: [✅/❌]
  6 API routes: [✅/❌]
  Deployed: [✅/❌]
  GitHub pushed: [✅/❌]
  
BLOCKERS ENCOUNTERED: [describe]
NOTES FOR SESSION #003: [context]

PRODUCTION HEALTH:
  curl https://sovereign-orchestrator.pages.dev/api/health → [result]
  Version: v3.7
```

---

*Session Handoff #002 | Sovereign Business Engine | CONFIDENTIAL | Haidar Faras*
