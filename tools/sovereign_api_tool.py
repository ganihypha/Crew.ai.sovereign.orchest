"""
Sovereign API Tool for CrewAI
=============================
Allows AI agents to interact with the Sovereign Orchestrator Web API.
Used to push results back to the dashboard and check system health.
"""

import os
import json
import requests
from crewai.tools import BaseTool
from pydantic import Field


class SovereignAPITool(BaseTool):
    name: str = "sovereign_api"
    description: str = """
    Interact with the Sovereign Orchestrator Web Dashboard API.
    Use this to push validation results back to the dashboard 
    and check system health.
    
    Supported actions:
    - health: Check system health (GET /api/health)
    - validation_stats: Get current validation stats (GET /api/validation/stats)
    - log_event: Log a validation event (POST /api/validation/events)
    - record_metric: Record a validation metric (POST /api/validation/metrics)
    - dashboard: Get dashboard stats (GET /api/dashboard/stats)
    
    Input format: JSON with 'action' (required) and 'data' (optional for POST actions).
    
    Example: {"action": "health"}
    Example: {"action": "log_event", "data": {"layer": "demand", "event_type": "insight", "title": "Revenue Growing", "description": "15% growth detected"}}
    Example: {"action": "record_metric", "data": {"layer": "demand", "metric_name": "daily_revenue", "metric_value": 574000, "unit": "IDR"}}
    """
    
    base_url: str = Field(default="")
    auth_token: str = Field(default="")
    
    def __init__(self, base_url: str = None, auth_token: str = None, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url or os.getenv(
            'SOVEREIGN_WEB_URL', 
            'https://sovereign-orchestrator.pages.dev'
        )
        self.auth_token = auth_token or os.getenv('SOVEREIGN_AUTH_TOKEN', '')
    
    def _run(self, query: str) -> str:
        try:
            params = json.loads(query) if isinstance(query, str) else query
        except json.JSONDecodeError:
            params = {"action": query.strip()}
        
        action = params.get('action', '')
        data = params.get('data', {})
        
        headers = {
            "Content-Type": "application/json"
        }
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        action_map = {
            "health": ("GET", "/api/health"),
            "validation_stats": ("GET", "/api/validation/stats"),
            "validation_report": ("GET", "/api/validation/report"),
            "dashboard": ("GET", "/api/dashboard/stats"),
            "products": ("GET", "/api/products"),
            "orders": ("GET", "/api/orders"),
            "customers": ("GET", "/api/customers"),
            "leads": ("GET", "/api/scout/leads"),
            "log_event": ("POST", "/api/validation/events"),
            "record_metric": ("POST", "/api/validation/metrics"),
        }
        
        if action not in action_map:
            return json.dumps({
                "error": f"Unknown action: {action}",
                "valid_actions": list(action_map.keys())
            })
        
        method, path = action_map[action]
        url = f"{self.base_url}{path}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                return json.dumps({
                    "success": True,
                    "action": action,
                    "data": response.json()
                }, indent=2, default=str)
            else:
                return json.dumps({
                    "success": False,
                    "status": response.status_code,
                    "message": response.text[:500]
                })
        except Exception as e:
            return json.dumps({"error": str(e)})
