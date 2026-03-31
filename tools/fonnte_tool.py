"""
Fonnte WhatsApp Tools for CrewAI
================================
Send WhatsApp messages and check device status via Fonnte API.
"""

import os
import json
import requests
from crewai.tools import BaseTool
from pydantic import Field


class FonnteSendTool(BaseTool):
    name: str = "fonnte_send"
    description: str = """
    Send a WhatsApp message via Fonnte API.
    Use this to send outreach messages to leads.
    
    Input format: JSON with 'phone' (required, Indonesian format: 628xxx), 
    'message' (required, max 300 chars), 'type' (optional, default 'text').
    
    Example: {"phone": "6281234567890", "message": "Haii kak! Mau liat katalog FashionKas?"}
    
    IMPORTANT: Only send messages between 9 AM - 8 PM WIB.
    NEVER send to numbers marked as 'lost' or who said 'stop'.
    """
    
    token: str = Field(default="")
    
    def __init__(self, token: str = None, **kwargs):
        super().__init__(**kwargs)
        self.token = token or os.getenv('FONNTE_TOKEN', '')
    
    def _run(self, query: str) -> str:
        if not self.token or self.token == '<to-be-configured>':
            return json.dumps({
                "error": "Fonnte token not configured",
                "action": "Set FONNTE_TOKEN environment variable"
            })
        
        try:
            params = json.loads(query) if isinstance(query, str) else query
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON input"})
        
        phone = params.get('phone', '')
        message = params.get('message', '')
        msg_type = params.get('type', 'text')
        
        if not phone or not message:
            return json.dumps({"error": "Both 'phone' and 'message' are required"})
        
        if len(message) > 300:
            return json.dumps({
                "error": "Message too long",
                "length": len(message),
                "max": 300
            })
        
        url = "https://api.fonnte.com/send"
        headers = {
            "Authorization": self.token
        }
        data = {
            "target": phone,
            "message": message,
            "type": msg_type
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=15)
            result = response.json()
            return json.dumps({
                "success": result.get('status', False),
                "phone": phone,
                "message_preview": message[:50] + "...",
                "fonnte_response": result
            }, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})


class FonnteStatusTool(BaseTool):
    name: str = "fonnte_status"
    description: str = """
    Check Fonnte WhatsApp device connection status.
    Use this to verify the WhatsApp bridge is online before sending messages.
    
    No input required - just call this tool to check status.
    """
    
    token: str = Field(default="")
    
    def __init__(self, token: str = None, **kwargs):
        super().__init__(**kwargs)
        self.token = token or os.getenv('FONNTE_TOKEN', '')
    
    def _run(self, query: str = "") -> str:
        if not self.token or self.token == '<to-be-configured>':
            return json.dumps({
                "status": "not_configured",
                "message": "Fonnte token not set. WhatsApp bridge is offline.",
                "action": "Set FONNTE_TOKEN environment variable"
            })
        
        url = "https://api.fonnte.com/device"
        headers = {
            "Authorization": self.token
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            result = response.json()
            return json.dumps({
                "status": "connected" if result.get('status') else "disconnected",
                "device_info": result
            }, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })
