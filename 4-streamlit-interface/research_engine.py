import os
import sys
from pathlib import Path
import datetime

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Disable telemetry
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from dotenv import load_dotenv
from crewai import Crew, Process

# Import agent and task creators
from agents import TechContentCreator
from tasks import TechContentResearchTasks

# Load environment variables
load_dotenv()

def run_research(tech_theme, research_focus=None, 
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
    agent_creator = TechContentCreator()
    
    # Initialize agents
    trend_researcher = agent_creator.trend_researcher_agent()
    technical_expert = agent_creator.technical_expert_agent()
    content_specialist = agent_creator.content_structure_specialist_agent()
    source_validator = agent_creator.source_validator_agent()
    editor = agent_creator.editor_in_chief_agent()
    
    # Initialize task creator
    task_creator = TechContentResearchTasks()
    
    # Create first task - trend research
    research_task = task_creator.trend_research_task(trend_researcher, tech_theme)
    
    # Update progress for task 1
    if progress_callback:
        progress_callback(0, f"Researching trends in {tech_theme}...")
    
    # Second task WITH explicit dependency on first task
    analysis_task = task_creator.technical_analysis_task(
        technical_expert, 
        tech_theme,
        context=[research_task]  # Depends on research task
    )
    
    # Progress update
    if progress_callback:
        progress_callback(1, f"Analyzing technical details of {tech_theme} trends...")
    
    # Structure task depends on research and analysis
    structure_task = task_creator.content_structure_task(
        content_specialist,
        context=[research_task, analysis_task]  # Depends on both previous tasks
    )
    
    # Progress update
    if progress_callback:
        progress_callback(2, f"Creating content structure for {tech_theme} article...")
    
    # Source validation task
    validation_task = task_creator.source_validation_task(
        source_validator,
        context=[research_task, analysis_task]  # Validate sources from research and analysis
    )
    
    # Progress update
    if progress_callback:
        progress_callback(3, f"Validating sources for {tech_theme} research...")
    
    # Final review task
    review_task = task_creator.final_review_task(
        editor, 
        tech_theme,
        context=[research_task, analysis_task, structure_task, validation_task]  # Depends on ALL previous tasks
    )
    
    # Progress update
    if progress_callback:
        progress_callback(4, f"Finalizing comprehensive report on {tech_theme}...")
    
    # Create crew with task workflow (order matters)
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
        process=Process.sequential # Run tasks in sequence
    )
    
    # Run the crew with input context
    context = {
        "theme": tech_theme,
        "focus": research_focus, # TODO: Decoratative, not implemented in tasks
        "audience": target_audience, # TODO: Decoratative, not implemented in tasks
        "depth": depth # TODO: Decoratative, not implemented in tasks
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