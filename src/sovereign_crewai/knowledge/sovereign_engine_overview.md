# SOVEREIGN BUSINESS ENGINE - Knowledge Base
# Classification: CONFIDENTIAL | Founder Access Only
# Version: 3.0 | Last Updated: 2026-03-31

## Engine Identity

The Sovereign Business Engine is NOT a fashion app. It is a **Private Business 
Orchestration System** that uses FashionKas as a real-world market laboratory.

What we sell: The ENGINE (orchestration, automation, validation systems)
What we DON'T sell: The WHEELS (individual fashion products)

The engine validates business models through 3 Instagram brands running 
simultaneously as a controlled experiment.

## 3-Layer Market Validation System

### Layer 1: DEMAND VALIDATION (@fashionkas.official)
- **Purpose**: Prove product-market fit with real transaction data
- **Brand**: FashionKas - Premium street fashion
- **Data Source**: Supabase `products`, `orders`, `customers` tables
- **Key Metrics**:
  - Active Products: 8 SKUs
  - Total Orders: 8+ (4 completed)
  - Total Revenue: Rp 2,296,000+
  - Average Order Value: Rp 574,000
  - Customer Count: 6+ (1 VIP, 1 Gold, 2 Silver, 2 Bronze)
  - Repeat Purchase Rate: target > 20%

### Layer 2: SYSTEM/SCALE VALIDATION (@resellerkas.official)  
- **Purpose**: Prove the automation system scales effectively
- **Brand**: ResellerKas - Reseller community & education
- **Data Source**: Supabase `leads`, `outreach_logs`, `outreach_campaigns` tables
- **Key Metrics**:
  - Total Leads: 10+ (6 hot, scores 70+)
  - Contact Rate: 20%
  - Conversion Rate: 10%
  - Top Lead Score: 95 (Wardrobe ID - converted)
  - Digital Gap: 4 High, 4 Medium, 2 Low
  - Outreach Sequences: Day 0/3/7/14

### Layer 3: TRUST/AUTHORITY VALIDATION (@haidar_faras_m)
- **Purpose**: Prove founder credibility and brand authority
- **Brand**: Haidar Faras M - Personal brand, "Build in Public"
- **Data Source**: Supabase `validation_events`, `validation_metrics` tables
- **Key Metrics**:
  - Trust Score: 60
  - Hot Leads (trust indicators): 6
  - Validation Events: 11 logged
  - Validation Metrics: 15 tracked
  - Content Consistency: daily posting target

## Current Validation Status

| Metric | Value | Status |
|--------|-------|--------|
| Overall Validation Score | 100 | MARKET VALIDATED |
| Demand Verdict | GROWING DEMAND | Active |
| System Verdict | SYSTEM WORKING | Active |
| Trust Verdict | BUILDING TRUST | Active |
| Data Points Analyzed | 24+ | Growing |

## Business Model

FashionKas products (fashion items) are the "fuel" for validation.
Each sale, each lead, each social proof data point feeds into the 
validation engine to prove the system works.

Exit strategy: License the Sovereign Engine to other businesses 
who want the same orchestration + validation capability.

## Target Customer Profile

**For FashionKas products**:
- Indonesian millennials/Gen-Z
- Premium street fashion buyers
- Price range: Rp 79,000 - Rp 289,000
- Cities: Bandung, Jakarta, Surabaya, Semarang, Yogyakarta, Malang

**For Reseller Network**:
- Small Instagram fashion sellers
- 1K-50K followers
- Selling offline, lacking online presence ("digital gap")
- Looking for supplier/wholesale partnership

## Technology Stack

- **Frontend**: Cloudflare Pages (sovereign-orchestrator.pages.dev)
- **Backend**: Hono.js on Cloudflare Workers
- **Database**: Supabase PostgreSQL with RLS
- **AI Brain**: CrewAI (this system) + LangGraph.js (edge)
- **WhatsApp**: Fonnte API
- **Scraping**: ScraperAPI
- **Search**: SerpAPI
- **Auth**: 4-digit PIN + JWT (Web Crypto API)

## Supabase Database Schema

### Products Table
- id (UUID), name, sku (unique), category, price, cost_price
- stock, min_stock, description, image_url, is_active
- Top SKUs: FK-KOS-BLK-001, FK-HDI-NVY-003, FK-JGR-BLK-004

### Customers Table  
- id, name, phone, address, city, tier (bronze/silver/gold/vip)
- total_orders, total_spent, notes
- VIP: Sari Wulandari (Rp 5,670,000 lifetime, 25 orders)
- Gold: Rina Aulia (Rp 2,850,000 lifetime, 12 orders)

### Orders Table
- id, customer_name, customer_phone, items (JSONB)
- total_amount, status (pending/processing/completed/cancelled)
- notes, source

### Leads Table
- id, shop_name, platform, username, phone, followers
- score (0-100), digital_gap (high/medium/low)
- status (new/scored/contacted/converted/lost)
- Hottest Lead: Wardrobe ID (score 95, converted)

### Validation Tables
- validation_events: layer, event_type, title, description, impact
- validation_metrics: layer, metric_name, metric_value, unit

## API Endpoints (Sovereign Web)

Base URL: https://sovereign-orchestrator.pages.dev

- GET /api/health - System health
- GET /api/dashboard/stats - Dashboard metrics
- GET /api/products - Product catalog
- GET /api/orders - Order list
- GET /api/customers - Customer list
- GET /api/scout/leads - Lead list
- GET /api/validation/stats - Validation statistics
- GET /api/validation/report - Full validation report
- POST /api/validation/events - Log validation event
- POST /api/validation/metrics - Record validation metric

## Important Rules for AI Agents

1. Always use Bahasa Indonesia for customer-facing messages
2. Never expose API keys or sensitive data in outputs
3. All financial figures are in IDR (Indonesian Rupiah)
4. Lead scoring uses 0-100 scale
5. Digital Gap levels: High (no online presence), Medium (basic), Low (established)
6. Customer tiers: Bronze (<Rp 500K), Silver (Rp 500K-2M), Gold (Rp 2M-5M), VIP (>Rp 5M)
7. Validation verdicts must be evidence-based, not assumed
8. The Founder is the only user - this is a private system
