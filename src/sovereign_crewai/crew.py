"""
Sovereign Business Engine - CrewAI Crew Definition
====================================================
8 specialized agents across 3 validation layers.
Uses Groq (Llama) as LLM provider for fast, free inference.
"""

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class SovereignCrew():
    """
    Sovereign Validation Crew - 3-Layer Market Validation System

    8 agents across 3 layers:
    - Layer 1 (Demand): demand_analyst, revenue_tracker
    - Layer 2 (System): lead_scout, system_validator, closer_agent
    - Layer 3 (Trust): trust_auditor, content_strategist
    - Meta: sovereign_orchestrator
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # =============================================
    # LAYER 1: DEMAND VALIDATION AGENTS
    # =============================================

    @agent
    def demand_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['demand_analyst'],  # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def revenue_tracker(self) -> Agent:
        return Agent(
            config=self.agents_config['revenue_tracker'],  # type: ignore[index]
            verbose=True
        )

    # =============================================
    # LAYER 2: SYSTEM/SCALE VALIDATION AGENTS
    # =============================================

    @agent
    def lead_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_scout'],  # type: ignore[index]
            tools=[ScrapeWebsiteTool(), SerperDevTool()],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def system_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['system_validator'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def closer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['closer_agent'],  # type: ignore[index]
            verbose=True
        )

    # =============================================
    # LAYER 3: TRUST/AUTHORITY VALIDATION AGENTS
    # =============================================

    @agent
    def trust_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['trust_auditor'],  # type: ignore[index]
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],  # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True
        )

    # =============================================
    # META AGENT
    # =============================================

    @agent
    def sovereign_orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['sovereign_orchestrator'],  # type: ignore[index]
            verbose=True,
            allow_delegation=True
        )

    # =============================================
    # TASKS
    # =============================================

    @task
    def analyze_demand(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_demand']  # type: ignore[index]
        )

    @task
    def track_revenue(self) -> Task:
        return Task(
            config=self.tasks_config['track_revenue']  # type: ignore[index]
        )

    @task
    def scout_leads(self) -> Task:
        return Task(
            config=self.tasks_config['scout_leads']  # type: ignore[index]
        )

    @task
    def validate_system(self) -> Task:
        return Task(
            config=self.tasks_config['validate_system']  # type: ignore[index]
        )

    @task
    def compose_outreach(self) -> Task:
        return Task(
            config=self.tasks_config['compose_outreach']  # type: ignore[index]
        )

    @task
    def audit_trust(self) -> Task:
        return Task(
            config=self.tasks_config['audit_trust']  # type: ignore[index]
        )

    @task
    def plan_content(self) -> Task:
        return Task(
            config=self.tasks_config['plan_content']  # type: ignore[index]
        )

    @task
    def generate_validation_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_validation_report'],  # type: ignore[index]
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
        """Creates the Sovereign Validation Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
