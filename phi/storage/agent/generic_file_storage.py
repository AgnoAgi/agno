import json
from pathlib import Path
from typing import Union, Any, Optional
from phi.storage.agent.base import AgentStorage
from phi.agent import AgentSession

class GenericFileStorage(AgentStorage):
    def __init__(self, path: Union[str, Path]):
        self.base_path = Path(path)
        self.by_id_path = self.base_path / "by_id"
        self.by_name_path = self.base_path / "by_name"
        self.by_id_path.mkdir(parents=True, exist_ok=True)
        self.by_name_path.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def serialize(self, data: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self) -> Any:
        raise NotImplementedError

    def create(self) -> None:
        """Create the storage if it doesn't exist."""
        if not self.by_id_path.exists():
            self.by_id_path.mkdir(parents=True, exist_ok=True)

    def read(self, session_id: str, user_id: Optional[str] = None) -> Optional[AgentSession]:
        """Read an AgentSession from the storage."""
        session_file = self.by_id_path / f"{session_id}.json"
        if session_file.exists():
            data = self.deserialize(session_file)
            return AgentSession.model_validate(data)
        return None

    def get_all_session_ids(self, user_id: Optional[str] = None, agent_id: Optional[str] = None) -> list[str]:
        """Get all session IDs, optionally filtered by user_id and/or agent_id."""
        session_files = self.by_id_path.glob("*.json")
        session_ids = []
        for session_file in session_files:
            data = self.deserialize(session_file)
            if (not user_id or data['user_id'] == user_id) and (not agent_id or data['agent_id'] == agent_id):
                session_ids.append(data['session_id'])
        return session_ids
        return []

    def get_all_sessions(self, user_id: Optional[str] = None, agent_id: Optional[str] = None) -> list[AgentSession]:
        """Get all sessions, optionally filtered by user_id and/or agent_id."""
        session_files = self.by_id_path.glob("*.json")
        sessions = []
        for session_file in session_files:
            data = self.deserialize(session_file)
            if (not user_id or data['user_id'] == user_id) and (not agent_id or data['agent_id'] == agent_id):
                sessions.append(AgentSession.model_validate(data))
        return sessions
        return []

    def upsert(self, session: AgentSession, create_and_retry: bool = True) -> Optional[AgentSession]:
        """Insert or update an AgentSession in the storage."""
        session_file = self.by_id_path / f"{session.session_id}.json"
        self.serialize(session.dict(), session_file)
        return session

    def delete_session(self, session_id: Optional[str] = None):
        """Delete a session from the storage."""
        if session_id is None:
            return
        session_file = self.by_id_path / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()

    def drop(self) -> None:
        """Drop the storage."""
        if self.by_id_path.exists():
            for session_file in self.by_id_path.glob("*.json"):
                session_file.unlink()

    def upgrade_schema(self) -> None:
        """Upgrade the schema of the storage."""
        pass
