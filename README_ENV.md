# Development Guide

This document contains development setup, configuration, architecture details, and environment variable information for MeshChat.

## Development Setup

### Prerequisites
- Python 3.11+
- Poetry

### Install Dependencies

```bash
poetry install
```

### Development Mode

```bash
poetry shell
meshchat --help
```

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=chatserver

# Run specific test file
poetry run pytest test/test_basic.py -v
```

## Code Quality

```bash
# Check code style
poetry run ruff check chatserver/

# Format code
poetry run ruff format chatserver/
```

## Architecture

```
meshchat/
├── chatserver/
│   ├── core/           # Core chat logic
│   │   ├── client.py   # Client connection handler
│   │   ├── room.py     # Chat room management
│   │   └── message.py  # Message model
│   ├── network/        # Network layer
│   │   └── server.py   # TCP server implementation
│   ├── ui/             # User interface
│   │   └── formatter.py # ANSI formatting
│   └── main.py         # Application entry point
└── test/               # Tests
```

## How It Works

1. **Server** - Listens for TCP connections on specified port
2. **Client Connection** - Each connection creates a Client instance
3. **Room Management** - All clients join a shared Room
4. **Message Broadcasting** - Messages are broadcast to all connected clients
5. **ANSI Formatting** - Messages are styled with colors for better readability

## Technical Stack

- **Language**: Python 3.11+
- **Async Framework**: asyncio
- **CLI**: Typer
- **Terminal UI**: Rich
- **Rate Limiting**: aiolimiter
- **Settings**: pydantic-settings
- **Testing**: pytest, pytest-asyncio
- **Linting**: ruff

## Configuration

### Command-Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--port` | `-p` | 2323 | TCP port to listen on |
| `--room-name` | `-r` | "Chat Room" | Name displayed in the chat |
| `--max-users` | `-m` | 10 | Maximum concurrent users |
| `--history` | | False | Enable message history for new users |
| `--history-size` | | 50 | Number of messages to keep in history |
| `--plain-text` | | False | Disable ANSI formatting |

### Environment Variables

All variables use the `MESHCHAT_` prefix:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MESHCHAT_HOST` | str | 0.0.0.0 | Host address to bind |
| `MESHCHAT_PORT` | int | 2323 | TCP port |
| `MESHCHAT_ROOM_NAME` | str | "Chat Room" | Room name |
| `MESHCHAT_MAX_USERS` | int | 10 | Maximum users |
| `MESHCHAT_ENABLE_HISTORY` | bool | false | Enable history |
| `MESHCHAT_HISTORY_SIZE` | int | 50 | History size |
| `MESHCHAT_PLAIN_TEXT` | bool | false | Plain text mode |
| `MESHCHAT_LOG_LEVEL` | str | INFO | Log level |
| `MESHCHAT_MAX_MESSAGE_LENGTH` | int | 1000 | Max message length |
| `MESHCHAT_RATE_LIMIT_MAX_MESSAGES` | int | 5 | Rate limit messages |
| `MESHCHAT_RATE_LIMIT_WINDOW_SECONDS` | int | 5 | Rate limit window |
| `MESHCHAT_MAX_NICKNAME_LEN` | int | 20 | Max nickname length |
| `MESHCHAT_MIN_NICKNAME_LEN` | int | 2 | Min nickname length |

### Using .env File

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit the file with your settings:
```env
MESHCHAT_HOST=0.0.0.0
MESHCHAT_PORT=2323
MESHCHAT_ROOM_NAME="Chat Room"
MESHCHAT_MAX_USERS=10
MESHCHAT_ENABLE_HISTORY=false
MESHCHAT_HISTORY_SIZE=50
MESHCHAT_PLAIN_TEXT=false
MESHCHAT_LOG_LEVEL=INFO
MESHCHAT_MAX_MESSAGE_LENGTH=1000
MESHCHAT_RATE_LIMIT_MAX_MESSAGES=5
MESHCHAT_RATE_LIMIT_WINDOW_SECONDS=5
MESHCHAT_MAX_NICKNAME_LEN=20
MESHCHAT_MIN_NICKNAME_LEN=2
```

### Configuration Priority

Settings are loaded in the following order (later overrides earlier):

1. **Default values** - Defined in code
2. **Environment variables** - From `.env` file  
3. **Command-line arguments** - Override everything

Examples:

```bash
# Uses .env values
poetry run meshchat

# Overrides port and room name from .env
poetry run meshchat --port 3000 --room-name "Dev Room"
```

### Configuration Cache

The configuration uses `@lru_cache` to avoid repeated reads of the `.env` file.
