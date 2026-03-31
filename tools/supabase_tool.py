"""
Supabase Query Tool for CrewAI
==============================
Allows AI agents to query the Sovereign Engine's Supabase database.
"""

import os
import json
import requests
from crewai.tools import BaseTool
from pydantic import Field


class SupabaseQueryTool(BaseTool):
    name: str = "supabase_query"
    description: str = """
    Query the Sovereign Business Engine's Supabase database.
    Use this to fetch products, orders, customers, leads, and validation data.
    
    Supported tables: products, customers, orders, leads, 
    outreach_campaigns, outreach_logs, validation_events, validation_metrics
    
    Input format: JSON with 'table' (required), 'select' (optional, default '*'),
    'filters' (optional), 'limit' (optional, default 100), 'order' (optional).
    
    Example: {"table": "products", "select": "name,price,stock", "limit": 10}
    Example: {"table": "orders", "filters": "status=eq.completed", "order": "created_at.desc"}
    Example: {"table": "leads", "filters": "score=gte.70", "select": "shop_name,score,digital_gap"}
    """
    
    supabase_url: str = Field(default="")
    supabase_key: str = Field(default="")
    
    def __init__(self, supabase_url: str = None, supabase_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL', '')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_SERVICE_KEY', '')
    
    def _run(self, query: str) -> str:
        try:
            params = json.loads(query) if isinstance(query, str) else query
        except json.JSONDecodeError:
            # Simple table name as input
            params = {"table": query.strip()}
        
        table = params.get('table', '')
        select = params.get('select', '*')
        filters = params.get('filters', '')
        limit = params.get('limit', 100)
        order = params.get('order', 'created_at.desc')
        
        valid_tables = [
            'products', 'customers', 'orders', 'leads',
            'outreach_campaigns', 'outreach_logs',
            'validation_events', 'validation_metrics'
        ]
        
        if table not in valid_tables:
            return json.dumps({
                "error": f"Invalid table: {table}",
                "valid_tables": valid_tables
            })
        
        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        query_params = {
            "select": select,
            "limit": str(limit),
            "order": order
        }
        
        if filters:
            # Parse filters like "status=eq.completed"
            for f in filters.split(','):
                parts = f.split('=', 1)
                if len(parts) == 2:
                    query_params[parts[0].strip()] = parts[1].strip()
        
        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return json.dumps({
                    "success": True,
                    "table": table,
                    "count": len(data),
                    "data": data
                }, indent=2, default=str)
            else:
                return json.dumps({
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                })
        except Exception as e:
            return json.dumps({"error": str(e)})
