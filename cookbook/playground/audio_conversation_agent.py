from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage

audio_agent = Agent(
    name="Audio Chat Agent",
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "pcm16"},  # Wav not supported for streaming
    ),
    debug_mode=True,
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    storage=SqliteAgentStorage(table_name="audio_agent", db_file="tmp/audio_agent.db"),
)


app = Playground(agents=[audio_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("audio_conversation_agent:app", reload=True)
