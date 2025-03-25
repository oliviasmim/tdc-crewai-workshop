import os
import sys
from pathlib import Path
import datetime
import time

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Disable telemetry
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from dotenv import load_dotenv
from crewai import Crew
from crewai.agent import Agent
from crewai.task import Task

# Import agent and task creators
sys.path.append(str(project_root / "3-crew-with-tools"))
from agents import TechContentCreator
from tasks import TechContentResearchTasks

# Load environment variables
load_dotenv()

def run_research(tech_theme, model="GPT-4 Turbo", research_focus=None, 
                target_audience="Mixed", depth=3, progress_callback=None):
    """
    Run the tech content research with progress updates for Streamlit
    
    Args:
        tech_theme: The technology theme to research
        model: The language model to use
        research_focus: Specific areas to focus on
        target_audience: Target audience for the content
        depth: Research depth level (1-5)
        progress_callback: Function to call with progress updates
    
    Returns:
        tuple: (results, output_file_path)
    """
    # Initialize agent creator with model choice
    agent_creator = TechContentCreator()
    if model == "GPT-3.5 Turbo":
        agent_creator.llm.model_name = "gpt-3.5-turbo"
    else:
        agent_creator.llm.model_name = "gpt-4-turbo"
    
    # Initialize agents
    trend_researcher = agent_creator.trend_researcher_agent()
    technical_expert = agent_creator.technical_expert_agent()
    content_specialist = agent_creator.content_structure_specialist_agent()
    source_validator = agent_creator.source_validator_agent()
    editor = agent_creator.editor_in_chief_agent()
    
    # Initialize task creator
    task_creator = TechContentResearchTasks()
    
    # Create tasks
    research_task = task_creator.trend_research_task(trend_researcher, tech_theme)
    
    # Update progress for task 1
    if progress_callback:
        progress_callback(0, f"Researching trends in {tech_theme}...")
    
    # Second task with dependency on first
    analysis_task = task_creator.technical_analysis_task(technical_expert, tech_theme)
    
    # Progress update
    if progress_callback:
        progress_callback(1, f"Analyzing technical details of {tech_theme} trends...")
    
    # Structure task depends on research and analysis
    structure_task = task_creator.content_structure_task(content_specialist)
    
    # Progress update
    if progress_callback:
        progress_callback(2, f"Creating content structure for {tech_theme} article...")
    
    # Source validation task
    validation_task = task_creator.source_validation_task(source_validator)
    
    # Progress update
    if progress_callback:
        progress_callback(3, f"Validating sources for {tech_theme} research...")
    
    # Final review task
    review_task = task_creator.final_review_task(editor, tech_theme)
    
    # Progress update
    if progress_callback:
        progress_callback(4, f"Finalizing comprehensive report on {tech_theme}...")
    
    # Create crew with explicit task dependencies
    crew = Crew(
        agents=[
            trend_researcher,
            technical_expert, 
            content_specialist,
            source_validator,
            editor
        ],
        tasks=[
            research_task,
            analysis_task,
            structure_task, 
            validation_task,
            review_task
        ],
        verbose=True,
    )
    
    # Run the crew with input context
    context = {
        "theme": tech_theme,
        "focus": research_focus,
        "audience": target_audience,
        "depth": depth
    }
    
    result = crew.kickoff(inputs=context)
    
    # Generate output file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_theme = tech_theme.replace(" ", "_").lower()
    output_file = Path(__file__).parent / "cache" / f"{sanitized_theme}_research_{timestamp}.md"
    
    # Create cache directory if it doesn't exist
    output_file.parent.mkdir(exist_ok=True)
    
    # Write results to Markdown file
    with open(output_file, 'w') as f:
        f.write(f"# Tech Content Research: {tech_theme}\n\n")
        f.write(f"**Date:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("## Executive Summary\n\n")
        f.write("This report contains comprehensive research on the latest trends, technical analysis, and a structured outline for creating content about this technology theme.\n\n")
        f.write("## Research Results\n\n")
        f.write(result.raw)
    
    return result, str(output_file)