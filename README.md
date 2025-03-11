<div align="center">
  
# 🤖 Raiyan Selfbot

[![Version](https://img.shields.io/badge/version-3.1-blue.svg)](https://raiyanhossain.net)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-1.7.3-blue.svg)](https://discordpy.readthedocs.io/en/stable/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<img src="https://img.raiyanhossain.net/img/logo.png" alt="Raiyan Selfbot Logo" width="200"/>

*A powerful and feature-rich Discord selfbot with moderation, utility, and entertainment capabilities*

[Features](#features) • [Installation](#installation) • [Configuration](#configuration) • [Commands](#commands) • [Support](#support)

---

</div>

## ⚠️ Disclaimer
> **Warning**: Self-bots are against Discord's Terms of Service. Use at your own risk. The developers are not responsible for any consequences.

## ✨ Features

<details>
<summary>Click to expand feature list</summary>

### 🎮 Core Features
- **🤖 Advanced Selfbot System**
  - Customizable prefix
  - Dynamic configuration
  - Real-time status updates
  
- **⚡ Performance**
  - Lightning-fast response time
  - Efficient resource usage
  - Stable connection handling

- **🛡️ Security**
  - Authorization system
  - Secure token handling
  - Protected commands

### 🔥 Key Highlights
- **Nitro Sniper**
  - Auto-detection system
  - Fast claiming mechanism
  - Success rate tracking
  
- **Auto Responder**
  - Custom triggers
  - Dynamic responses
  - JSON-based storage

- **Message Management**
  - Bulk operations
  - Smart filtering
  - Archive functionality

</details>

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Discord account token

### One-Click Setup
```bash
git clone https://github.com/RaiyanRafid/RaiyanSelfbot.git
cd RaiyanSelfbot
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Config File Setup
Create `config.yml` in the root directory:
```yaml
bot:
  prefix: "."          # Your command prefix
  developer: "Raiyan"  # Developer name
  website: "raiyanhossain.net"
```

### 2. Token Configuration
Update `config.py`:
```python
class BotConfig:
    TOKEN = 'your_token_here'    # Your Discord token
    USER_ID = your_user_id_here  # Your Discord user ID
```

## 🎮 Commands

<details>
<summary>🛠️ General Commands</summary>

### Auto Responder
| Command | Description | Usage |
|---------|-------------|-------|
| `/addar` | Add auto response | `/addar <trigger> <response>` |
| `/removear` | Remove auto response | `/removear <trigger>` |
| `/listar` | List all responses | `/listar` |

### Message Management
| Command | Description | Usage |
|---------|-------------|-------|
| `/spam` | Repeat messages | `/spam <count> <message>` |
| `/asci` | Create ASCII art | `/asci <text>` |
| `/clear` | Delete messages | `/clear <amount>` |

</details>

<details>
<summary>⚡ Admin Commands</summary>

### Moderation
| Command | Description | Usage |
|---------|-------------|-------|
| `/kick` | Kick user | `/kick @user [reason]` |
| `/ban` | Ban user | `/ban @user [reason]` |
| `/unban` | Unban user | `/unban <user_id>` |

</details>

<details>
<summary>💣 Nuke Commands</summary>

### Server Management
| Command | Description | Usage |
|---------|-------------|-------|
| `/massban` | Ban multiple users | `/massban <user_ids>` |
| `/nukechannels` | Delete channels | `/nukechannels` |
| `/massdm` | Mass DM users | `/massdm <message>` |

</details>

## 🔧 Advanced Configuration

### Permissions System
```python
AUTHORIZED_USERS = [
    your_user_id,  # Main user
    trusted_user_id  # Trusted user
]
```

### Auto Responder Setup
```json
{
    "trigger": "response",
    "hello": "world",
    "custom": "reply"
}
```

## 🌟 Features In-Depth

### Nitro Sniper
- **Detection System**: Monitors messages for Nitro gifts
- **Smart Claiming**: Automated claiming with delay tracking
- **Analytics**: Success rate and performance metrics

### Message Management
- **Bulk Actions**: Handle multiple messages efficiently
- **Smart Filtering**: Advanced message filtering options
- **Data Export**: Save chat history and important info

### User Tools
- **Information Gathering**: Detailed user analytics
- **Avatar Management**: Easy avatar operations
- **Status Control**: Dynamic status updates

## 📚 Documentation

For detailed documentation, visit our [Wiki](https://raiyanhossain.net/docs).

### Quick Links
- [Command List](https://raiyanhossain.net/commands)
- [Setup Guide](https://raiyanhossain.net/setup)
- [FAQ](https://raiyanhossain.net/faq)

## 🛡️ Security Best Practices

- Never share your token
- Use strong passwords
- Enable 2FA on Discord
- Regular security audits
- Keep backups of data

## 🆘 Support

<div align="center">

[![Website](https://img.shields.io/badge/Website-raiyanhossain.net-blue)](https://raiyanhossain.net)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289DA)](https://discord.gg/yourserver)
[![Email](https://img.shields.io/badge/Email-contact%40raiyanhossain.net-red)](mailto:contact@raiyanhossain.net)

</div>

### Common Issues
1. **Token Invalid**: Refresh your Discord token
2. **Permission Errors**: Check role hierarchy
3. **Rate Limits**: Implement delays between actions
4. **Connection Issues**: Check internet stability

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=RaiyanRafid/RaiyanSelfbot&type=Date)](https://star-history.com/#RaiyanRafid/RaiyanSelfbot&Date)

---

<div align="center">

Made with ❤️ by [Raiyan](https://raiyanhossain.net)

<a href="https://raiyanhossain.net">
  <img src="https://img.raiyanhossain.net/img/footer.png" alt="Footer" width="100%"/>
</a>

</div> 