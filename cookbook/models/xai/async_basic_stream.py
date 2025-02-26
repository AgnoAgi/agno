import asyncio
from os import getenv
from typing import Iterator  # noqa

from agno.agent import Agent, RunResponse  # noqa
from agno.models.xai import xAI

agent = Agent(model=xAI(id="grok-beta"), api_key=getenv("XAI_API_KEY"), markdown=True)

# Get the response in a variable
# run_response: Iterator[RunResponse] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)

# Print the response in the terminal
asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
