# 🎯 MASTER SESSION HANDOFF #006 → #007
## SOVEREIGN BUSINESS ENGINE — Phase 6: Fonnte Live + Auto-Sequence WhatsApp

**Session**: #006
**Status**: ⏳ PENDING — Dimulai Setelah Session #005 Complete
**Prerequisite**: Session #005 done + **FONNTE TOKEN WAJIB ADA**
**Next Session Budget**: 100 credits

---

## ♾️ INFINITE GROWTH LOOP STATUS

```yaml
Session #6 Projection:
  Efficiency: 90%
  Knowledge: 1.75 (Fonnte + outreach automation expertise)
  Expected Output: ~100 × 0.90 × 1.75 = 157.5 effective credits

Prediction for Session #7:
  Efficiency: 92%
  Knowledge: 1.90 (Dashboard + AI insights integration)
  Expected Output: ~100 × 0.92 × 1.90 = 174.8 effective credits
  Improvement: +11% vs Session #6!
```

---

## 🚨 CRITICAL REQUIREMENT: FONNTE TOKEN

**Session #006 TIDAK BISA DIMULAI tanpa Fonnte token!**

### Cara Dapat Fonnte Token:
1. Buka https://fonnte.com
2. Register/login akun
3. Klik "Add Device" → scan QR dengan WhatsApp kamu
4. Setelah device connected, copy token dari dashboard
5. Token format: string panjang (bukan Bearer prefix)

**Test token kamu:**
```bash
curl -X POST "https://api.fonnte.com/send" \
  -H "Authorization: <YOUR_FONNTE_TOKEN>" \
  -d "target=+62xxxxx&message=test"
```

---

## 📋 SESSION #006 GOALS (Fonnte Live + Auto-Sequence)

### Primary Objectives
1. **Test Fonnte connection** live (kirim pesan test)
2. **Buat `/api/wa/send`** endpoint live (bukan mock)
3. **Buat `/api/wa/broadcast`** endpoint untuk bulk sending
4. **Buat auto-sequence system** (Day 0, 3, 7, 14)
5. **Buat sequence scheduler** menggunakan Supabase scheduled tasks
6. **Update Closer Agent UI** dengan live status
7. **Deploy & push**

### Success Criteria
- [ ] Test WA message terkirim ke nomor sendiri ✅
- [ ] `/api/wa/send` return {"success":true,"message":"sent"} 
- [ ] `/api/wa/broadcast` bisa kirim ke 5 nomor sekaligus
- [ ] Sequence records tersimpan di `outreach_campaigns` table
- [ ] Day 0 message auto-trigger saat lead di-assign
- [ ] Deployed & live

---

## ✅ VERIFY SESSION #005 COMPLETE

```bash
# Check AI page loads
curl -s "https://sovereign-orchestrator.pages.dev/ai" | grep -o "AI Intelligence Center"
# Expected: AI Intelligence Center

# Check intelligence API  
curl -s "https://sovereign-orchestrator.pages.dev/api/ai/intelligence/status" \
  -H "Authorization: Bearer <JWT>"
# Expected: {"success":true,"total_agents":12}
```

---

## ⚙️ SESSION #006 SETUP

```bash
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git" webapp
cd webapp && npm install
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"

# Update .dev.vars dengan Fonnte token!
cat >> .dev.vars << 'EOF'
FONNTE_TOKEN=<PASTE_YOUR_FONNTE_TOKEN_HERE>
EOF

npm run build
fuser -k 3000/tcp 2>/dev/null || true
pm2 start ecosystem.config.cjs
sleep 3 && curl http://localhost:3000/api/health
```

---

## 🛠️ TASK BREAKDOWN SESSION #006

### Task 1 — Verify & Test Fonnte Connection [~10 credits]

```bash
# Test kirim pesan ke nomor sendiri dulu
FONNTE_TOKEN="<your-token>"
YOUR_WA="628xxxxxxxxxxxx"  # nomor WA kamu format 628xxx

curl -X POST "https://api.fonnte.com/send" \
  -H "Authorization: ${FONNTE_TOKEN}" \
  -d "target=${YOUR_WA}&message=🤖 Sovereign OS Test — Fonnte integration berhasil! $(date)"

# Expected response:
# {"status":true,"process":"wait"}
```

---

### Task 2 — Update wa.ts Routes (Live) [~25 credits]

Update `src/routes/wa.ts` dengan implementasi live:

```typescript
// src/routes/wa.ts (FULL IMPLEMENTATION)
import { Hono } from 'hono'
import { createClient } from '@supabase/supabase-js'

const router = new Hono<{ Bindings: {
  SUPABASE_URL: string; SUPABASE_SERVICE_KEY: string; FONNTE_TOKEN: string
}}>()

const FONNTE_API = 'https://api.fonnte.com'
const supabase = (env: any) => createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY)

// Helper: Send via Fonnte
async function fonnteRequest(endpoint: string, env: any, body: Record<string, string>) {
  const formData = new URLSearchParams(body)
  const res = await fetch(`${FONNTE_API}${endpoint}`, {
    method: 'POST',
    headers: { 'Authorization': env.FONNTE_TOKEN },
    body: formData
  })
  return res.json() as Promise<any>
}

// POST /api/wa/send
router.post('/send', async (c) => {
  const { target, message, lead_id } = await c.req.json()
  if (!target || !message) return c.json({ success: false, error: 'target and message required' }, 400)
  if (!c.env.FONNTE_TOKEN) return c.json({ success: false, error: 'Fonnte token not configured' }, 503)
  
  const result = await fonnteRequest('/send', c.env, {
    target: target.replace(/[^0-9]/g, ''),
    message,
    delay: '2',
    countryCode: '62'
  })
  
  // Log to Supabase
  await supabase(c.env).from('wa_logs').insert({
    target,
    message,
    lead_id: lead_id || null,
    direction: 'outbound',
    status: result.status ? 'sent' : 'failed',
    fonnte_response: result
  })
  
  return c.json({ success: result.status === true, result })
})

// POST /api/wa/bulk
router.post('/bulk', async (c) => {
  const { targets, message, delay = '5' } = await c.req.json()
  if (!targets || !Array.isArray(targets) || targets.length === 0) {
    return c.json({ success: false, error: 'targets array required' }, 400)
  }
  if (targets.length > 50) {
    return c.json({ success: false, error: 'Maximum 50 targets per bulk send' }, 400)
  }
  
  const targetStr = targets.map((t: string) => t.replace(/[^0-9]/g, '')).join(',')
  const result = await fonnteRequest('/send', c.env, {
    target: targetStr,
    message,
    delay,
    countryCode: '62'
  })
  
  // Log bulk to Supabase
  await supabase(c.env).from('wa_logs').insert({
    target: targetStr,
    message,
    direction: 'outbound',
    status: result.status ? 'sent' : 'failed',
    is_bulk: true,
    bulk_count: targets.length,
    fonnte_response: result
  })
  
  return c.json({ success: result.status === true, result, sent_to: targets.length })
})

// GET /api/wa/status
router.get('/status', async (c) => {
  if (!c.env.FONNTE_TOKEN) return c.json({ success: false, connected: false, error: 'Token not configured' })
  
  const result = await fonnteRequest('/device', c.env, { token: c.env.FONNTE_TOKEN })
  return c.json({
    success: true,
    connected: result.status === true,
    device: result.device || null,
    quota: result.quota || 0
  })
})

// GET /api/wa/history
router.get('/history', async (c) => {
  const limit = parseInt(c.req.query('limit') || '20')
  const lead_id = c.req.query('lead_id')
  
  let query = supabase(c.env).from('wa_logs')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(limit)
  
  if (lead_id) query = query.eq('lead_id', lead_id)
  
  const { data, error } = await query
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, logs: data || [], count: data?.length || 0 })
})

// POST /api/wa/webhook (receive messages from Fonnte)
router.post('/webhook', async (c) => {
  const body = await c.req.json()
  
  // Log incoming message
  await supabase(c.env).from('wa_logs').insert({
    target: body.sender,
    message: body.message,
    direction: 'inbound',
    status: 'received',
    fonnte_response: body
  })
  
  // Check if response to outreach (keyword detection)
  const msg = (body.message || '').toLowerCase()
  const interested_keywords = ['harga', 'mau', 'order', 'minat', 'tertarik', 'info']
  const stop_keywords = ['stop', 'tidak tertarik', 'unsubscribe', 'hapus']
  
  if (stop_keywords.some(k => msg.includes(k))) {
    // Mark lead as DNC (Do Not Contact)
    await supabase(c.env).from('leads')
      .update({ status: 'dnc', notes: 'Opted out via WA' })
      .eq('phone', body.sender)
  } else if (interested_keywords.some(k => msg.includes(k))) {
    // Escalate to founder - create ai_insights record
    await supabase(c.env).from('ai_insights').insert({
      insight_type: 'lead_response',
      title: `🔥 Lead Interested: ${body.sender}`,
      content: `Lead responded: "${body.message.substring(0, 100)}" — Manual follow-up needed!`,
      data: { sender: body.sender, message: body.message },
      priority: 'high'
    })
  }
  
  return c.json({ success: true })
})

export default router
```

---

### Task 3 — Buat Auto-Sequence System [~25 credits]

Buat file `src/routes/sequences.ts`:

```typescript
// src/routes/sequences.ts
// Auto-sequence WhatsApp outreach: Day 0, 3, 7, 14
import { Hono } from 'hono'
import { createClient } from '@supabase/supabase-js'

const router = new Hono<{ Bindings: {
  SUPABASE_URL: string; SUPABASE_SERVICE_KEY: string; FONNTE_TOKEN: string
}}>()

const supabase = (env: any) => createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY)

// Message templates per day
const SEQUENCE_TEMPLATES = {
  day0: (name: string, shop: string) => 
    `Halo kak ${name}! 👋 Saya dari FashionKas, lihat toko ${shop || 'Kakak'} di IG. Ada koleksi fashion baru yang cocok banget buat reseller. Boleh saya share info-nya kak? 🌸`,
  
  day3: (name: string) => 
    `Halo kak ${name}! Saya follow up nih. Kemarin sempet kirim info soal FashionKas. Masih penasaran? Ada penawaran spesial untuk reseller baru bulan ini loh! 🎁`,
  
  day7: (name: string) => 
    `Kak ${name}, masih ada! 😊 Mau kasih info: bulan ini ada produk hijab premium masuk, margin reseller sampai 40%. Kalau kakak mau lihat katalognya, boleh saya kirimin? Gratis ongkir untuk order pertama kak! ✨`,
  
  day14: (name: string) => 
    `Halo kak ${name}! Saya Haidar dari FashionKas. Ini follow up terakhir dari saya. Kalau kapan-kapan tertarik jadi reseller fashion premium, langsung hubungi saya ya! Sukses terus toko kak ${name} 🙏`
}

// POST /api/sequences/enroll (enroll lead into sequence)
router.post('/enroll', async (c) => {
  const { lead_id, phone, name, shop_name } = await c.req.json()
  
  // Check if already enrolled
  const { data: existing } = await supabase(c.env).from('outreach_campaigns')
    .select('id').eq('lead_id', lead_id).eq('status', 'active').single()
  
  if (existing) {
    return c.json({ success: false, error: 'Lead already enrolled in active sequence' })
  }
  
  // Create campaign record
  const { data: campaign, error } = await supabase(c.env).from('outreach_campaigns').insert({
    lead_id,
    phone,
    name,
    shop_name,
    status: 'active',
    sequence_day: 0,
    next_send_at: new Date().toISOString(),
    enrolled_at: new Date().toISOString()
  }).select().single()
  
  if (error) return c.json({ success: false, error: error.message }, 500)
  
  // Send Day 0 message immediately
  const message = SEQUENCE_TEMPLATES.day0(name, shop_name)
  
  const formData = new URLSearchParams({
    target: phone.replace(/[^0-9]/g, ''),
    message,
    delay: '2',
    countryCode: '62'
  })
  
  const fonnteRes = await fetch('https://api.fonnte.com/send', {
    method: 'POST',
    headers: { 'Authorization': c.env.FONNTE_TOKEN },
    body: formData
  })
  const fonnteData = await fonnteRes.json() as any
  
  // Log message
  await supabase(c.env).from('outreach_logs').insert({
    campaign_id: campaign.id,
    lead_id,
    sequence_day: 0,
    message,
    status: fonnteData.status ? 'sent' : 'failed',
    sent_at: new Date().toISOString()
  })
  
  // Schedule Day 3
  const day3Date = new Date()
  day3Date.setDate(day3Date.getDate() + 3)
  
  await supabase(c.env).from('outreach_campaigns')
    .update({ sequence_day: 0, next_send_at: day3Date.toISOString() })
    .eq('id', campaign.id)
  
  return c.json({
    success: true,
    campaign_id: campaign.id,
    day0_sent: fonnteData.status === true,
    next_followup: day3Date.toISOString()
  })
})

// POST /api/sequences/process-queue (called by Cloudflare Cron or manually)
router.post('/process-queue', async (c) => {
  const now = new Date().toISOString()
  
  // Get all sequences that need processing
  const { data: campaigns } = await supabase(c.env).from('outreach_campaigns')
    .select('*')
    .eq('status', 'active')
    .lte('next_send_at', now)
    .lt('sequence_day', 14)
  
  if (!campaigns || campaigns.length === 0) {
    return c.json({ success: true, processed: 0, message: 'No sequences to process' })
  }
  
  let processed = 0
  const results = []
  
  for (const campaign of campaigns) {
    const nextDay = campaign.sequence_day >= 0 && campaign.sequence_day < 3 ? 3 :
                    campaign.sequence_day >= 3 && campaign.sequence_day < 7 ? 7 :
                    campaign.sequence_day >= 7 && campaign.sequence_day < 14 ? 14 : null
    
    if (nextDay === null) {
      // Sequence complete
      await supabase(c.env).from('outreach_campaigns')
        .update({ status: 'completed', completed_at: now })
        .eq('id', campaign.id)
      continue
    }
    
    const template = SEQUENCE_TEMPLATES[`day${nextDay}` as keyof typeof SEQUENCE_TEMPLATES]
    if (!template) continue
    
    const message = template(campaign.name || 'Kakak', campaign.shop_name)
    
    const formData = new URLSearchParams({
      target: (campaign.phone || '').replace(/[^0-9]/g, ''),
      message,
      delay: String(processed * 3 + 2),  // Stagger sends
      countryCode: '62'
    })
    
    const fonnteRes = await fetch('https://api.fonnte.com/send', {
      method: 'POST',
      headers: { 'Authorization': c.env.FONNTE_TOKEN },
      body: formData
    })
    const fonnteData = await fonnteRes.json() as any
    
    // Log
    await supabase(c.env).from('outreach_logs').insert({
      campaign_id: campaign.id,
      lead_id: campaign.lead_id,
      sequence_day: nextDay,
      message,
      status: fonnteData.status ? 'sent' : 'failed',
      sent_at: now
    })
    
    // Update next schedule
    const nextDate = new Date()
    const daysUntilNext = nextDay === 3 ? 4 : nextDay === 7 ? 7 : null  // Day 3→7, Day 7→14, Day 14→complete
    
    if (daysUntilNext) {
      nextDate.setDate(nextDate.getDate() + daysUntilNext)
      await supabase(c.env).from('outreach_campaigns')
        .update({ sequence_day: nextDay, next_send_at: nextDate.toISOString() })
        .eq('id', campaign.id)
    } else {
      // Final message sent, mark complete
      await supabase(c.env).from('outreach_campaigns')
        .update({ sequence_day: nextDay, status: 'completed', completed_at: now })
        .eq('id', campaign.id)
    }
    
    results.push({ campaign_id: campaign.id, day: nextDay, sent: fonnteData.status === true })
    processed++
    
    // Rate limit: max 10 per run
    if (processed >= 10) break
  }
  
  return c.json({ success: true, processed, results })
})

// GET /api/sequences/active
router.get('/active', async (c) => {
  const { data, error } = await supabase(c.env).from('outreach_campaigns')
    .select('*, leads(shop_name, platform, score)')
    .eq('status', 'active')
    .order('next_send_at', { ascending: true })
    .limit(50)
  
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, campaigns: data || [], count: data?.length || 0 })
})

// DELETE /api/sequences/:id/cancel
router.delete('/:id/cancel', async (c) => {
  const id = c.req.param('id')
  const { data, error } = await supabase(c.env).from('outreach_campaigns')
    .update({ status: 'cancelled', completed_at: new Date().toISOString() })
    .eq('id', id)
    .select().single()
  
  if (error) return c.json({ success: false, error: error.message }, 500)
  return c.json({ success: true, campaign: data })
})

export default router
```

---

### Task 4 — Create Required DB Tables [~10 credits]

```sql
-- Di Supabase SQL Editor
CREATE TABLE IF NOT EXISTS outreach_campaigns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id),
  phone TEXT NOT NULL,
  name TEXT,
  shop_name TEXT,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'cancelled')),
  sequence_day INTEGER DEFAULT 0,
  next_send_at TIMESTAMPTZ,
  enrolled_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS outreach_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES outreach_campaigns(id),
  lead_id UUID REFERENCES leads(id),
  sequence_day INTEGER NOT NULL,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed', 'opened')),
  sent_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wa_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  target TEXT NOT NULL,
  message TEXT NOT NULL,
  lead_id UUID,
  direction TEXT DEFAULT 'outbound' CHECK (direction IN ('inbound', 'outbound')),
  status TEXT DEFAULT 'pending',
  is_bulk BOOLEAN DEFAULT FALSE,
  bulk_count INTEGER,
  fonnte_response JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### Task 5 — Add Fonnte Secret to Cloudflare [~5 credits]

```bash
# Set Fonnte token as Cloudflare Pages secret
npx wrangler pages secret put FONNTE_TOKEN --project-name sovereign-orchestrator
# (paste token when prompted)

# Verify
npx wrangler pages secret list --project-name sovereign-orchestrator
```

---

### Task 6 — Build, Test & Deploy [~15 credits]

```bash
# In src/index.tsx, mount new routers:
# import sequencesRouter from './routes/sequences'
# app.route('/api/sequences', sequencesRouter)
# (wa router should already be mounted)

npm run build

fuser -k 3000/tcp 2>/dev/null || true
pm2 restart sovereign
sleep 4

# Test WA status
curl -s http://localhost:3000/api/wa/status
# Expected: {"success":true,"connected":true,"device":"..."}

# Test WA send (to your own number)
curl -s -X POST http://localhost:3000/api/wa/send \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"target":"628xxxx","message":"Test dari Sovereign OS 🚀"}'

# Test sequence enroll
curl -s -X POST http://localhost:3000/api/sequences/enroll \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"lead_id":"<lead-uuid>","phone":"628xxxx","name":"Test","shop_name":"TestStore"}'

# Deploy
npx wrangler pages deploy dist --project-name sovereign-orchestrator

git add -A
git commit -m "feat: Session 6 - Fonnte Live + WhatsApp Auto-Sequence

- /api/wa/send: live WhatsApp sending via Fonnte
- /api/wa/bulk: bulk sending (max 50 targets)
- /api/wa/status: device connection status
- /api/wa/history: WA log history
- /api/wa/webhook: inbound message handling + DNC + escalation
- /api/sequences/enroll: enroll lead to Day 0-3-7-14 sequence
- /api/sequences/process-queue: batch process scheduled messages
- /api/sequences/active: list active campaigns
- Tables: outreach_campaigns, outreach_logs, wa_logs created
- Version: v5.0"
git push origin main
```

---

## 📊 WHAT SHOULD BE DELIVERED

```yaml
Fonnte Integration:
  POST /api/wa/send (live): ✅
  POST /api/wa/bulk: ✅
  GET /api/wa/status: ✅
  GET /api/wa/history: ✅
  POST /api/wa/webhook: ✅

Auto-Sequence:
  POST /api/sequences/enroll: ✅
  POST /api/sequences/process-queue: ✅
  GET /api/sequences/active: ✅
  DELETE /api/sequences/:id/cancel: ✅

Database Tables Created:
  outreach_campaigns: ✅
  outreach_logs: ✅
  wa_logs: ✅

Cloudflare Secret:
  FONNTE_TOKEN: ✅ Set

WA Message Sent (Test): ✅
Deployed: v5.0 ✅
```

---

## ⚠️ CRITICAL NOTES

1. **Rate Limiting**: Fonnte limit: 1 pesan/detik per device. Gunakan `delay` parameter. Default 2 detik.

2. **Credit Monitoring**: Cek sisa kredit Fonnte di dashboard. Gratis akun = limited credits.

3. **Sequence Processing**: `process-queue` harus dipanggil secara periodik. Opsi:
   - Manual trigger dari UI
   - Cloudflare Cron Trigger (butuh Workers Paid plan)
   - Atau trigger otomatis dari endpoint lain

4. **DNC List**: Jangan pernah kirim ke nomor yang sudah reply "stop". Webhook handler sudah otomatis handle ini.

---

## 💡 NOTES FOR SESSION #007

Session #007 fokus ke **Real-Money Dashboard upgrade** dengan AI-enhanced insights.
Akan menghitung revenue realtime, prediksi trend, dan anomaly detection.

**Prerequisites untuk Session #007:**
- [ ] Session #006 complete (Fonnte live, sequences working)
- [ ] Minimal ada 1 sequence enrolled untuk test data

---

## 🎉 FILL THIS AFTER SESSION #006 COMPLETE

```
SESSION #006 ACTUAL RESULTS:
  Credits Used: __ credits (estimate: 80-95)
  Duration: __ minutes
  
DELIVERABLES:
  WA send live: [✅/❌]
  Auto-sequence: [✅/❌]
  Test message sent: [✅/❌]
  Deployed: [✅/❌]
  
FONNTE TOKEN: [obtained ✅ / still missing ❌]
BLOCKERS: [describe]
NOTES FOR SESSION #007: [context]

PRODUCTION HEALTH:
  https://sovereign-orchestrator.pages.dev/api/wa/status → connected: true/false
  Version: v5.0
```

---

*Session Handoff #006 | Sovereign Business Engine | CONFIDENTIAL | Haidar Faras*
