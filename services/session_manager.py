import time
import logging
from pathlib import Path
from typing import Dict, Any, List
from utils.cleanup import delete_file

logger = logging.getLogger(__name__)

class UserSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.photos: List[str] = []  # List of local file paths
        self.layout: str = "auto"
        self.bg_color: str = "#FFFFFF"
        self.spacing: int = 15
        self.corner_radius: int = 0
        self.fit_mode: str = "crop"
        self.title: str | None = None
        self.state: str = "IDLE"  # IDLE, AWAITING_PHOTOS, AWAITING_HEX, AWAITING_TITLE
        self.last_active: float = time.time()

    def touch(self):
        self.last_active = time.time()

    def clear_photos(self):
        for path in self.photos:
            delete_file(path)
        self.photos.clear()

class SessionManager:
    def __init__(self, timeout_seconds: int = 1800):
        self._sessions: Dict[int, UserSession] = {}
        self.timeout_seconds = timeout_seconds

    def get_session(self, user_id: int) -> UserSession:
        self.cleanup_expired()
        if user_id not in self._sessions:
            self._sessions[user_id] = UserSession(user_id)
        else:
            self._sessions[user_id].touch()
        return self._sessions[user_id]

    def add_photo(self, user_id: int, file_path: str) -> int:
        session = self.get_session(user_id)
        session.photos.append(file_path)
        session.touch()
        return len(session.photos)

    def delete_session(self, user_id: int) -> None:
        if user_id in self._sessions:
            self._sessions[user_id].clear_photos()
            del self._sessions[user_id]

    def cleanup_expired(self) -> None:
        now = time.time()
        expired_users = [
            uid for uid, session in self._sessions.items()
            if now - session.last_active > self.timeout_seconds
        ]
        for uid in expired_users:
            logger.info(f"Cleaning up expired session for user {uid}")
            self.delete_session(uid)

session_manager = SessionManager()
