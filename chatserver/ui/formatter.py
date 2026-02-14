from chatserver.ui.constants import (
    USER_COLORS,
    RESET,
    BOLD,
    ITALIC,
    DIM,
    SYSTEM_COLOR,
    ACCENT_COLOR,
    INFO_COLOR,
)


def get_user_color(username: str) -> str:
    hash_val = sum(ord(c) * (i * 7 + 13) for i, c in enumerate(username))
    return USER_COLORS[hash_val % len(USER_COLORS)]


class Formatter:
    def __init__(self, plain_text: bool = False):
        self.plain_text = plain_text
    
    def format_system_message(self, message: str) -> str:
        if self.plain_text:
            return f"[System] {message}"
        return f"{SYSTEM_COLOR}{BOLD}[System]{RESET} {SYSTEM_COLOR}{message}{RESET}"
    
    def format_user_message(self, username: str, message: str, timestamp: str) -> str:
        if self.plain_text:
            return f"[{timestamp}] {username}: {message}"
        
        color = get_user_color(username)
        return f"{DIM}[{timestamp}]{RESET} {color}{BOLD}{username}:{RESET} {message}"
    
    def format_action_message(self, username: str, action: str) -> str:
        if self.plain_text:
            return f"* {username} {action}"
        
        color = get_user_color(username)
        return f"{color}{ITALIC}* {username} {action}{RESET}"
    
    def format_title(self, title: str) -> str:
        if self.plain_text:
            return f"=== {title} ==="
        return f"{ACCENT_COLOR}{BOLD}=== {title} ==={RESET}"
    
    def format_banner(self, banner: str) -> str:
        if self.plain_text:
            return banner
        return f"{SYSTEM_COLOR}{BOLD}{banner}{RESET}"
    
    def format_welcome_message(self, room_name: str, nickname: str) -> str:
        if self.plain_text:
            return f"Welcome to {room_name}, {nickname}!\n\nType a message and press Enter to send. Use /help to see available commands."
        
        return f"{ACCENT_COLOR}{BOLD}Welcome to {INFO_COLOR}{room_name}{ACCENT_COLOR}, {nickname}!{RESET}\n\nType a message and press Enter to send. Use /help to see available commands."
    
    def format_help(self) -> str:
        if self.plain_text:
            return """Available Commands:
/who - Show all users in the room
/me <action> - Perform an action
/help - Show this help message
/quit - Leave the chat"""
        
        return f"""{ACCENT_COLOR}{BOLD}Available Commands:{RESET}
{INFO_COLOR}{BOLD}/who{RESET} - Show all users in the room
{INFO_COLOR}{BOLD}/me <action>{RESET} - Perform an action
{INFO_COLOR}{BOLD}/help{RESET} - Show this help message
{INFO_COLOR}{BOLD}/quit{RESET} - Leave the chat"""
    
    def format_user_list(self, room_name: str, users: list[str], max_users: int) -> str:
        if self.plain_text:
            result = f"Users in {room_name} ({len(users)}/{max_users}):\n"
            for user in users:
                result += f"- {user}\n"
            return result.rstrip()
        
        result = f"{ACCENT_COLOR}{BOLD}Users in {room_name} {INFO_COLOR}({len(users)}/{max_users}):{RESET}\n"
        for user in users:
            color = get_user_color(user)
            result += f"{DIM}- {RESET}{color}{BOLD}{user}{RESET}\n"
        
        return result.rstrip()
