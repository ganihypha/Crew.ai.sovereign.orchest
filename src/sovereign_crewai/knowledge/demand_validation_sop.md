# DEMAND VALIDATION - Standard Operating Procedure
# Layer 1: @fashionkas.official
# Sovereign Business Engine v3.0

## Purpose
Validate that real customer demand exists for FashionKas products 
through measurable transaction data.

## Validation Criteria

### STRONG DEMAND (Score 80-100)
- Completed orders >= 10
- Repeat customer rate >= 25%
- Average order value >= Rp 400,000
- Monthly revenue growth >= 15%
- Customer count >= 10
- At least 2 VIP/Gold customers

### GROWING DEMAND (Score 50-79)
- Completed orders >= 4
- Repeat customer rate >= 10%
- Average order value >= Rp 200,000
- Revenue is increasing month-over-month
- Customer count >= 5
- At least 1 Gold customer

### WEAK DEMAND (Score 20-49)
- Completed orders >= 1
- Some repeat customers exist
- Revenue exists but stagnant
- Customer count >= 2

### NO DEMAND (Score 0-19)
- No completed orders or minimal activity
- No repeat customers
- No revenue growth signals

## Data Sources (Supabase)

### Query: Total Revenue
```sql
SELECT SUM(total_amount) as total_revenue 
FROM orders 
WHERE status = 'completed'
```

### Query: Order Statistics
```sql
SELECT 
  COUNT(*) as total_orders,
  COUNT(*) FILTER (WHERE status = 'completed') as completed,
  AVG(total_amount) as avg_value
FROM orders
```

### Query: Customer Tiers
```sql
SELECT tier, COUNT(*) as count, SUM(total_spent) as total
FROM customers
GROUP BY tier
```

### Query: Product Performance
```sql
SELECT name, sku, price, stock 
FROM products 
WHERE is_active = true 
ORDER BY price DESC
```

## Scoring Algorithm

```
demand_score = (
  (completed_orders / 10 * 25) +          # Max 25 points
  (repeat_rate / 25 * 20) +               # Max 20 points  
  (avg_order_value / 500000 * 20) +        # Max 20 points
  (customer_count / 10 * 15) +             # Max 15 points
  (revenue_growth_pct / 15 * 10) +         # Max 10 points
  (vip_gold_count / 3 * 10)                # Max 10 points
)
# Cap at 100
```

## Current Baseline Data (2026-03-31)
- Total Revenue: Rp 2,296,000
- Completed Orders: 4
- Average Order Value: Rp 574,000
- Customer Count: 6
- VIP Customers: 1 (Sari Wulandari)
- Gold Customers: 1 (Rina Aulia)
- Current Score: ~72 (GROWING DEMAND)

## Alert Thresholds
- Revenue drops > 20% week-over-week: ALERT
- Zero orders in 3 consecutive days: ALERT
- Stock reaches 0 on any active product: ALERT
- Average order value drops below Rp 150,000: WARNING
