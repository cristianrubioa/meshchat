from dataclasses import dataclass

from chatserver.config import get_settings


settings = get_settings()


@dataclass
class NicknameEmptyError(Exception):
    def __str__(self):
        return "Nickname cannot be empty. Please try again."


@dataclass
class NicknameTooShortError(Exception):
    def __str__(self):
        return f"Nickname must be at least {settings.min_nickname_len} characters."


@dataclass
class NicknameTooLongError(Exception):
    def __str__(self):
        return f"Nickname must be at most {settings.max_nickname_len} characters."


@dataclass
class NicknameReservedError(Exception):
    def __str__(self):
        return "Nickname 'System' is reserved. Please choose another nickname."


@dataclass
class NicknameInvalidCharsError(Exception):
    def __str__(self):
        return "Nickname can only contain letters, numbers, underscores, and hyphens."


@dataclass
class NicknameTakenError(Exception):
    nickname: str
    
    def __str__(self):
        return f"Nickname '{self.nickname}' is already taken. Please choose another."


@dataclass
class MessageTooLongError(Exception):
    def __str__(self):
        return f"Message is too long (max {settings.max_message_length} characters)."


@dataclass
class RateLimitError(Exception):
    def __str__(self):
        return "You are sending messages too quickly. Please slow down."


@dataclass
class RoomFullError(Exception):
    def __str__(self):
        return "The chat room is currently full. Please try again later."


@dataclass
class UnknownCommandError(Exception):
    command: str
    
    def __str__(self):
        return f"Unknown command: {self.command}"
