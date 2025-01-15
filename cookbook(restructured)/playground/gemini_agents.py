from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.playground import Playground, serve_playground_app
from agno.models.google import Gemini

finance_agent = Agent(
    name="Finance Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[YFinanceTools(stock_price=True)],
    debug_mode=True,
)

app = Playground(agents=[finance_agent]).get_app(use_async=False)

if __name__ == "__main__":
    serve_playground_app("gemini_agents:app", reload=True)
