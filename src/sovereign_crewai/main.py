#!/usr/bin/env python
"""
Sovereign Business Engine - CrewAI Entry Point
===============================================
Entry point for CrewAI AMP deployment.
Uses run() function as required by CrewAI AMP for Crew-type projects.

Environment Variables Required in CrewAI AMP:
- GROQ_API_KEY: Groq API key for LLM inference (via LiteLLM)
- SERPER_API_KEY: Serper.dev API key for web search (optional)
"""

import os

# Suppress OpenAI fallback warning - we use Groq via LiteLLM
if not os.environ.get('OPENAI_API_KEY'):
    os.environ['OPENAI_API_KEY'] = 'NA'

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


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'total_products': 8,
        'target_platform': 'instagram',
        'min_lead_score': 70,
        'outreach_day': 0
    }
    try:
        SovereignCrew().crew().train(
            n_iterations=int(os.environ.get('TRAIN_ITERATIONS', '3')),
            filename='sovereign_training_data.pkl',
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Training error: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SovereignCrew().crew().replay(
            task_id=os.environ.get('REPLAY_TASK_ID', '')
        )
    except Exception as e:
        raise Exception(f"Replay error: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'total_products': 8,
        'target_platform': 'instagram',
        'min_lead_score': 70,
        'outreach_day': 0
    }
    try:
        SovereignCrew().crew().test(
            n_iterations=int(os.environ.get('TEST_ITERATIONS', '1')),
            openai_model_name='groq/llama-3.3-70b-versatile',
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Test error: {e}")


if __name__ == "__main__":
    run()
