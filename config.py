"""
Discord Self-Bot Configuration
============================
A comprehensive configuration file containing all settings, API tokens,
and customizable options for the Discord self-bot.

Author: raiyan
Version: 1.0
"""

import colorama
from colorama import Fore, Style

colorama.init()

# Core Bot Configuration
# ====================
class BotConfig:
    """Core bot settings and authentication"""
    TOKEN = 'User-Discord-User-Token'          # Your Discord user token
    USER_ID = Your-User-ID        # Your Discord user ID
    PREFIX = "."                       # Command prefix for the bot
    COMMAND_COOLDOWN = 3               # Cooldown between commands (seconds)
    DELETE_COMMANDS = True             # Auto-delete command messages
    BOT_NAME = "Raiyan Bot"           # Name of the bot
    BOT_VERSION = "3.1.0"             # Bot version

# Help Command Settings
# ===================
class HelpConfig:
    """Help command configuration and categories"""
    
    class Categories:
        """Command categories and their emojis"""
        GENERAL = {"name": "General", "emoji": "⚙️"}
        UTILITY = {"name": "Utility", "emoji": "🛠️"}
        INFORMATION = {"name": "Information", "emoji": "ℹ️"}
        MODERATION = {"name": "Moderation", "emoji": "🛡️"}
        FUN = {"name": "Fun", "emoji": "🎮"}
        TOOLS = {"name": "Tools", "emoji": "🔧"}
        NSFW = {"name": "NSFW", "emoji": "🔞"}
        MISC = {"name": "Miscellaneous", "emoji": "📦"}
    
    class Display:
        """Help command display settings"""
        SHOW_ALIASES = True            # Show command aliases
        SHOW_COOLDOWNS = True          # Show command cooldowns
        SHOW_PERMISSIONS = True        # Show required permissions
        COMPACT_VIEW = False           # Use compact view
        SHOW_HIDDEN = False           # Show hidden commands
        COLOR_CODE = 0x2b2d31        # Embed color (Discord dark theme)
    
    class Formatting:
        """Help command formatting settings"""
        TITLE = "Command Help Menu"    # Help command title
        FOOTER = "Type {prefix}help <command> for detailed information"  # Footer text
        CATEGORY_SEPARATOR = "\n"      # Separator between categories
        COMMAND_SEPARATOR = " | "      # Separator between commands
        MAX_COMMANDS_PER_PAGE = 10    # Maximum commands per page

# API Configuration
# ===============
class APIConfig:
    """API tokens and endpoints for various services"""
    
    class Discord:
        """Discord-specific API settings"""
        API_VERSION = 'v9'
        BASE_URL = 'https://canary.discordapp.com/api'
    
    class IPServices:
        """IP information service tokens"""
        IPINFO_TOKEN = '6505155fbcd91a'
        ABUSEIPDB_TOKEN = '41d3b27ffb6a1d'
        GENERAL_API_KEY = 'a91c8e0d5897462581c0c923ada079e5'

# Display Settings
# ==============
class DisplayConfig:
    """Visual and display-related settings"""
    
    class Colors:
        """Color settings for various displays"""
        SUCCESS = Fore.GREEN
        ERROR = Fore.RED
        WARNING = Fore.YELLOW
        INFO = Fore.CYAN
        RESET = Style.RESET_ALL
    
    class ASCII:
        """ASCII art configuration"""
        FONT = 'standard'              # Default figlet font
        ENABLED = True                 # Enable ASCII art
        WIDTH = 50                     # Maximum width for ASCII art

# Command Settings
# ==============
class CommandConfig:
    """Settings for specific command behaviors"""
    
    class Calculator:
        """Calculator command settings"""
        DECIMAL_PLACES = 6             # Number of decimal places in results
        SCIENTIFIC_NOTATION = True     # Enable scientific notation
        MAX_DIGITS = 15               # Maximum digits to display
    
    class IPLookup:
        """IP lookup command settings"""
        MAX_AGE_DAYS = 90             # Maximum age for abuse reports
        SHOW_DOMAINS = True           # Show hosted domains
        MAX_DOMAINS = 5               # Maximum domains to display
    
    class TokenInfo:
        """Token info command settings"""
        SHOW_EMAIL = True             # Whether to show email
        SHOW_PHONE = True            # Whether to show phone number
        SAFE_MODE = True             # Hide sensitive information

# Timing Settings
# =============
class TimingConfig:
    """Timing and delay settings"""
    DELETE_TIMEOUT = 30               # Message deletion timeout (seconds)
    RESPONSE_TIMEOUT = 60            # Bot response timeout (seconds)
    EDIT_TIMEOUT = 15               # Message edit timeout (seconds)
    TYPING_DURATION = 2             # Typing indicator duration (seconds)

# Security Settings
# ==============
class SecurityConfig:
    """Security and protection settings"""
    SAFE_MODE = True                 # Enable additional safety checks
    LOG_COMMANDS = True              # Log command usage
    ENCRYPT_TOKENS = True            # Encrypt stored tokens
    MAX_RETRIES = 3                 # Maximum API request retries

# System Settings
# =============
class SystemConfig:
    """System-related settings"""
    CHECK_UPDATES = True             # Check for bot updates
    DEBUG_MODE = False              # Enable debug logging
    SAVE_LOGS = True               # Save logs to file
    MAX_MEMORY_MB = 512           # Maximum memory usage

"""
DISCLAIMER AND USAGE TERMS
=========================
This bot is created by raiyan and is not open source. By using this bot, you agree to the following:

1. You are responsible for any consequences of using or modifying this bot
2. The creator is not liable for account bans or disabilities
3. This bot is for educational purposes only
4. Modifications are at your own risk

For support or inquiries:
- Discord: _raiyan_01
- Version: 3.1.0
- Last Updated: 11/03/2025
"""
