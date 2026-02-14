from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    from_user: str
    content: str
    timestamp: datetime
    is_system: bool = False
    is_action: bool = False
