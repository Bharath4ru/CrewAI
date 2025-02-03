import os
from dotenv import load_dotenv
from crewai import Agent
from crewai_tools import SerperDevTool
from crewai import Task , LLM
from crewai import Crew, Process

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
os.environ["SERPER_API_KEY"] = SERPER_API_KEY 



     

llm = LLM(
    model="sambanova/Meta-Llama-3.1-8B-Instruct",
    temperature=0.7,
    api_key=os.getenv("SAMBANOVA_API_KEY")
)




search_tool = SerperDevTool()


# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies in {topic}',
    verbose=True,
    memory=True,
    backstory=(
       """ Driven by curiosity, you're at the forefront of
        innovation, eager to explore and share knowledge that could change
        the world."""
    ),
    tools=[search_tool],
    allow_delegation=True,
    llm=llm
)


# Creating a writer agent with custom tools and delegation capability
writer = Agent(
    role='Writer',
    goal='Narrate compelling tech stories about {topic}',
    verbose=True,
    memory=True,
    backstory=(
        """With a flair for simplifying complex topics, you craft
        engaging narratives that captivate and educate, bringing new
        discoveries to light in an accessible manner."""
    ),
    tools=[search_tool],
    allow_delegation=False,
    llm=llm
)


research_task = Task(
    description=(
        "Identify the next big trend in {topic}. "
        "Focus on identifying pros and cons and the overall narrative. "
        "Your final report should clearly articulate the key points, "
        "its market opportunities, and potential risks."
    ),
    expected_output="A comprehensive 3 paragraphs long report on the latest AI trends.",
    tools=[search_tool],
    agent=researcher,
)


write_task = Task(
    description=(
        "Compose an insightful article on {topic}. "
        "Focus on the latest trends and how it's impacting the industry. "
        "This article should be easy to understand, engaging, and positive."
    ),
    expected_output="A 4 paragraph article on {topic} advancements formatted as markdown.",
    tools=[search_tool],
    agent=writer,
    async_execution=False,
    output_file="new-blog-post1.md",
)


# Forming the tech-focused crew with enhanced configurations
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Optional: Sequential task execution is default
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'CrewAI Framework vs Phidata Framework'}) #AgenticAI in healthcare
print(result)
