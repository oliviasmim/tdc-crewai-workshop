import os
from crewai import Agent, Task, Crew, Process

# No need for an LLM if we're just doing a static output
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Define the agent
greeter_agent = Agent(
    role="Greeter",
    name="WelcomeBot",
    goal="Greet the user with a welcome message.",
    backstory="A friendly bot designed to introduce users to the workshop.",
    allow_delegation=False,
)

# Define the task
greet_task = Task(
    description="Say 'Hello and welcome to the PR Review Crew Workshop!'",
    agent=greeter_agent,
)

# Create the crew
crew = Crew(
    agents=[greeter_agent],
    tasks=[greet_task],
    verbose=2, # You can set it to 1 or 2 to see more details
    process=Process.sequential,
)

# Run the crew (no input needed for this static task)
result = crew.kickoff()

print(result) #output the result.