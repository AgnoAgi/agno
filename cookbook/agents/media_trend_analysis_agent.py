"""Please install dependencies using:
pip install openai exa-py phidata firecrawl
"""

from textwrap import dedent
from datetime import datetime, timedelta

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.exa import ExaTools
from phi.tools.firecrawl import FirecrawlTools


def calculate_start_date(days: int) -> str:
    """Calculate start date based on number of days."""
    start_date = datetime.now() - timedelta(days=days)
    return start_date.strftime("%Y-%m-%d")


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        ExaTools(start_published_date=calculate_start_date(30), type="keyword"),
        FirecrawlTools(scrape=True, crawl=False),
    ],
    description=dedent("""\
        You are an expert media trend analyst specializing in:
        1. Identifying emerging trends across news and digital platforms
        2. Recognizing pattern changes in media coverage
        3. Providing actionable insights based on data
        4. Forecasting potential future developments
    """),
    instructions=[
        "Analyze the provided topic according to the user's specifications:",
        "1. Use keywords to perform targeted searches",
        "2. Identify key influencers and authoritative sources",
        "3. Extract main themes and recurring patterns",
        "4. Provide actionable recommendations",
    ],
    expected_output=dedent("""\
    # Media Trend Analysis Report

    ## Executive Summary
    {High-level overview of findings and key metrics}

    ## Trend Analysis
    ### Volume Metrics
    - Total mentions: {count}
    - Peak discussion periods: {dates}
    - Growth rate: {percentage}

    ### Key Themes
    1. {Theme 1}
       - Frequency: {count}
       - Notable mentions: {examples}
    2. {Theme 2}
       - Frequency: {count}
       - Notable mentions: {examples}

    ## Source Analysis
    ### Top Sources
    1. {Source 1}
       - Influence score: {score}
    2. {Source 2}
       - Influence score: {score}

    ## Actionable Insights
    1. {Insight 1}
       - Evidence: {data points}
       - Recommended action: {action}
    2. {Insight 2}
       - Evidence: {data points}
       - Recommended action: {action}

    ## Future Predictions
    1. {Prediction 1}
       - Supporting evidence: {evidence}
    2. {Prediction 2}
       - Supporting evidence: {evidence}

    ## References
    {Detailed source list with links}
    """),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    save_response_to_file="tmp/trend_analysis_{message}.md",
)

# Example usage:
analysis_prompt = """\
Analyze media trends for:
Keywords: artificial intelligence, AI regulation
Sources: techcrunch.com, wired.com, theverge.com
"""

agent.print_response(analysis_prompt, stream=True)

# Alternative prompt example
crypto_prompt = """\
Analyze media trends for:
Keywords: cryptocurrency, bitcoin, ethereum
Sources: coindesk.com, cointelegraph.com
"""

# agent.print_response(crypto_prompt, stream=True)
