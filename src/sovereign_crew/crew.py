"""
Sovereign Business Engine - CrewAI Orchestrator
================================================
The AI Brain behind the 3-Layer Market Validation System.

This is the main entry point for the CrewAI crew that powers
the Sovereign Business Engine's autonomous validation system.

Architecture:
- CrewAI Studio: Design & Test agents visually
- CrewAI AMP: Deploy & run agents 24/7
- Sovereign Web: Monitor results via dashboard

Integration Flow:
  Sovereign Web -> API Request -> CrewAI AMP -> Execute Crew -> Return Results -> Sovereign Web
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.supabase_tool import SupabaseQueryTool
from tools.fonnte_tool import FonnteSendTool, FonnteStatusTool
from tools.sovereign_api_tool import SovereignAPITool


@CrewBase
class SovereignValidationCrew:
    """
    Sovereign Validation Crew - 3-Layer Market Validation System
    
    This crew orchestrates 8 specialized AI agents across 3 validation layers:
    - Layer 1 (Demand): demand_analyst, revenue_tracker
    - Layer 2 (System): lead_scout, system_validator, closer_agent
    - Layer 3 (Trust): trust_auditor, content_strategist
    - Meta: sovereign_orchestrator (coordinates all layers)
    """
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    # =============================================
    # TOOLS INITIALIZATION
    # =============================================
    
    def __init__(self):
        """Initialize tools with environment variables."""
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.supabase_tool = SupabaseQueryTool(
            supabase_url=os.getenv('SUPABASE_URL'),
            supabase_key=os.getenv('SUPABASE_SERVICE_KEY')
        )
        self.fonnte_send_tool = FonnteSendTool(
            token=os.getenv('FONNTE_TOKEN')
        )
        self.fonnte_status_tool = FonnteStatusTool(
            token=os.getenv('FONNTE_TOKEN')
        )
        self.sovereign_api_tool = SovereignAPITool(
            base_url=os.getenv('SOVEREIGN_WEB_URL', 'https://sovereign-orchestrator.pages.dev')
        )
    
    # =============================================
    # LAYER 1: DEMAND VALIDATION AGENTS
    # =============================================
    
    @agent
    def demand_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['demand_analyst'],
            tools=[self.supabase_tool, self.search_tool],
            verbose=True
        )
    
    @agent
    def revenue_tracker(self) -> Agent:
        return Agent(
            config=self.agents_config['revenue_tracker'],
            tools=[self.supabase_tool],
            verbose=True
        )
    
    # =============================================
    # LAYER 2: SYSTEM/SCALE VALIDATION AGENTS
    # =============================================
    
    @agent
    def lead_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_scout'],
            tools=[self.scrape_tool, self.search_tool, self.supabase_tool],
            verbose=True,
            allow_delegation=True
        )
    
    @agent
    def system_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['system_validator'],
            tools=[self.supabase_tool, self.fonnte_status_tool, self.sovereign_api_tool],
            verbose=True
        )
    
    @agent
    def closer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['closer_agent'],
            tools=[self.fonnte_send_tool, self.supabase_tool],
            verbose=True
        )
    
    # =============================================
    # LAYER 3: TRUST/AUTHORITY VALIDATION AGENTS
    # =============================================
    
    @agent
    def trust_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['trust_auditor'],
            tools=[self.search_tool, self.scrape_tool, self.supabase_tool],
            verbose=True
        )
    
    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],
            tools=[self.search_tool],
            verbose=True
        )
    
    # =============================================
    # META AGENT
    # =============================================
    
    @agent
    def sovereign_orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['sovereign_orchestrator'],
            tools=[self.supabase_tool, self.sovereign_api_tool],
            verbose=True,
            allow_delegation=True
        )
    
    # =============================================
    # TASKS
    # =============================================
    
    @task
    def analyze_demand(self) -> Task:
        return Task(config=self.tasks_config['analyze_demand'])
    
    @task
    def track_revenue(self) -> Task:
        return Task(config=self.tasks_config['track_revenue'])
    
    @task
    def scout_leads(self) -> Task:
        return Task(config=self.tasks_config['scout_leads'])
    
    @task
    def validate_system(self) -> Task:
        return Task(config=self.tasks_config['validate_system'])
    
    @task
    def compose_outreach(self) -> Task:
        return Task(config=self.tasks_config['compose_outreach'])
    
    @task
    def audit_trust(self) -> Task:
        return Task(config=self.tasks_config['audit_trust'])
    
    @task
    def plan_content(self) -> Task:
        return Task(config=self.tasks_config['plan_content'])
    
    @task
    def generate_validation_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_validation_report'],
            context=[
                self.analyze_demand(),
                self.track_revenue(),
                self.scout_leads(),
                self.validate_system(),
                self.audit_trust()
            ]
        )
    
    # =============================================
    # CREW DEFINITION
    # =============================================
    
    @crew
    def crew(self) -> Crew:
        """
        Creates the Sovereign Validation Crew.
        
        Process: Hierarchical
        - sovereign_orchestrator manages all other agents
        - Tasks flow through 3 layers before final report
        
        Execution Order:
        1. Layer 1 tasks (demand + revenue) run in parallel
        2. Layer 2 tasks (scout + system + outreach) run in parallel
        3. Layer 3 tasks (trust + content) run in parallel
        4. Meta task (validation report) runs last, using all outputs
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.sovereign_orchestrator(),
            verbose=True,
            memory=True,
            planning=True
        )
