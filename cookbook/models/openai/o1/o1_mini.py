from agno.agent import Agent, RunResponse  # noqa
from agno.models.openai import OpenAI

agent = Agent(model=OpenAI(id="o1-mini"))

# Print the response in the terminal
agent.print_response("What is the closest galaxy to milky way?")
