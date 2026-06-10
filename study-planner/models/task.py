from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    name: str
    deadline: datetime
    difficulty: int
