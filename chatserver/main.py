import asyncio
import logging
import signal

import click

from chatserver.config import get_settings
from chatserver.network.server import Server

logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", type=str, help="Host to bind to")
@click.option("--port", type=int, help="TCP port to listen on")
@click.option("--room-name", type=str, help="Chat room name")
@click.option("--max-users", type=int, help="Maximum concurrent users")
@click.option("--history", is_flag=True, help="Enable message history")
@click.option("--history-size", type=int, help="Number of messages in history")
@click.option("--plain-text", is_flag=True, help="Disable ANSI formatting")
@click.option("--log-level", type=str, help="Logging level (DEBUG, INFO, WARNING, ERROR)")
def cli(host, port, room_name, max_users, history, history_size, plain_text, log_level):
    settings = get_settings()
    config_dict = settings.model_dump()
    
    overrides = {
        "host": host,
        "port": port,
        "room_name": room_name,
        "max_users": max_users,
        "history_size": history_size,
        "log_level": log_level,
    }
    
    if history:
        overrides["enable_history"] = True
    if plain_text:
        overrides["plain_text"] = True
    
    config_dict.update({k: v for k, v in overrides.items() if v is not None})
    
    level = config_dict.pop("log_level")
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    
    server = Server(
        host=config_dict["host"],
        port=config_dict["port"],
        room_name=config_dict["room_name"],
        max_users=config_dict["max_users"],
        enable_history=config_dict["enable_history"],
        history_size=config_dict["history_size"],
        plain_text=config_dict["plain_text"]
    )
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    def signal_handler():
        logger.info("Received shutdown signal")
        loop.create_task(server.stop())
        loop.stop()
    
    signal.signal(signal.SIGINT, lambda *_: signal_handler())
    signal.signal(signal.SIGTERM, lambda *_: signal_handler())
    
    try:
        loop.run_until_complete(server.run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(server.stop())
        loop.close()


if __name__ == "__main__":
    cli()






