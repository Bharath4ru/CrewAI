from crewai_tools import FileReadTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = LLM(
    model="gemini/gemini-1.5-pro",
    temperature=0.5,
    api_key=GOOGLE_API_KEY
)

# For fixed directory searches
tool = FileReadTool()

# Create an agent with the knowledge store
agent = Agent(
    role="File Read Agent",
    goal="You will read the file for the answer to the question.  Use the tools to read the file.",
    backstory="""You are a master at reading files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="What's in this file: {question}",
    expected_output="An answer to the question.",
    tools=[tool],
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)

while True:
    question = input("The file is: ")
    if question == "exit":
        break
    result = crew.kickoff(inputs={"question": question})
    print(result)