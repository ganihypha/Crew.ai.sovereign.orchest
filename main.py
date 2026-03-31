"""
Sovereign Business Engine - Main Entry Point
=============================================
Run this file to execute the full 3-Layer Validation Crew.

Usage:
  python main.py                          # Full validation run
  python main.py --layer demand           # Only Layer 1
  python main.py --layer system           # Only Layer 2
  python main.py --layer trust            # Only Layer 3
  python main.py --task scout_leads       # Single task
  
Environment Variables Required:
  SUPABASE_URL          - Supabase project URL
  SUPABASE_SERVICE_KEY  - Supabase service role JWT
  SERPER_API_KEY        - Serper.dev search API key
  FONNTE_TOKEN          - Fonnte WhatsApp API token
  OPENAI_API_KEY        - OpenAI API key for LLM
  SOVEREIGN_WEB_URL     - Sovereign web dashboard URL
"""

import sys
import json
import argparse
from datetime import datetime
from src.sovereign_crew.crew import SovereignValidationCrew


def run_full_validation():
    """Execute the full 3-Layer Validation Crew."""
    print("=" * 60)
    print("  SOVEREIGN BUSINESS ENGINE v3.0")
    print("  3-Layer Market Validation System")
    print(f"  Execution Time: {datetime.now().isoformat()}")
    print("=" * 60)
    
    inputs = {
        'total_products': 8,
        'target_platform': 'instagram',
        'min_lead_score': 70,
        'outreach_day': 0
    }
    
    crew = SovereignValidationCrew()
    result = crew.crew().kickoff(inputs=inputs)
    
    print("\n" + "=" * 60)
    print("  VALIDATION REPORT GENERATED")
    print("=" * 60)
    print(result)
    
    return result


def run_single_layer(layer_name):
    """Execute tasks for a single validation layer."""
    print(f"\n  Running Layer: {layer_name.upper()}")
    print("-" * 40)
    
    crew = SovereignValidationCrew()
    
    layer_tasks = {
        'demand': ['analyze_demand', 'track_revenue'],
        'system': ['scout_leads', 'validate_system', 'compose_outreach'],
        'trust': ['audit_trust', 'plan_content']
    }
    
    if layer_name not in layer_tasks:
        print(f"Unknown layer: {layer_name}. Use: demand, system, trust")
        return None
    
    # For single layer runs, we use sequential process
    from crewai import Crew, Process
    
    tasks = []
    agents = []
    
    task_methods = {
        'analyze_demand': (crew.analyze_demand, crew.demand_analyst),
        'track_revenue': (crew.track_revenue, crew.revenue_tracker),
        'scout_leads': (crew.scout_leads, crew.lead_scout),
        'validate_system': (crew.validate_system, crew.system_validator),
        'compose_outreach': (crew.compose_outreach, crew.closer_agent),
        'audit_trust': (crew.audit_trust, crew.trust_auditor),
        'plan_content': (crew.plan_content, crew.content_strategist),
    }
    
    for task_name in layer_tasks[layer_name]:
        task_fn, agent_fn = task_methods[task_name]
        tasks.append(task_fn())
        agents.append(agent_fn())
    
    single_crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    inputs = {
        'total_products': 8,
        'target_platform': 'instagram',
        'min_lead_score': 70,
        'outreach_day': 0
    }
    
    result = single_crew.kickoff(inputs=inputs)
    print(f"\n  Layer {layer_name.upper()} Complete!")
    print(result)
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Sovereign Business Engine - CrewAI Orchestrator'
    )
    parser.add_argument(
        '--layer', 
        choices=['demand', 'system', 'trust'],
        help='Run a specific validation layer only'
    )
    parser.add_argument(
        '--task',
        help='Run a specific task only'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print configuration without executing'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("  DRY RUN - Configuration Check")
        print("-" * 40)
        crew = SovereignValidationCrew()
        print(f"  Agents: {len(crew.agents_config)} configured")
        print(f"  Tasks: {len(crew.tasks_config)} configured")
        print(f"  Knowledge files: 4")
        print(f"  Tools: Supabase, Fonnte, Scraper, Search")
        return
    
    if args.layer:
        run_single_layer(args.layer)
    else:
        run_full_validation()


if __name__ == "__main__":
    main()
