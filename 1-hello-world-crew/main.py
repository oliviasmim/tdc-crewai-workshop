import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.disable_telemetry import disable_telemetry
disable_telemetry()

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_MODEL_NAME'] = "gpt-3.5-turbo"


# Define the agent
greeter_agent = Agent(
    role="Greeter",
    goal="Greet the user with a welcome message.",
    backstory="A friendly bot designed to introduce users to the workshop.",
    allow_delegation=False,
    verbose=True,
)

# Define the task
greet_task = Task(
    description="Say 'Hello and welcome to the PR Review Crew Workshop!'",
    agent=greeter_agent,
    expected_output="A friendly welcome message for the workshop participants"
)

# Create the crew
crew = Crew(
    agents=[greeter_agent],
    tasks=[greet_task],
    verbose=True,
)

# Run the crew (no input needed for this static task)
result = crew.kickoff()

print(result) #output the result.