import asyncio
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

from chatserver.core.message import Message

if TYPE_CHECKING:
    from chatserver.core.client import Client

logger = logging.getLogger(__name__)


@dataclass
class Room:
    name: str
    max_users: int
    enable_history: bool
    history_size: int
    plain_text: bool
    
    clients: dict[str, "Client | None"] = field(default_factory=dict)
    history: deque[Message] = field(default_factory=deque)
    
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)
    _broadcast_queue: asyncio.Queue[Message] = field(default_factory=asyncio.Queue, init=False, repr=False)
    _running: bool = field(default=False, init=False, repr=False)
    _task: asyncio.Task | None = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        self.history = deque(maxlen=self.history_size)
    
    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())
    
    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
    
    async def _run(self):
        try:
            while self._running:
                msg = await self._broadcast_queue.get()
                await self._broadcast_message(msg)
        except asyncio.CancelledError:
            pass
    
    async def join(self, client: "Client"):
        async with self._lock:
            active_count = sum(1 for c in self.clients.values() if c is not None)
            
            if active_count >= self.max_users:
                if client.nickname in self.clients:
                    del self.clients[client.nickname]
                client.full_room_rejection = True
                return
            
            self.clients[client.nickname] = client
        
        await self.broadcast(Message(
            from_user="System",
            content=f"{client.nickname} has joined the room",
            timestamp=datetime.now(),
            is_system=True
        ))
    
    async def leave(self, client: "Client"):
        async with self._lock:
            if client.nickname in self.clients:
                del self.clients[client.nickname]
                should_broadcast = True
            else:
                should_broadcast = False
        
        if should_broadcast:
            await self.broadcast(Message(
                from_user="System",
                content=f"{client.nickname} has left the room",
                timestamp=datetime.now(),
                is_system=True
            ))
    
    async def broadcast(self, msg: Message):
        await self._broadcast_queue.put(msg)
    
    async def _broadcast_message(self, msg: Message):
        if self.enable_history:
            self.history.append(msg)
        
        async with self._lock:
            clients = [client for client in self.clients.values() if client is not None]
        
        tasks = [client.send_message(msg) for client in clients]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_history(self) -> list[Message]:
        return list(self.history)
    
    def get_user_list(self) -> list[str]:
        return list(self.clients.keys())
    
    def reserve_nickname(self, nickname: str) -> bool:
        if nickname in self.clients:
            return False
        self.clients[nickname] = None
        return True
