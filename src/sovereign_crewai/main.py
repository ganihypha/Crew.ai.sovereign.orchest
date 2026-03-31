#!/usr/bin/env python
"""
Sovereign Business Engine - CrewAI Entry Point
===============================================
Entry point for CrewAI AMP deployment.
Uses run() function as required by CrewAI AMP for Crew-type projects.
"""

from sovereign_crewai.crew import SovereignCrew


def run():
    """
    Run the Sovereign Validation Crew.
    This is the entry point called by CrewAI AMP.
    """
    inputs = {
        'total_products': 8,
        'target_platform': 'instagram',
        'min_lead_score': 70,
        'outreach_day': 0
    }
    result = SovereignCrew().crew().kickoff(inputs=inputs)
    return result


if __name__ == "__main__":
    run()
