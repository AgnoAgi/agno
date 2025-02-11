from typing import Iterator  # noqa
from agno.agent import Agent, RunResponse  # noqa
from agno.models.aws.bedrock import AwsBedrock

agent = Agent(
    model=AwsBedrock(id="mistral.mistral-small-2402-v1:0"), markdown=True
)

# Get the response in a variable
# run_response: Iterator[RunResponse] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story", stream=True)
