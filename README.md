# MeshChat

A terminal-based chat application built in Python. Share a chat room over your network - users connect via netcat or telnet, no client installation needed.

## Features

- **Zero Client Setup** - Users connect with just `nc` or `telnet`
- **Colorful UI** - Each user gets a unique color, styled messages with ANSI colors
- **Message History** - New users can see recent chat history (optional)
- **Chat Commands** - `/who`, `/me`, `/help`, `/quit`
- **Rate Limiting** - Built-in protection against spam
- **Async I/O** - Built with Python asyncio for efficient connection handling

## Quick Start

```bash
# Install dependencies
poetry install

# Run server
poetry run meshchat

# Or with options
poetry run meshchat --port 2323 --room-name "My Room" --history
```

Connect from any machine:
```bash
nc localhost 2323
# or
telnet localhost 2323
```

## Installation

### From Source

```bash
git clone <repo-url>
cd meshchat
poetry install
```

### Development Mode

```bash
poetry install
poetry shell
meshchat --help
```

## Configuration

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--port` | `-p` | 2323 | TCP port to listen on |
| `--room-name` | `-r` | "Chat Room" | Name displayed in the chat |
| `--max-users` | `-m` | 10 | Maximum concurrent users |
| `--history` | | False | Enable message history for new users |
| `--history-size` | | 50 | Number of messages to keep in history |
| `--plain-text` | | False | Disable ANSI formatting |

## Examples

### Basic Usage

Start a server on the default port:
```bash
poetry run meshchat
```

### Custom Room

Start a server with a custom room name and port:
```bash
poetry run meshchat --port 3000 --room-name "Python Devs" --max-users 20
```

### With Message History

Enable history so new users can see recent messages:
```bash
poetry run meshchat --history --history-size 100
```

### Plain Text Mode

For clients that don't support ANSI colors:
```bash
poetry run meshchat --plain-text
```

## Chat Commands

| Command | Description |
|---------|-------------|
| `/who` | List all users in the room |
| `/me <action>` | Send an action (e.g., `/me waves` → `* Alice waves`) |
| `/help` | Show available commands |
| `/quit` | Disconnect from chat |

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

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=chatserver

# Run specific test file
poetry run pytest test/test_basic.py -v
```

### Code Quality

```bash
# Check code style
poetry run ruff check chatserver/

# Format code
poetry run ruff format chatserver/
```

## How It Works

1. **Server** - Listens for TCP connections on specified port
2. **Client Connection** - Each connection creates a Client instance
3. **Room Management** - All clients join a shared Room
4. **Message Broadcasting** - Messages are broadcast to all connected clients
5. **ANSI Formatting** - Messages are styled with colors for better readability

## Technical Details

- **Language**: Python 3.11+
- **Async Framework**: asyncio
- **CLI**: argparse
- **Testing**: pytest
- **Linting**: ruff

## License

MIT
## Configuration with Environment Variables

### Using .env file

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:
```env
MESHCHAT_HOST=0.0.0.0
PORT=2323
ROOM_NAME="Chat Room"
MAX_USERS=10
ENABLE_HISTORY=false
HISTORY_SIZE=50
PLAIN_TEXT=false
LOG_LEVEL=INFO
MESHCHAT_MAX_MESSAGE_LENGTH=1000
MESHCHAT_RATE_LIMIT_MAX_MESSAGES=5
MESHCHAT_RATE_LIMIT_WINDOW_SECONDS=5
MESHCHAT_MAX_NICKNAME_LEN=20
MESHCHAT_MIN_NICKNAME_LEN=2
```

### Configuration Priority

Settings are loaded in the following order (later overrides earlier):
1. Default values (defined in code)
2. Environment variables from `.env` file
3. Command-line arguments

Example:
```bash
# Uses .env values
poetry run meshchat

# Overrides port and room name from .env
poetry run meshchat --port 3000 --room-name "Dev Room"
```
