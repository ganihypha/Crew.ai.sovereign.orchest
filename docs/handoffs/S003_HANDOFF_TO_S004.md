# 🎯 MASTER SESSION HANDOFF #003 → #004
## SOVEREIGN BUSINESS ENGINE — Phase 3: LangGraph.js v2 + RAG Memory

**Session**: #003
**Status**: ⏳ PENDING — Dimulai Setelah Session #002 Complete
**Prerequisite**: Session #002 done (pgvector + embeddings table + OpenAI key WAJIB)
**Next Session Budget**: 100 credits

---

## ♾️ INFINITE GROWTH LOOP STATUS

```yaml
Session #3 Projection:
  Efficiency: 84%
  Knowledge: 1.30 (pgvector expertise + RAG patterns gained)
  Expected Output: ~100 × 0.84 × 1.30 = 109.2 effective credits

Prediction for Session #4:
  Efficiency: 86%
  Knowledge: 1.45 (CrewAI Python expertise added)
  Expected Output: ~100 × 0.86 × 1.45 = 124.7 effective credits
  Improvement: +14% vs Session #3!
```

---

## 📋 SESSION #003 GOALS

### Primary Objectives
1. **Install @langchain/community + @langchain/openai** di webapp
2. **Upgrade MessageComposer → v2** dengan pgvector RAG memory
3. **Buat PricingOptimizer agent** (LangGraph.js)
4. **Buat RAG query endpoint** `/api/ai/rag/query`
5. **Buat human-in-loop resume** endpoint
6. **Deploy & push**

### Success Criteria
- [ ] `npm install` sukses dengan packages baru (zero peer dep errors)
- [ ] `/api/closer/ai-compose` menggunakan MessageComposerV2 (RAG-aware)
- [ ] `/api/ai/rag/query` return hasil similarity search
- [ ] `/api/pricing/suggest/:productId` return pricing recommendation
- [ ] `/api/ai/resume-thread` endpoint exists
- [ ] Build `dist/_worker.js` < 300KB (workers size limit check)
- [ ] Deployed & verified

---

## ✅ VERIFY SESSION #002 COMPLETE

```bash
# Check pgvector
curl -s "https://lfohzibcsafqthupcvdg.supabase.co/rest/v1/rpc/match_documents" \
  -H "apikey: <SUPABASE_ANON_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"query_embedding":[0.1,0.2],"match_count":1}' | head -20
# Expected: [] atau data (NOT error)

# Check embeddings table
curl -s "https://lfohzibcsafqthupcvdg.supabase.co/rest/v1/embeddings?select=id&limit=1" \
  -H "apikey: <SUPABASE_ANON_KEY>" | python3 -c "import sys,json; print('embeddings OK')"
```

---

## ⚙️ SESSION #003 SETUP

```bash
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git" webapp
cd webapp && npm install
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"
# .dev.vars WAJIB include OPENAI_API_KEY=<your-openai-key>
npm run build
fuser -k 3000/tcp 2>/dev/null || true
pm2 start ecosystem.config.cjs
sleep 3 && curl http://localhost:3000/api/health
```

---

## 🛠️ TASK BREAKDOWN SESSION #003

### Task 1 — Install New Dependencies [~5 credits]

```bash
cd /home/user/webapp
npm install @langchain/community @langchain/openai

# Verify package sizes (workers size limit: 10MB compressed)
npm run build 2>&1 | grep -E "worker.js|kB|MB"
# Expected: dist/_worker.js < 500kB (monitor!)
```

**⚠️ PENTING**: Jika bundle size > 5MB setelah install, pertimbangkan:
- Pindahkan embedding generation ke Supabase Edge Function
- Atau gunakan Cloudflare Workers AI untuk embedding (bukan OpenAI)

---

### Task 2 — Upgrade MessageComposer v2 dengan RAG [~30 credits]

Buat file `src/agents/messageComposerV2.ts`:

```typescript
// src/agents/messageComposerV2.ts
// MessageComposer v2: Context-aware dengan pgvector RAG memory

import { StateGraph, END } from "@langchain/langgraph/web"
import { ChatOpenAI } from "@langchain/openai"
import { SupabaseVectorStore } from "@langchain/community/vectorstores/supabase"
import { OpenAIEmbeddings } from "@langchain/openai"
import { createClient } from '@supabase/supabase-js'

interface MessageState {
  lead_id: string
  lead_data: any
  lead_score: number
  memory_context: string
  final_message: string
  requires_human: boolean
  error?: string
}

export function createMessageComposerV2(env: any) {
  const supabaseClient = createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY)
  const llm = new ChatOpenAI({
    modelName: "gpt-4o-mini",
    temperature: 0.7,
    openAIApiKey: env.OPENAI_API_KEY,
    maxTokens: 300
  })

  const builder = new StateGraph<MessageState>({
    channels: {
      lead_id: { value: (a: string) => a },
      lead_data: { value: (a: any) => a },
      lead_score: { value: (a: number) => a },
      memory_context: { value: (a: string, b: string) => b || a, default: () => "" },
      final_message: { value: (a: string, b: string) => b || a, default: () => "" },
      requires_human: { value: (a: boolean) => a, default: () => false }
    }
  })

  // Node 1: Fetch historical context via RAG
  builder.addNode("fetch_memory", async (state: MessageState) => {
    try {
      const vectorStore = await SupabaseVectorStore.fromExistingIndex(
        new OpenAIEmbeddings({ openAIApiKey: env.OPENAI_API_KEY, modelName: "text-embedding-3-small" }),
        { client: supabaseClient, tableName: "embeddings", queryName: "match_documents" }
      )
      const docs = await vectorStore.similaritySearch(
        `lead_id:${state.lead_id} whatsapp history outreach`,
        3
      )
      return { memory_context: docs.map(d => d.pageContent).join("\n---\n") || "Belum ada riwayat." }
    } catch {
      return { memory_context: "Riwayat tidak tersedia." }
    }
  })

  // Node 2: Compose RAG-aware message
  builder.addNode("compose", async (state: MessageState) => {
    const lead = state.lead_data
    const systemPrompt = `Kamu adalah Closer Agent untuk FashionKas, bisnis fashion reseller Indonesia.
Gaya: hangat, casual, persuasif. Bahasa: Indonesia gaul.
Riwayat komunikasi sebelumnya:
${state.memory_context}

Data lead:
- Toko: ${lead?.shop_name || 'N/A'}
- Platform: ${lead?.platform || 'Instagram'}
- Followers: ${lead?.followers || 'N/A'}
- Score: ${state.lead_score}/100

Tulis pesan WhatsApp pembuka yang natural. Max 3 kalimat. Jangan terlalu salesy.`

    const res = await llm.invoke(systemPrompt)
    return { final_message: res.content as string }
  })

  // Node 3: Check if high-value lead needs human review
  builder.addNode("check_escalate", (state: MessageState) => {
    return { requires_human: state.lead_score > 85 }
  })

  // Node 4: Human review placeholder
  builder.addNode("human_review", async (state: MessageState) => {
    // This node pauses execution — message goes to review queue
    await supabaseClient.from('ai_tasks').insert({
      agent_type: 'langgraph',
      task_type: 'human_review',
      input_data: { lead_id: state.lead_id, draft_message: state.final_message, lead_score: state.lead_score },
      status: 'pending_human'
    })
    return {}
  })

  builder.setEntryPoint("fetch_memory")
  builder.addEdge("fetch_memory", "compose")
  builder.addEdge("compose", "check_escalate")
  builder.addConditionalEdges("check_escalate", (s: MessageState) => s.requires_human ? "human_review" : END, {
    human_review: "human_review",
    [END]: END
  })
  builder.addEdge("human_review", END)

  return builder.compile({ interruptBefore: ["human_review"] })
}
```

---

### Task 3 — Buat PricingOptimizer Agent [~20 credits]

Buat file `src/agents/pricingOptimizer.ts`:

```typescript
// src/agents/pricingOptimizer.ts
import { StateGraph, END } from "@langchain/langgraph/web"
import { ChatOpenAI } from "@langchain/openai"

interface PricingState {
  product_id: string
  product_data: any
  competitor_data: any[]
  pricing_suggestion: { old_price: number; new_price: number; reasoning: string; confidence: number } | null
}

export function createPricingOptimizer(env: any) {
  const llm = new ChatOpenAI({
    modelName: "gpt-4o-mini",
    temperature: 0.2,
    openAIApiKey: env.OPENAI_API_KEY,
    maxTokens: 500
  })

  const builder = new StateGraph<PricingState>({
    channels: {
      product_id: { value: (a: string) => a },
      product_data: { value: (a: any) => a },
      competitor_data: { value: (a: any[]) => a, default: () => [] },
      pricing_suggestion: { value: (a: any) => a, default: () => null }
    }
  })

  builder.addNode("calculate_price", async (state: PricingState) => {
    const prompt = `Kamu adalah pricing strategist untuk bisnis fashion Indonesia.

Produk saat ini: ${JSON.stringify(state.product_data)}
Data kompetitor: ${JSON.stringify(state.competitor_data.slice(0, 3))}

Hitung harga optimal dengan:
- Margin minimum 30%
- Tetap kompetitif vs kompetitor
- Harga tidak boleh naik/turun lebih dari 20% dari harga saat ini

Response JSON ONLY:
{"new_price": <number>, "reasoning": "<max 50 words>", "confidence": <0-1>}`

    const res = await llm.invoke(prompt)
    try {
      const parsed = JSON.parse(res.content as string)
      return {
        pricing_suggestion: {
          old_price: state.product_data?.price || 0,
          ...parsed
        }
      }
    } catch {
      return { pricing_suggestion: { old_price: state.product_data?.price || 0, new_price: state.product_data?.price || 0, reasoning: "Parse error - keeping current price", confidence: 0 } }
    }
  })

  builder.setEntryPoint("calculate_price")
  builder.addEdge("calculate_price", END)
  return builder.compile()
}
```

---

### Task 4 — Update API Routes [~15 credits]

Di `src/routes/closer.ts` atau `src/index.tsx`:

```typescript
// Update POST /api/closer/ai-compose → gunakan V2
app.post('/api/closer/ai-compose', jwtMiddleware, async (c) => {
  const { leadId, leadData, leadScore } = await c.req.json()
  const composer = createMessageComposerV2(c.env)
  const result = await composer.invoke({ lead_id: leadId, lead_data: leadData, lead_score: leadScore || 50 })
  return c.json({
    success: true,
    message: result.final_message,
    requires_human: result.requires_human,
    rag_used: result.memory_context !== "Riwayat tidak tersedia."
  })
})

// NEW: GET /api/pricing/suggest/:productId
app.get('/api/pricing/suggest/:productId', jwtMiddleware, async (c) => {
  const productId = c.req.param('productId')
  const { data: product } = await supabase(c.env).from('products').select('*').eq('id', productId).single()
  if (!product) return c.json({ success: false, error: 'Product not found' }, 404)
  
  const { data: competitors } = await supabase(c.env).from('competitor_intel').select('*').order('scraped_at', { ascending: false }).limit(5)
  
  const optimizer = createPricingOptimizer(c.env)
  const result = await optimizer.invoke({ product_id: productId, product_data: product, competitor_data: competitors || [] })
  
  return c.json({ success: true, suggestion: result.pricing_suggestion, product })
})

// NEW: POST /api/ai/rag/query
app.post('/api/ai/rag/query', jwtMiddleware, async (c) => {
  const { query, limit = 5 } = await c.req.json()
  if (!c.env.OPENAI_API_KEY) return c.json({ success: false, error: 'OpenAI key not configured' }, 503)
  
  // Generate embedding
  const embRes = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${c.env.OPENAI_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'text-embedding-3-small', input: query })
  })
  const embData = await embRes.json() as any
  const embedding = embData.data?.[0]?.embedding
  
  if (!embedding) return c.json({ success: false, error: 'Embedding generation failed' }, 500)
  
  const { data } = await supabase(c.env).rpc('match_documents', { query_embedding: embedding, match_count: limit })
  return c.json({ success: true, results: data || [], count: data?.length || 0 })
})

// NEW: POST /api/ai/resume-thread (human-in-loop approval)
app.post('/api/ai/resume-thread', jwtMiddleware, async (c) => {
  const { taskId, approved, overrideMessage } = await c.req.json()
  
  const updateData: any = { status: approved ? 'approved' : 'rejected', completed_at: new Date().toISOString() }
  if (overrideMessage) updateData.output_data = { approved_message: overrideMessage }
  
  const { data } = await supabase(c.env).from('ai_tasks').update(updateData).eq('id', taskId).select().single()
  return c.json({ success: true, task: data, status: approved ? 'approved' : 'rejected' })
})
```

---

### Task 5 — Build, Test & Deploy [~10 credits]

```bash
# Build (monitor bundle size!)
npm run build 2>&1
echo "Worker size:"
ls -lh dist/_worker.js

# Start & test
fuser -k 3000/tcp 2>/dev/null || true
pm2 restart sovereign
sleep 4

# Test RAG endpoint
curl -s -X POST http://localhost:3000/api/ai/rag/query \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"query":"fashion reseller outreach","limit":3}'

# Deploy
npx wrangler pages deploy dist --project-name sovereign-orchestrator
npx wrangler pages secret put OPENAI_API_KEY --project-name sovereign-orchestrator
# (paste OpenAI key when prompted)

# Git push
git add -A
git commit -m "feat: Session 3 - LangGraph v2 RAG + PricingOptimizer + RAG query API

- MessageComposerV2: context-aware with pgvector RAG memory
- PricingOptimizer: AI pricing suggestions via GPT-4o-mini
- POST /api/ai/rag/query: similarity search on embeddings
- GET /api/pricing/suggest/:id: product pricing recommendation
- POST /api/ai/resume-thread: human-in-loop task approval
- Version bump to v3.9"
git push origin main
```

---

## 📊 WHAT SHOULD BE DELIVERED

```yaml
New Packages:
  @langchain/community: ✅ Installed
  @langchain/openai: ✅ Installed

New Agents:
  MessageComposerV2: ✅ (with RAG memory)
  PricingOptimizer: ✅ (with competitor context)

New API Routes:
  POST /api/ai/rag/query: ✅
  GET /api/pricing/suggest/:id: ✅
  POST /api/ai/resume-thread: ✅
  POST /api/closer/ai-compose: ✅ (upgraded to V2)

Secrets (Cloudflare):
  OPENAI_API_KEY: ✅ Set via wrangler secret put

Bundle Size: < 500kB ✅ (critical check!)
Deployed: v3.9 ✅
GitHub: pushed ✅
```

---

## ⚠️ CRITICAL NOTES

1. **Bundle Size**: LangChain packages bisa besar. Jika `_worker.js` > 1MB compressed, perlu:
   - Lazy import atau tree-shaking
   - Atau pindahkan ke route yang hanya load saat dibutuhkan

2. **OpenAI API Cost**: `text-embedding-3-small` = $0.02/1M tokens. Sangat murah tapi track usage.

3. **Cloudflare Workers CPU Limit**: Jika ada error `CPU exceeded`, berarti LangGraph workflow terlalu berat → simplify ke direct OpenAI call.

---

## 💡 NOTES FOR SESSION #004

Session #004 fokus ke **CrewAI Python v4.0 upgrade** — bukan di webapp TypeScript.
Perlu clone repo `Crew.ai.sovereign.orchest` dan tambah 4 agen baru.

**Prerequisites untuk Session #004:**
- [ ] Session #003 complete
- [ ] Fonnte token ada (untuk churn_detector agent)

---

## 🎉 FILL THIS AFTER SESSION #003 COMPLETE

```
SESSION #003 ACTUAL RESULTS:
  Credits Used: __ credits (estimate: 95-109)
  Duration: __ minutes
  
DELIVERABLES:
  MessageComposerV2: [✅/❌]
  PricingOptimizer: [✅/❌]
  RAG query endpoint: [✅/❌]
  Bundle size: __ kB
  Deployed: [✅/❌]
  
BLOCKERS: [describe]
NOTES FOR SESSION #004: [context]

PRODUCTION HEALTH:
  https://sovereign-orchestrator.pages.dev/api/health → Version: v3.9
```

---

*Session Handoff #003 | Sovereign Business Engine | CONFIDENTIAL | Haidar Faras*
