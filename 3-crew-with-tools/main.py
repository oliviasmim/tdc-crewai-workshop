import os
import sys
from pathlib import Path
import datetime

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


from utils.disable_telemetry import disable_telemetry
disable_telemetry()


# Import required libraries
from dotenv import load_dotenv
from crewai import Crew
from agents import TechContentCreator
from tasks import TechContentResearchTasks

# Load environment variables
load_dotenv()

def main(tech_theme):
    """Run the tech content research crew for a specified theme."""
    print(f"Starting research on: {tech_theme}")
    
    # Initialize agent creator
    agent_creator = TechContentCreator()
    
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
    analysis_task = task_creator.technical_analysis_task(technical_expert, tech_theme)
    structure_task = task_creator.content_structure_task(content_specialist)
    validation_task = task_creator.source_validation_task(source_validator)
    review_task = task_creator.final_review_task(editor, tech_theme)
    
    # Create crew
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
    
    # Run the crew
    result = crew.kickoff(inputs={"theme": tech_theme})
    
    # Generate output file name with timestamp and theme
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_theme = tech_theme.replace(" ", "_").lower()
    output_file = f"{sanitized_theme}_research_{timestamp}.md"
    
    # Write results to Markdown file
    with open(output_file, 'w') as f:
        f.write(f"# Tech Content Research: {tech_theme}\n\n")
        f.write(f"**Date:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("## Executive Summary\n\n")
        f.write("This report contains comprehensive research on the latest trends, technical analysis, and a structured outline for creating content about this technology theme.\n\n")
        f.write("## Research Results\n\n")
        f.write(result.raw)
    
    print(f"Research complete! Report saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    # Get theme from command line argument or use default
    if len(sys.argv) > 1:
        theme = ' '.join(sys.argv[1:])
    else:
        theme = "Artificial Intelligence in Healthcare"
    
    output_file = main(theme)
    print(f"You can view your research in: {output_file}")