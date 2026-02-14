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

## Usage Examples

Start a basic server:
```bash
poetry run meshchat
```

With custom settings:
```bash
poetry run meshchat --port 3000 --room-name "Python Devs" --history
```

See all options:
```bash
poetry run meshchat --help
```

## Chat Commands

| Command | Description |
|---------|-------------|
| `/who` | List all users in the room |
| `/me <action>` | Send an action message (e.g., `/me waves`) |
| `/help` | Show available commands |
| `/quit` | Disconnect from chat |

## Development

For development setup, configuration details, and architecture information, see [README_ENV.md](README_ENV.md).

## License

BSD-3-Clause license
