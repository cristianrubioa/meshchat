import asyncio
import logging
from dataclasses import dataclass, field

from chatserver.core.room import Room
from chatserver.core.client import Client

logger = logging.getLogger(__name__)


@dataclass
class Server:
    host: str
    port: int
    room_name: str
    max_users: int
    enable_history: bool
    history_size: int
    plain_text: bool
    
    room: Room = field(init=False)
    server: asyncio.Server | None = field(default=None, init=False)
    connections: list[Client] = field(default_factory=list, init=False)
    
    def __post_init__(self):
        self.room = Room(
            name=self.room_name,
            max_users=self.max_users,
            enable_history=self.enable_history,
            history_size=self.history_size,
            plain_text=self.plain_text
        )
    
    async def start(self):
        self.room.start()
        
        self.server = await asyncio.start_server(
            self._handle_connection,
            self.host,
            self.port
        )
        
        addr = self.server.sockets[0].getsockname()
        logger.info(f"Server started on {addr[0]}:{addr[1]} (room: {self.room_name}, max users: {self.max_users})")
        logger.info(f"Connect with: nc localhost {self.port}")
    
    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        logger.info(f"New connection from {addr}")
        
        client = Client(reader, writer, self.room)
        self.connections.append(client)
        
        try:
            if await client.initialize():
                await client.handle()
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
        finally:
            if client in self.connections:
                self.connections.remove(client)
            await client.close()
            logger.info(f"Connection from {addr} closed")
    
    async def stop(self):
        logger.info("Stopping server...")
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        close_tasks = [client.close() for client in self.connections]
        await asyncio.gather(*close_tasks, return_exceptions=True)
        
        await self.room.stop()
        
        logger.info("Server stopped")
    
    async def run(self):
        await self.start()
        
        async with self.server:
            await self.server.serve_forever()

