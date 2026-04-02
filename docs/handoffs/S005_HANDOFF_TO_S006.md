# 🎯 MASTER SESSION HANDOFF #005 → #006
## SOVEREIGN BUSINESS ENGINE — Phase 5: AI Intelligence Dashboard UI

**Session**: #005
**Status**: ⏳ PENDING — Dimulai Setelah Session #004 Complete
**Prerequisite**: Session #004 done (8 CrewAI agents ready, RAG working)
**Next Session Budget**: 100 credits

---

## ♾️ INFINITE GROWTH LOOP STATUS

```yaml
Session #5 Projection:
  Efficiency: 88%
  Knowledge: 1.60 (Full-stack AI UI patterns mastered)
  Expected Output: ~100 × 0.88 × 1.60 = 140.8 effective credits

Prediction for Session #6:
  Efficiency: 90%
  Knowledge: 1.75 (Fonnte live integration + automation)
  Expected Output: ~100 × 0.90 × 1.75 = 157.5 effective credits
  Improvement: +12% vs Session #5!
```

---

## 📋 SESSION #005 GOALS (AI Intelligence Page)

### Primary Objectives
1. **Buat halaman `/ai`** — AI Intelligence Center UI
2. **Engine Status card** — status 12 agents (LangGraph + CrewAI)
3. **Insight cards** — recent AI-generated insights dari tabel `ai_insights`
4. **Task queue table** — pending, running, completed tasks dari `ai_tasks`
5. **Trigger buttons** — kick off CrewAI crews dari UI
6. **Real-time polling** — auto-refresh setiap 30 detik
7. **Deploy & push**

### Success Criteria
- [ ] `/ai` page loads tanpa error
- [ ] Engine status menampilkan 8 CrewAI agents + 4 LangGraph agents
- [ ] Task queue menampilkan data dari `ai_tasks` table
- [ ] "Run Churn Analysis" button trigger `/api/ai/crew/churn-analysis`
- [ ] "Run Upsell Analysis" button trigger `/api/ai/crew/upsell-analysis`
- [ ] Mobile responsive ✅
- [ ] Deployed & verified

---

## ✅ VERIFY SESSION #004 COMPLETE

```bash
# Check churn analysis endpoint
curl -s -X POST "https://sovereign-orchestrator.pages.dev/api/ai/crew/churn-analysis" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json"
# Expected: {"success":true,"task_id":"...","status":"running"}

# Check health shows v4.0
curl -s "https://sovereign-orchestrator.pages.dev/api/health"
# Expected: version "4.0"
```

---

## ⚙️ SESSION #005 SETUP

```bash
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git" webapp
cd webapp && npm install
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"
npm run build
fuser -k 3000/tcp 2>/dev/null || true
pm2 start ecosystem.config.cjs
sleep 3 && curl http://localhost:3000/api/health
```

---

## 🛠️ TASK BREAKDOWN SESSION #005

### Task 1 — Check Current AI Route & ai_tasks Table [~5 credits]

```bash
# Check if ai_tasks table exists
curl -s "https://lfohzibcsafqthupcvdg.supabase.co/rest/v1/ai_tasks?limit=5" \
  -H "apikey: <SUPABASE_ANON_KEY>"

# Check ai_insights table
curl -s "https://lfohzibcsafqthupcvdg.supabase.co/rest/v1/ai_insights?limit=5" \
  -H "apikey: <SUPABASE_ANON_KEY>"
```

Jika table tidak ada, buat dulu:

```sql
-- Di Supabase SQL Editor
CREATE TABLE IF NOT EXISTS ai_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_type TEXT NOT NULL,
  task_type TEXT NOT NULL,
  input_data JSONB,
  output_data JSONB,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'pending_human', 'approved', 'rejected')),
  kickoff_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS ai_insights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  insight_type TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  data JSONB,
  priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### Task 2 — Buat AI Intelligence API Routes [~20 credits]

Buat file `src/routes/intelligence.ts`:

```typescript
// src/routes/intelligence.ts
import { Hono } from 'hono'
import { createClient } from '@supabase/supabase-js'

const router = new Hono<{ Bindings: { 
  SUPABASE_URL: string; SUPABASE_SERVICE_KEY: string; 
  CREWAI_AMP_URL: string; CREWAI_AMP_TOKEN: string 
}}>()

const supabase = (env: any) => createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY)

// GET /api/ai/intelligence/status
router.get('/status', async (c) => {
  const langgraphAgents = [
    { name: 'ScoutScorer', type: 'langgraph', status: 'active', latency: '<3s' },
    { name: 'MessageComposerV2', type: 'langgraph', status: 'active', latency: '<2s' },
    { name: 'InsightGenerator', type: 'langgraph', status: 'active', latency: '<5s' },
    { name: 'PricingOptimizer', type: 'langgraph', status: 'active', latency: '<3s' }
  ]
  const crewaiAgents = [
    { name: 'MarketValidator', type: 'crewai', status: 'active' },
    { name: 'LeadResearcher', type: 'crewai', status: 'active' },
    { name: 'RevenueAnalyst', type: 'crewai', status: 'active' },
    { name: 'ContentStrategist', type: 'crewai', status: 'active' },
    { name: 'ChurnDetector', type: 'crewai', status: 'active' },
    { name: 'UpsellAdvisor', type: 'crewai', status: 'active' },
    { name: 'EngagementAnalyzer', type: 'crewai', status: 'active' },
    { name: 'CompetitorIntelAgent', type: 'crewai', status: 'active' }
  ]
  return c.json({
    success: true,
    total_agents: 12,
    langgraph: langgraphAgents,
    crewai: crewaiAgents,
    system_status: 'operational'
  })
})

// GET /api/ai/intelligence/insights
router.get('/insights', async (c) => {
  const limit = parseInt(c.req.query('limit') || '10')
  const { data, error } = await supabase(c.env).from('ai_insights')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(limit)
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, insights: data || [], count: data?.length || 0 })
})

// POST /api/ai/intelligence/insights (create insight manually)
router.post('/insights', async (c) => {
  const body = await c.req.json()
  const { data, error } = await supabase(c.env).from('ai_insights').insert({
    insight_type: body.insight_type || 'manual',
    title: body.title,
    content: body.content,
    data: body.data || {},
    priority: body.priority || 'medium'
  }).select().single()
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, insight: data })
})

// PATCH /api/ai/intelligence/insights/:id/read
router.patch('/insights/:id/read', async (c) => {
  const id = c.req.param('id')
  const { data, error } = await supabase(c.env).from('ai_insights')
    .update({ is_read: true }).eq('id', id).select().single()
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, insight: data })
})

// GET /api/ai/intelligence/tasks
router.get('/tasks', async (c) => {
  const status = c.req.query('status')
  let query = supabase(c.env).from('ai_tasks')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(20)
  if (status) query = query.eq('status', status)
  const { data, error } = await query
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, tasks: data || [], count: data?.length || 0 })
})

export default router
```

---

### Task 3 — Buat AI Intelligence UI Page [~35 credits]

Tambahkan ke `src/index.tsx` route untuk halaman AI:

```typescript
// GET /ai - AI Intelligence Center page
app.get('/ai', jwtMiddleware, (c) => {
  return c.html(`<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Intelligence | Sovereign OS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    body { background: #0a0a0f; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    .glass { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(12px); }
    .agent-badge-crewai { background: rgba(59,130,246,0.2); border: 1px solid rgba(59,130,246,0.4); color: #93c5fd; }
    .agent-badge-langgraph { background: rgba(34,197,94,0.2); border: 1px solid rgba(34,197,94,0.4); color: #86efac; }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    .status-dot.active { background: #22C55E; box-shadow: 0 0 6px #22C55E; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .priority-critical { border-left: 3px solid #EF4444; }
    .priority-high { border-left: 3px solid #F59E0B; }
    .priority-medium { border-left: 3px solid #3B82F6; }
    .priority-low { border-left: 3px solid #6B7280; }
  </style>
</head>
<body class="min-h-screen p-4">
  
  <!-- Header -->
  <div class="flex items-center justify-between mb-6">
    <div class="flex items-center gap-3">
      <a href="/" class="text-gray-400 hover:text-white"><i class="fas fa-arrow-left"></i></a>
      <div>
        <h1 class="text-xl font-bold text-white"><i class="fas fa-brain mr-2 text-purple-400"></i>AI Intelligence Center</h1>
        <p class="text-xs text-gray-400">Sovereign Business Engine v4.0 — 12 Active Agents</p>
      </div>
    </div>
    <div class="flex gap-2">
      <span id="systemStatus" class="text-xs px-3 py-1 rounded-full glass"><span class="status-dot active mr-1"></span>Operational</span>
      <button onclick="refreshAll()" class="text-xs px-3 py-1 glass rounded-full hover:bg-white/10">
        <i class="fas fa-sync-alt mr-1"></i>Refresh
      </button>
    </div>
  </div>

  <!-- Agent Grid -->
  <div class="glass rounded-xl p-4 mb-4">
    <h2 class="text-sm font-semibold text-gray-300 mb-3"><i class="fas fa-robot mr-2"></i>Active Agents (12)</h2>
    <div id="agentGrid" class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <!-- Populated by JS -->
    </div>
  </div>

  <!-- Action Buttons -->
  <div class="glass rounded-xl p-4 mb-4">
    <h2 class="text-sm font-semibold text-gray-300 mb-3"><i class="fas fa-play-circle mr-2"></i>Run Analysis</h2>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button onclick="runCrew('churn-analysis')" class="px-3 py-2 rounded-lg text-xs font-medium bg-red-900/30 border border-red-500/30 text-red-300 hover:bg-red-900/50 transition">
        <i class="fas fa-user-times mr-1"></i>Churn Analysis
      </button>
      <button onclick="runCrew('upsell-analysis')" class="px-3 py-2 rounded-lg text-xs font-medium bg-green-900/30 border border-green-500/30 text-green-300 hover:bg-green-900/50 transition">
        <i class="fas fa-arrow-trend-up mr-1"></i>Upsell Analysis
      </button>
      <button onclick="runCrew('kickoff')" class="px-3 py-2 rounded-lg text-xs font-medium bg-purple-900/30 border border-purple-500/30 text-purple-300 hover:bg-purple-900/50 transition">
        <i class="fas fa-brain mr-1"></i>Full Validation
      </button>
      <button onclick="runCrew('engagement')" class="px-3 py-2 rounded-lg text-xs font-medium bg-blue-900/30 border border-blue-500/30 text-blue-300 hover:bg-blue-900/50 transition">
        <i class="fas fa-chart-line mr-1"></i>Engagement
      </button>
    </div>
    <div id="crewStatus" class="mt-2 text-xs text-gray-400"></div>
  </div>

  <!-- Insights + Tasks Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    
    <!-- AI Insights -->
    <div class="glass rounded-xl p-4">
      <div class="flex justify-between items-center mb-3">
        <h2 class="text-sm font-semibold text-gray-300"><i class="fas fa-lightbulb mr-2 text-yellow-400"></i>AI Insights</h2>
        <span id="insightCount" class="text-xs text-gray-500">loading...</span>
      </div>
      <div id="insightsList" class="space-y-2 max-h-80 overflow-y-auto">
        <div class="text-xs text-gray-500 text-center py-4"><i class="fas fa-spinner fa-spin mr-1"></i>Loading insights...</div>
      </div>
    </div>

    <!-- Task Queue -->
    <div class="glass rounded-xl p-4">
      <div class="flex justify-between items-center mb-3">
        <h2 class="text-sm font-semibold text-gray-300"><i class="fas fa-tasks mr-2 text-blue-400"></i>Task Queue</h2>
        <span id="taskCount" class="text-xs text-gray-500">loading...</span>
      </div>
      <div id="tasksList" class="space-y-2 max-h-80 overflow-y-auto">
        <div class="text-xs text-gray-500 text-center py-4"><i class="fas fa-spinner fa-spin mr-1"></i>Loading tasks...</div>
      </div>
    </div>
  </div>

  <script>
    const TOKEN = localStorage.getItem('sovereign_token') || ''
    const API_BASE = '/api'
    
    async function apiCall(endpoint, method = 'GET', body = null) {
      const opts = {
        method,
        headers: { 'Authorization': \`Bearer \${TOKEN}\`, 'Content-Type': 'application/json' }
      }
      if (body) opts.body = JSON.stringify(body)
      const res = await fetch(\`\${API_BASE}\${endpoint}\`, opts)
      return res.json()
    }

    async function loadAgents() {
      const data = await apiCall('/ai/intelligence/status')
      if (!data.success) return
      const grid = document.getElementById('agentGrid')
      const agents = [...(data.langgraph || []), ...(data.crewai || [])]
      grid.innerHTML = agents.map(a => \`
        <div class="rounded-lg p-2 \${a.type === 'crewai' ? 'agent-badge-crewai' : 'agent-badge-langgraph'} flex items-center gap-2">
          <span class="status-dot active"></span>
          <div>
            <div class="text-xs font-medium">\${a.name}</div>
            <div class="text-[10px] opacity-70">\${a.type.toUpperCase()}\${a.latency ? ' · ' + a.latency : ''}</div>
          </div>
        </div>
      \`).join('')
    }

    async function loadInsights() {
      const data = await apiCall('/ai/intelligence/insights?limit=10')
      const list = document.getElementById('insightsList')
      document.getElementById('insightCount').textContent = \`\${data.count || 0} insights\`
      if (!data.insights || data.insights.length === 0) {
        list.innerHTML = '<div class="text-xs text-gray-500 text-center py-4">Belum ada insight. Jalankan analysis dulu.</div>'
        return
      }
      list.innerHTML = data.insights.map(i => \`
        <div class="glass rounded-lg p-2 priority-\${i.priority} cursor-pointer hover:bg-white/5" onclick="markRead('\${i.id}')">
          <div class="flex justify-between items-start">
            <span class="text-xs font-medium text-white">\${i.title}</span>
            \${!i.is_read ? '<span class="w-2 h-2 rounded-full bg-blue-400 mt-1 flex-shrink-0"></span>' : ''}
          </div>
          <p class="text-[11px] text-gray-400 mt-1 line-clamp-2">\${i.content}</p>
          <div class="flex justify-between mt-1">
            <span class="text-[10px] text-gray-500">\${i.insight_type}</span>
            <span class="text-[10px] px-1 rounded \${
              i.priority === 'critical' ? 'text-red-400' : 
              i.priority === 'high' ? 'text-yellow-400' : 
              'text-blue-400'}">\${i.priority.toUpperCase()}</span>
          </div>
        </div>
      \`).join('')
    }

    async function loadTasks() {
      const data = await apiCall('/ai/intelligence/tasks')
      const list = document.getElementById('tasksList')
      document.getElementById('taskCount').textContent = \`\${data.count || 0} tasks\`
      if (!data.tasks || data.tasks.length === 0) {
        list.innerHTML = '<div class="text-xs text-gray-500 text-center py-4">Belum ada tasks aktif.</div>'
        return
      }
      const statusColor = { pending: 'text-yellow-400', running: 'text-blue-400', completed: 'text-green-400', failed: 'text-red-400', pending_human: 'text-orange-400' }
      list.innerHTML = data.tasks.map(t => \`
        <div class="glass rounded-lg p-2">
          <div class="flex justify-between items-center">
            <span class="text-xs font-medium">\${t.task_type}</span>
            <span class="text-[10px] \${statusColor[t.status] || 'text-gray-400'}">\${t.status.toUpperCase()}</span>
          </div>
          <div class="text-[10px] text-gray-500 mt-1">
            \${t.agent_type} · \${new Date(t.created_at).toLocaleString('id-ID', {hour:'2-digit',minute:'2-digit',day:'2-digit',month:'short'})}
          </div>
          \${t.status === 'pending_human' ? \`
            <div class="flex gap-1 mt-2">
              <button onclick="approveTask('\${t.id}', true)" class="text-[10px] px-2 py-0.5 bg-green-900/50 text-green-300 rounded">✅ Approve</button>
              <button onclick="approveTask('\${t.id}', false)" class="text-[10px] px-2 py-0.5 bg-red-900/50 text-red-300 rounded">❌ Reject</button>
            </div>
          \` : ''}
        </div>
      \`).join('')
    }

    async function runCrew(type) {
      const statusEl = document.getElementById('crewStatus')
      statusEl.innerHTML = \`<i class="fas fa-spinner fa-spin mr-1"></i>Starting \${type}...\`
      
      const endpoint = type === 'kickoff' ? '/ai/crew/kickoff' : \`/ai/crew/\${type}\`
      const data = await apiCall(endpoint, 'POST', { inputs: {} })
      
      if (data.success) {
        statusEl.innerHTML = \`<span class="text-green-400">✅ \${type} started — Task ID: \${data.task_id || 'N/A'}</span>\`
        setTimeout(() => loadTasks(), 2000)
      } else {
        statusEl.innerHTML = \`<span class="text-red-400">❌ Error: \${data.error || 'Unknown error'}</span>\`
      }
    }

    async function markRead(id) {
      await apiCall(\`/ai/intelligence/insights/\${id}/read\`, 'PATCH')
      loadInsights()
    }

    async function approveTask(id, approved) {
      await apiCall('/ai/resume-thread', 'POST', { taskId: id, approved })
      loadTasks()
    }

    function refreshAll() {
      loadAgents()
      loadInsights()
      loadTasks()
    }

    // Initial load
    refreshAll()
    
    // Auto-refresh every 30 seconds
    setInterval(refreshAll, 30000)
  </script>
</body>
</html>`)
})
```

---

### Task 4 — Update Navigation Sidebar [~10 credits]

Di `src/index.tsx` atau template partial, tambahkan "AI" ke sidebar navigation:

```html
<!-- Tambahkan di sidebar navigation items -->
<a href="/ai" class="nav-item flex items-center gap-3 px-4 py-2.5 rounded-lg hover:bg-white/5 transition text-gray-400 hover:text-white">
  <i class="fas fa-brain w-5 text-center"></i>
  <span>AI Intelligence</span>
</a>
```

---

### Task 5 — Mount Intelligence Router [~5 credits]

Di `src/index.tsx`:

```typescript
import intelligenceRouter from './routes/intelligence'

// Add after existing route mounts
app.route('/api/ai/intelligence', intelligenceRouter)
```

---

### Task 6 — Build, Test & Deploy [~15 credits]

```bash
npm run build

fuser -k 3000/tcp 2>/dev/null || true
pm2 restart sovereign
sleep 4

# Test AI intelligence page
curl -s http://localhost:3000/ai | head -20

# Test intelligence API
curl -s http://localhost:3000/api/ai/intelligence/status
# Expected: {"success":true,"total_agents":12,...}

curl -s http://localhost:3000/api/ai/intelligence/insights
# Expected: {"success":true,"insights":[...],"count":...}

# Deploy
npx wrangler pages deploy dist --project-name sovereign-orchestrator

# Git push
git add -A
git commit -m "feat: Session 5 - AI Intelligence Center UI + API

- New /ai page with Terminal-Chic glassmorphism design
- 12-agent status grid (4 LangGraph + 8 CrewAI)
- AI Insights feed with priority levels and read tracking
- Task Queue with human-in-loop approval UI
- Run Analysis buttons (churn, upsell, validation, engagement)
- Auto-refresh every 30 seconds
- New /api/ai/intelligence/* routes
- Version bump to v4.5"
git push origin main
```

---

## 📊 WHAT SHOULD BE DELIVERED

```yaml
New UI Pages:
  /ai - AI Intelligence Center: ✅

New API Routes:
  GET /api/ai/intelligence/status: ✅
  GET /api/ai/intelligence/insights: ✅
  POST /api/ai/intelligence/insights: ✅
  PATCH /api/ai/intelligence/insights/:id/read: ✅
  GET /api/ai/intelligence/tasks: ✅

Features Working:
  Agent status grid (12 agents): ✅
  Insights feed: ✅
  Task queue: ✅
  Run analysis buttons: ✅
  Human-in-loop approval: ✅
  Auto-refresh 30s: ✅

Mobile Responsive: ✅
Deployed: v4.5 ✅
GitHub: pushed ✅
```

---

## ⚠️ CRITICAL NOTES

1. **JWT Token**: Halaman `/ai` butuh valid JWT. Pastikan user sudah login. Redirect ke PIN gate jika tidak ada token.

2. **ai_tasks Table**: Harus dibuat sebelum halaman AI bisa menampilkan task queue. Cek di Session #001 apakah sudah dibuat.

3. **Glassmorphism CSS**: Style harus konsisten dengan design system yang sudah ada di halaman lain (glass card dengan rgba(255,255,255,0.05)).

---

## 💡 NOTES FOR SESSION #006

Session #006 fokus ke **Fonnte Live Integration** dan auto-sequence Day 0/3/7/14.
Ini adalah milestone paling penting untuk outreach automation!

**Prerequisites untuk Session #006:**
- [ ] Fonnte token SUDAH ADA (critical!)
- [ ] Session #005 complete (AI Intelligence page ready)

---

## 🎉 FILL THIS AFTER SESSION #005 COMPLETE

```
SESSION #005 ACTUAL RESULTS:
  Credits Used: __ credits (estimate: 90-109)
  Duration: __ minutes
  
DELIVERABLES:
  /ai page: [✅/❌]
  Agent status grid: [✅/❌]
  Insights feed: [✅/❌]
  Task queue: [✅/❌]
  Deployed: [✅/❌]
  
BLOCKERS: [describe]
NOTES FOR SESSION #006: [context]

PRODUCTION HEALTH:
  https://sovereign-orchestrator.pages.dev/ai → 200 OK
  https://sovereign-orchestrator.pages.dev/api/ai/intelligence/status → {"total_agents":12}
  Version: v4.5
```

---

*Session Handoff #005 | Sovereign Business Engine | CONFIDENTIAL | Haidar Faras*
