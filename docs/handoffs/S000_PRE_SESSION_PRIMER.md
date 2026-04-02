# 🏛️ SOVEREIGN BUSINESS ENGINE
# PRE-SESSION PRIMER — WAJIB BACA SEBELUM SETIAP SESSION
### Classification: CONFIDENTIAL | Founder Access Only

---

## ⚡ APA ITU PROJECT INI?

**Sovereign Business Engine** adalah private AI-powered business orchestration platform milik **Haidar Faras**.
Platform ini menggunakan 3 Instagram brand sebagai laboratorium validasi market dan bisnis fashion.

**INGAT**: Ini BUKAN app baru. Ini adalah **lanjutan dari project yang sudah LIVE di production**.

---

## 🌐 LIVE PRODUCTION URLS

| Service | URL |
|---------|-----|
| **Production App** | https://sovereign-orchestrator.pages.dev |
| **GitHub Main Repo** | https://github.com/ganihypha/Sovereign.private.real.busines.orchest |
| **GitHub CrewAI Repo** | https://github.com/ganihypha/Crew.ai.sovereign.orchest |
| **CrewAI AMP** | https://crew-ai-sovereign-orchest-ef50eb91-6c9d-4fc-f916c3e6.crewai.com |
| **Supabase** | https://lfohzibcsafqthupcvdg.supabase.co |

---

## ⚙️ SETUP WAJIB TIAP AWAL SESSION

```bash
# STEP 1: Clone repo
git clone "https://<GITHUB_PAT_TOKEN>@github.com/ganihypha/Sovereign.private.real.busines.orchest.git" webapp
cd webapp

# STEP 2: Install dependencies
npm install

# STEP 3: Setup Cloudflare credentials
export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"
export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"
echo 'export CLOUDFLARE_API_TOKEN="<CF_API_TOKEN>"' >> ~/.bashrc
echo 'export CLOUDFLARE_ACCOUNT_ID="618d52f63c689422eacf6638436c3e8b"' >> ~/.bashrc

# STEP 4: Buat .dev.vars (copy dari SESSION HANDOFF aktif)
# JANGAN commit file ini ke git!

# STEP 5: Build & start
npm run build
fuser -k 3000/tcp 2>/dev/null || true
pm2 start ecosystem.config.cjs

# STEP 6: Verify
sleep 3 && curl http://localhost:3000/api/health
```

---

## 🔑 CREDENTIAL KEYS (Gunakan nilai asli dari .dev.vars lokal kamu)

| Key | Service | Status |
|-----|---------|--------|
| SUPABASE_URL | Supabase | ✅ CONFIGURED |
| SUPABASE_ANON_KEY | Supabase | ✅ CONFIGURED |
| SUPABASE_SERVICE_KEY | Supabase | ✅ CONFIGURED |
| JWT_SECRET | Auth | ✅ CONFIGURED |
| MASTER_PIN | Auth (nilai: 1945) | ✅ CONFIGURED |
| SCRAPER_API_KEY | ScraperAPI | ✅ CONFIGURED |
| LANGCHAIN_API_KEY | LangSmith | ✅ CONFIGURED |
| CREWAI_ORG_ID | CrewAI AMP | ✅ CONFIGURED |
| CREWAI_PAT | CrewAI AMP | ✅ CONFIGURED |
| CREWAI_ENTERPRISE_TOKEN | CrewAI AMP | ✅ CONFIGURED |
| CREWAI_AMP_URL | CrewAI AMP | ✅ CONFIGURED |
| CREWAI_AMP_TOKEN | CrewAI AMP | ✅ CONFIGURED |
| SERPAPI_KEY | SerpAPI | ✅ CONFIGURED |
| GROQ_API_KEY | Groq LLM | ✅ CONFIGURED |
| FONNTE_TOKEN | Fonnte WhatsApp | ❌ MISSING — daftar di fonnte.com |
| OPENAI_API_KEY | OpenAI (untuk RAG) | ❌ MISSING — buat di platform.openai.com |

---

## 📊 CURRENT STATE SNAPSHOT (v3.2 LIVE)

| Komponen | Status |
|----------|--------|
| Cloudflare Pages + Hono.js | ✅ LIVE |
| PIN Auth + JWT | ✅ LIVE (PIN: 1945) |
| Supabase 8 Tables | ✅ LIVE |
| LangGraph.js (4 edge agents) | ✅ INTEGRATED |
| CrewAI AMP (8 agents) | ✅ ONLINE |
| Fonnte WhatsApp | ❌ TOKEN MISSING |
| pgvector / RAG Memory | ❌ FASE 2+ |

### Database Current (8 tabel LIVE):
`products` (8 SKU) | `customers` (6) | `orders` (8, Revenue ~Rp 2.296.000) | `leads` (10, 6 HOT) | `outreach_campaigns` (0) | `outreach_logs` (0) | `validation_events` (11) | `validation_metrics` (15)

---

## ♾️ INFINITE GROWTH LOOP METRICS

```yaml
Session Growth Formula:
  Effective Output = Credits × Efficiency × Knowledge_Multiplier
  
Baseline (Session #1):
  Efficiency: 80%
  Knowledge: 1.0
  
Target Growth Per Session:
  Efficiency: +2-3% per session
  Knowledge: +0.15 per session
  
Goal by Session #8:
  Efficiency: 96%
  Knowledge: 2.05
  Effective Output: 100 × 0.96 × 2.05 = 196.8 effective credits!
```

---

## 📋 8-SESSION ROADMAP

| Session | Fokus | Est. Credits |
|---------|-------|--------------|
| **S1** | Foundation DB (4 tabel baru + Fonnte routes) | 80-95 |
| **S2** | pgvector + 5 tabel v4.0 + API routes baru | 85-100 |
| **S3** | LangGraph.js v2 dengan RAG memory | 95-109 |
| **S4** | CrewAI v4.0 (4 agen baru) | 95-109 |
| **S5** | AI Intelligence UI Page | 90-109 |
| **S6** | Fonnte Live + Auto-sequence | 80-95 |
| **S7** | Dashboard Upgrade + Real AI Insights | 75-90 |
| **S8** | Polish + Security + Final Deploy | 80-100 |
| **TOTAL** | | **~700-807 credits** |

---

## ✅ END-OF-SESSION CHECKLIST

Pastikan ini semua dilakukan sebelum tutup session:

```
□ npm run build → exit 0, ZERO errors
□ curl http://localhost:3000/api/health → status: "ok"
□ curl https://sovereign-orchestrator.pages.dev/api/health → versi match
□ git log --oneline -3 → commit terbaru ada
□ git push origin main → berhasil ke GitHub
□ pm2 logs --nostream → tidak ada critical errors
□ Tulis SESSION HANDOFF doc untuk session berikutnya
□ Backup jika ada perubahan besar
```

---

*Sovereign Business Engine | Pre-Session Primer | CONFIDENTIAL | Haidar Faras*
