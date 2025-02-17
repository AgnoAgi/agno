import requests

from agno.agent.agent import Agent
from agno.media import Audio, Image, Video
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools


def test_image_input():
    agent = Agent(
        model=Gemini(id="gemini-1.5-flash"),
        tools=[DuckDuckGoTools()],
        markdown=True,
        telemetry=False,
        monitoring=False
    )

    response = agent.run(
        "Tell me about this image and give me the latest news about it.",
        images=[Image(url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg")],
    )

    assert "golden" in response.content.lower()


def test_audio_input_bytes():
    # Fetch the audio file and convert it to a base64 encoded string
    url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
    response = requests.get(url)
    response.raise_for_status()
    wav_data = response.content

    # Provide the agent with the audio file and get result as text
    agent = Agent(
        model=Gemini(id="gemini-1.5-flash"),
        markdown=True,
        telemetry=False,
        monitoring=False
    )
    response = agent.run("What is in this audio?", audio=[Audio(content=wav_data, format="wav")])

    assert response.content is not None


def test_audio_input_url():
    agent = Agent(
        model=Gemini(id="gemini-1.5-flash"),
        markdown=True,
        telemetry=False,
        monitoring=False
    )

    response = agent.run(
        "What is in this audio?",
        audio=[Audio(url="https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav")],
    )

    assert response.content is not None


def test_video_input_bytes():
    agent = Agent(
        model=Gemini(id="gemini-1.5-flash"),
        markdown=True,
        telemetry=False,
        monitoring=False
    )

    url = "https://videos.pexels.com/video-files/5752729/5752729-uhd_2560_1440_30fps.mp4"

    # Download the video file from the URL as bytes
    response = requests.get(url)
    video_content = response.content

    response = agent.run(
        "Tell me about this video",
        videos=[Video(content=video_content)],
    )

    assert response.content is not None
