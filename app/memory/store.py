from typing import Dict, List, TypedDict


class MemoryItem(TypedDict):
    role: str
    content: str


class InMemoryStore:
    def __init__(self):
        self._data: Dict[str, List[MemoryItem]] = {}

    def add(self, user_id: str, role: str, content: str):
        self._data.setdefault(user_id, []).append({"role": role, "content": content})
        self._data[user_id] = self._data[user_id][-20:]

    def get(self, user_id: str) -> List[MemoryItem]:
        return self._data.get(user_id, [])
