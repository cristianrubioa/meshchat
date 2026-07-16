from chatserver.config import get_settings


def test_config_settings():
    settings = get_settings()

    assert settings.host == "0.0.0.0"
    assert settings.port == 2323
    assert settings.room_name == "Chat Room"
    assert settings.max_users == 10
    assert settings.max_message_length == 1000
    assert settings.rate_limit_max_messages == 5
    assert settings.rate_limit_window_seconds == 5
    assert settings.max_nickname_len == 20
    assert settings.min_nickname_len == 2


def test_config_immutable():
    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2
