import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from chatserver.config import get_settings
from chatserver.ui.constants import (
    CURSOR_UP,
    CLEAR_LINE,
    CURSOR_TO_START,
    INPUT_PROMPT,
)
from chatserver.core.validators import validate_nickname
from chatserver.core.exceptions import (
    NicknameTakenError,
    MessageTooLongError,
    RateLimitError,
    RoomFullError,
)
from chatserver.ui.banner import BANNER
from chatserver.ui.formatter import Formatter
from chatserver.core.message import Message

if TYPE_CHECKING:
    from chatserver.core.room import Room

logger = logging.getLogger(__name__)

settings = get_settings()


@dataclass
class Client:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    room: "Room"
    
    nickname: str = field(default="")
    formatter: Formatter = field(init=False)
    full_room_rejection: bool = field(default=False, init=False)
    message_timestamps: list[datetime] = field(default_factory=list, init=False)
    _write_lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)
    
    def __post_init__(self):
        self.formatter = Formatter(plain_text=self.room.plain_text)
        
    async def initialize(self) -> bool:
        try:
            if not await self._request_nickname():
                return False
            
            await self.room.join(self)
            
            if self.full_room_rejection:
                await self._write(f"{RoomFullError()}\r\n")
                return False
            
            if not await self._send_welcome_message():
                await self.room.leave(self)
                return False
            
            await self._send_history()
            
            return True
        except Exception as e:
            logger.error(f"Error initializing client: {e}")
            return False
    
    async def _request_nickname(self) -> bool:
        try:
            welcome = self.formatter.format_title("Welcome to MeshChat")
            await self._write(f"{welcome}\r\n\r\n")
            
            while True:
                await self._write("Please enter your nickname: ")
                
                line = await self.reader.readline()
                if not line:
                    return False
                
                nickname = line.decode("utf-8", errors="ignore").strip()
                
                try:
                    validate_nickname(nickname)
                except Exception as e:
                    await self._write(f"{e}\r\n")
                    continue
                
                if not self.room.reserve_nickname(nickname):
                    await self._write(f"{NicknameTakenError(nickname)}\r\n")
                    continue
                
                self.nickname = nickname
                return True
                
        except Exception as e:
            logger.error(f"Error requesting nickname: {e}")
            return False
    
    async def _send_welcome_message(self) -> bool:
        try:
            colored_banner = self.formatter.format_banner(BANNER)
            await self._write(f"{colored_banner}\r\n")
            
            welcome_msg = self.formatter.format_welcome_message(self.room.name, self.nickname)
            await self._write(f"{welcome_msg}\r\n\r\n")
            
            return True
        except Exception as e:
            logger.error(f"Error sending welcome message: {e}")
            return False
    
    async def _send_history(self):
        history = self.room.get_history()
        if not history:
            return
        
        header = self.formatter.format_system_message("--- Recent messages ---")
        await self._write(f"{header}\r\n")
        
        for msg in history:
            await self.send_message(msg)
        
        footer = self.formatter.format_system_message("--- End of history ---")
        await self._write(f"{footer}\r\n\r\n")
    
    async def handle(self):
        try:
            await self._show_prompt()
            
            while True:
                try:
                    line = await asyncio.wait_for(self.reader.readline(), timeout=30.0)
                except asyncio.TimeoutError:
                    continue
                
                if not line:
                    break
                
                message = line.decode("utf-8", errors="ignore").strip()
                
                await self._clear_input_line()
                
                if not message:
                    await self._show_prompt()
                    continue
                
                if len(message) > settings.max_message_length:
                    await self.send_system_message(str(MessageTooLongError()))
                    await self._show_prompt()
                    continue
                
                if not message.startswith("/quit"):
                    try:
                        self._check_rate_limit()
                    except RateLimitError as e:
                        await self.send_system_message(str(e))
                        await self._show_prompt()
                        continue
                
                if message.startswith("/"):
                    await self._handle_command(message)
                else:
                    await self.room.broadcast(Message(
                        from_user=self.nickname,
                        content=message,
                        timestamp=datetime.now()
                    ))
                
                await self._show_prompt()
                
        except Exception as e:
            logger.error(f"Error handling client {self.nickname}: {e}")
        finally:
            await self.room.leave(self)
            await self.close()
    
    async def _clear_input_line(self):
        if not self.room.plain_text:
            await self._write(f"{CURSOR_UP}{CLEAR_LINE}{CURSOR_TO_START}")
    
    async def _show_prompt(self):
        await self._write(INPUT_PROMPT)
    
    def _check_rate_limit(self):
        now = datetime.now()
        self.message_timestamps.append(now)
        
        cutoff = now - timedelta(seconds=settings.rate_limit_window_seconds)
        self.message_timestamps = [ts for ts in self.message_timestamps if ts > cutoff]
        
        if len(self.message_timestamps) > settings.rate_limit_max_messages:
            raise RateLimitError()
    
    async def _handle_command(self, cmd: str):
        parts = cmd.split(" ", 1)
        command = parts[0].lower()
        
        if command == "/who":
            await self._show_user_list()
        elif command == "/me":
            if len(parts) < 2 or not parts[1].strip():
                await self.send_system_message("Usage: /me <action>")
            else:
                await self.room.broadcast(Message(
                    from_user=self.nickname,
                    content=parts[1],
                    timestamp=datetime.now(),
                    is_action=True
                ))
        elif command == "/help":
            await self._show_help()
        elif command == "/quit":
            await self.send_system_message("Goodbye!")
            await self.close()
        else:
            await self.send_system_message("Unknown command. Type /help for available commands.")
    
    async def _show_user_list(self):
        users = self.room.get_user_list()
        msg = self.formatter.format_user_list(self.room.name, users, self.room.max_users)
        await self._write(f"{msg}\r\n")
    
    async def _show_help(self):
        help_msg = self.formatter.format_help()
        await self._write(f"{help_msg}\r\n")
    
    async def send_system_message(self, content: str):
        msg = Message(
            from_user="System",
            content=content,
            timestamp=datetime.now(),
            is_system=True
        )
        await self.send_message(msg)
    
    async def send_message(self, msg: Message):
        time_str = msg.timestamp.strftime("%H:%M:%S")
        
        if msg.is_system:
            formatted = self.formatter.format_system_message(msg.content)
        elif msg.is_action:
            formatted = self.formatter.format_action_message(msg.from_user, msg.content)
        else:
            formatted = self.formatter.format_user_message(msg.from_user, msg.content, time_str)
        
        await self._write(f"{formatted}\r\n")
    
    async def _write(self, data: str):
        async with self._write_lock:
            try:
                self.writer.write(data.encode("utf-8"))
                await self.writer.drain()
            except Exception as e:
                logger.error(f"Error writing to {self.nickname}: {e}")
    
    async def close(self):
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except Exception:
            pass
