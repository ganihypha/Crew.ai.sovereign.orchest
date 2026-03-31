# SYSTEM/SCALE VALIDATION - Standard Operating Procedure
# Layer 2: @resellerkas.official
# Sovereign Business Engine v3.0

## Purpose
Validate that the Sovereign Engine's automation systems work 
reliably and can scale from 10 to 100 to 1000 leads/customers.

## Validation Criteria

### FULLY OPERATIONAL (Score 80-100)
- All API endpoints responding (< 3s latency)
- WhatsApp (Fonnte) device online and sending
- Lead scoring algorithm accuracy >= 80%
- Conversion rate >= 15%
- Contact rate >= 40%
- Zero critical errors in 24h
- Outreach sequences completing Day 0-14 without drops

### SYSTEM WORKING (Score 50-79)
- Core APIs responding
- WhatsApp connected
- Conversion rate >= 5%
- Contact rate >= 20%
- Minor errors acceptable (< 5% failure rate)

### PARTIALLY OPERATIONAL (Score 20-49)
- Some APIs failing
- WhatsApp intermittent
- Conversion rate < 5%
- Multiple automation bottlenecks

### SYSTEM DOWN (Score 0-19)
- Critical APIs unreachable
- WhatsApp disconnected
- No lead processing
- Major automation failures

## System Health Checks

### 1. Database Health
```
Check: Can we query all 8 Supabase tables?
Tables: products, customers, orders, leads, 
        outreach_campaigns, outreach_logs,
        validation_events, validation_metrics
Pass: All return data within 2 seconds
```

### 2. API Endpoint Health  
```
Check: GET /api/health returns status: "ok"
Check: GET /api/products returns data
Check: GET /api/validation/stats returns data
Pass: All respond HTTP 200 within 3 seconds
```

### 3. WhatsApp (Fonnte) Health
```
Check: GET /api/wa/status returns device: "connected"
Pass: Device online, queue empty, no errors
```

### 4. Conversion Funnel
```
Stage 1: Lead Discovered -> new (lead enters system)
Stage 2: Lead Scored -> scored (algorithm assigns score)
Stage 3: Lead Contacted -> contacted (outreach message sent)
Stage 4: Lead Converted -> converted (became customer)
Stage 5: Lead Lost -> lost (did not convert after Day 14)

Healthy funnel: Each stage retains >= 30% of previous
```

## Lead Scoring Algorithm

```
lead_score = (
  followers_score +        # 0-20 (sweet spot: 1K-50K)
  engagement_score +       # 0-20 (posts frequency, quality)
  digital_gap_score +      # 0-30 (HIGH=30, MEDIUM=15, LOW=5)
  platform_score +         # 0-15 (instagram=15, tiktok=10, other=5)
  responsiveness_score     # 0-15 (replied within 24h=15, 48h=10, none=0)
)
```

### Score Thresholds
- Hot Lead: Score >= 70 (priority outreach)
- Warm Lead: Score 40-69 (queue for later)
- Cold Lead: Score < 40 (archive)

## Outreach Sequence (Day 0-3-7-14)

### Day 0: Introduction
- Trigger: Lead scored >= 70
- Template: Casual intro, mention their shop name
- Goal: Get a response

### Day 3: Value Proposition
- Trigger: No reply to Day 0
- Template: Share FashionKas catalog, wholesale pricing
- Goal: Spark interest

### Day 7: Social Proof
- Trigger: No reply to Day 3  
- Template: Share reseller success stories, earnings screenshots
- Goal: Build FOMO

### Day 14: Final Touch
- Trigger: No reply to Day 7
- Template: "Pintu masih terbuka, hubungi kapan aja ya!"
- Goal: Soft close, leave positive impression

## Current Baseline Data (2026-03-31)
- Total Leads: 10
- Hot Leads (70+): 6
- Contacted: 2 (20% contact rate)
- Converted: 1 (10% conversion rate)
- Highest Score: 95 (Wardrobe ID)
- Outreach Logs: 0 (Fonnte not yet integrated)
- Campaigns: 0 (pending setup)

## Scaling Targets
- Month 1: 50 leads, 15% conversion
- Month 3: 200 leads, 20% conversion  
- Month 6: 1000 leads, 25% conversion
