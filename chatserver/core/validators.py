from chatserver.config import get_settings
from chatserver.core.exceptions import (
    NicknameEmptyError,
    NicknameTooShortError,
    NicknameTooLongError,
    NicknameReservedError,
    NicknameInvalidCharsError,
)

settings = get_settings()


def validate_nickname(nickname: str):
    if not nickname:
        raise NicknameEmptyError()
    
    if len(nickname) < settings.min_nickname_len:
        raise NicknameTooShortError()
    
    if len(nickname) > settings.max_nickname_len:
        raise NicknameTooLongError()
    
    if nickname.lower() == "system":
        raise NicknameReservedError()
    
    if not all(c.isalnum() or c in ("_", "-") for c in nickname):
        raise NicknameInvalidCharsError()
