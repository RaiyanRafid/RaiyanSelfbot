import config
import discord
from discord.ext import commands
import json
import asyncio 
from pyfiglet import Figlet
from faker import Faker
from discord import Member
from asyncio import sleep 
import re
import requests
import random
import psutil
import platform
import colorama
from colorama import Fore, Style
import art 
import aiohttp
import datetime
from datetime import timezone
import time
from config import BotConfig, HelpConfig, DisplayConfig, TimingConfig
import yaml

colorama.init()

intents = discord.Intents.default()
intents.voice_states = True

auto_messages = {}


def load_autoresponder_data():
    try:
        with open('autoresponder_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_autoresponder_data(data):
    with open('autoresponder_data.json', 'w') as file:
        json.dump(data, file)

infared = BotConfig.USER_ID
AUTHORIZED_USERS = [infared]  

def load_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

# Load config at startup
config = load_config()

# Initialize bot with config values
bot = commands.Bot(
    command_prefix=config['bot']['prefix'],
    self_bot=True,  # Ensure selfbot mode is enabled
    help_command=None,
    intents=intents
)

fake = Faker()

def is_authorized(ctx):
    return ctx.author.id in AUTHORIZED_USERS



@bot.event
async def on_command_completion(ctx):
    await ctx.message.delete()

@bot.command()
@commands.check(is_authorized)
async def addar(ctx, trigger, *, response):
    autoresponder_data = load_autoresponder_data()
    autoresponder_data[trigger] = response
    save_autoresponder_data(autoresponder_data)
    await ctx.send(f'Autoresponder added: `{trigger}` -> `{response}`')

@bot.command()
@commands.check(is_authorized)
async def removear(ctx, trigger):
    autoresponder_data = load_autoresponder_data()
    if trigger in autoresponder_data:
        del autoresponder_data[trigger]
        save_autoresponder_data(autoresponder_data)
        await ctx.send(f'Autoresponder removed: `{trigger}`')
    else:
        await ctx.send('Autoresponder not found.')

@bot.command()
@commands.check(is_authorized)
async def listar(ctx):
    autoresponder_data = load_autoresponder_data()
    if autoresponder_data:
        response = 'Autoresponders:\n'
        for trigger, response_text in autoresponder_data.items():
            response += f'`{trigger}` -> `{response_text}`\n'
        await ctx.send(response)
    else:
        await ctx.send('No autoresponders found.')


@bot.command()
@commands.check(is_authorized)
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)


@bot.command(aliases=['mode'])
@commands.check(is_authorized)
async def status(ctx, activity_type, *, text):
    activity = None
    if activity_type == 'playing':
        activity = discord.Game(name=text)
    elif activity_type == 'streaming':
        activity = discord.Streaming(name=text, url='https://www.twitch.tv/empireproximus')
    elif activity_type == 'listening':
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)
    elif activity_type == 'watching':
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)

    if activity:
        await bot.change_presence(activity=activity)
        await ctx.send(f'Status updated: {activity_type} {text}')
    else:
        await ctx.send('Invalid activity type. Available types: playing, streaming, listening, watching')


def get_command_category(command):
    """Get the category for a command based on its cog or properties"""
    if hasattr(command, 'hidden') and command.hidden:
        return None if not HelpConfig.Display.SHOW_HIDDEN else HelpConfig.Categories.MISC
    
    cog_name = command.cog_name if command.cog_name else "No Category"
    
    # Map cog names to categories
    category_mapping = {
        "Info": HelpConfig.Categories.INFORMATION,
        "Utility": HelpConfig.Categories.UTILITY,
        "Mod": HelpConfig.Categories.MODERATION,
        "Fun": HelpConfig.Categories.FUN,
        "Adult": HelpConfig.Categories.NSFW,
        "No Category": HelpConfig.Categories.GENERAL
    }
    
    return category_mapping.get(cog_name, HelpConfig.Categories.MISC)

@bot.command(aliases=['h', 'commands', 'cmds'])
@commands.check(is_authorized)
async def help(ctx, command_name: str = None):
    """
    Advanced help command with categories and detailed information
    """
    if command_name:
        # Detailed help for specific command
        command = bot.get_command(command_name)
        if not command:
            await ctx.send(f"```❌ Command '{command_name}' not found```", delete_after=TimingConfig.DELETE_TIMEOUT)
            return

        help_text = (
            "```\n"
            "╔═════════════════ COMMAND INFO ════════════════╗\n"
            "║                                               ║\n"
            f"║  📌 Command: {command.name:<35} ║\n"
            f"║  📝 Description: {command.help or 'No description':<31} ║\n"
        )

        if hasattr(command, 'usage'):
            usage = command.usage if command.usage else f"{BotConfig.PREFIX}{command.name}"
            help_text += f"║  💡 Usage: {usage:<37} ║\n"

        if command.aliases:
            aliases = ", ".join(command.aliases)
            help_text += f"║  🔄 Aliases: {aliases:<35} ║\n"

        help_text += (
            "║                                               ║\n"
            "╚═══════════════════════════════════════════════╝\n"
            "```"
        )
        await ctx.send(help_text, delete_after=TimingConfig.RESPONSE_TIMEOUT)
        return

    # Main help menu
    main_help = (
        "```\n"
        "╔═════════════ RAIYAN SELFBOT ═══════════╗\n"
        "║               COMMAND LIST              ║\n"
        "╠════════════════════════════════════════╣\n"
    )

    # General Commands Section
    general_cmds = (
        "║  🛠️ GENERAL COMMANDS                     ║\n"
        "║  • addar, removear, listar              ║\n"
        "║  • spam, asci, clear, scrap             ║\n"
        "║  • userinfo, avatar, hack               ║\n"
        "║  • ping, status, selfbot                ║\n"
        "║                                         ║\n"
    )

    # Admin Commands Section
    admin_cmds = (
        "║  ⚡ ADMIN COMMANDS                       ║\n"
        "║  • kick, ban, unban, softban            ║\n"
        "║  • mute, forcenick, stopforcenick       ║\n"
        "║  • nuke, savebans, exportbans           ║\n"
        "║                                         ║\n"
    )

    # Info Commands Section
    info_cmds = (
        "║  ℹ️ INFO COMMANDS                       ║\n"
        "║  • tokeninfo, iplook, id                ║\n"
        "║  • calculation, nickscan                ║\n"
        "║                                         ║\n"
    )

    # Nuke Commands Section
    nuke_cmds = (
        "║  💣 NUKE COMMANDS                       ║\n"
        "║  • randomban, massban, massunban        ║\n"
        "║  • massdm, nukechannels                 ║\n"
        "║  • servername, servericon               ║\n"
        "║                                         ║\n"
    )

    # Extra Commands Section
    extra_cmds = (
        "║  🎮 EXTRA COMMANDS                      ║\n"
        "║  • fakenitro, give, link               ║\n"
        "║  • pay, bkash, nagad                   ║\n"
        "║                                         ║\n"
    )

    # Adult Commands Section
    adult_cmds = (
        "║  🔞 ADULT COMMANDS                      ║\n"
        "║  • hrandom, hass, ass, boobs           ║\n"
        "║  • pussy, 4k, cumm, hblowjob           ║\n"
        "║  • ahegao, lewd, feet, lesbian         ║\n"
        "║  • spank, hwallpaper, midriff          ║\n"
        "║  • hentai, holo, hneko, neko           ║\n"
        "║                                         ║\n"
    )

    # Help Commands Section
    help_cmds = (
        "║  📚 HELP COMMANDS                       ║\n"
        "║  • help, generalhelp, adminhelp         ║\n"
        "║  • infohelp, nukehelp, adulthelp       ║\n"
        "║  • allcmds                             ║\n"
        "║                                         ║\n"
    )

    # Footer Section
    footer = (
        "╠════════════════ INFO ═══════════════════╣\n"
        f"║  PREFIX: {BotConfig.PREFIX:<35} ║\n"
        "║  DEV  : Raiyan                          ║\n"
        "║  WEB  : raiyanhossain.net              ║\n"
        "╚════════════════════════════════════════╝\n"
        "```"
    )

    # Combine all sections
    full_help = main_help + general_cmds + admin_cmds + info_cmds + nuke_cmds + extra_cmds + adult_cmds + help_cmds + footer
    
    try:
        await ctx.send(full_help, delete_after=TimingConfig.RESPONSE_TIMEOUT)
        
        # Send additional information
        additional_info = (
            "**📌 Quick Links**\n"
            "• [Website](https://raiyanhossain.net)\n\n"
            "**⚠️ Important Notes**\n"
            "• Use commands responsibly\n"
            "• Some commands require special permissions\n"
            "• For detailed command info use: `.help <command>`"
        )
        await ctx.send(additional_info, delete_after=TimingConfig.RESPONSE_TIMEOUT)
    except discord.HTTPException as e:
        await ctx.send(f"```❌ Error displaying help menu: {str(e)}```", delete_after=TimingConfig.DELETE_TIMEOUT)


@bot.command()
@commands.check(is_authorized)
async def asci(ctx, *, text):
    f = Figlet(font='standard')
    ascii_art = art.text2art(text)
    await ctx.send(f'```{ascii_art}```')


@bot.command(aliases=['ui', 'whois'])
@commands.check(is_authorized)
async def userinfo(ctx, member: discord.Member):


    user_info = [
        f"• Username: {member.name}",
        f"• Discriminator: {member.discriminator}",
        f"• ID: {member.id}",
        f"• Nickname: {member.nick}",
        f"• Status: {member.status}",
        f"• Joined Discord: <t:{int(member.created_at.timestamp())}:d>",
        f"• Joined Server: <t:{int(member.joined_at.timestamp())}:d>"
    ]

    response = '\n'.join(user_info)
    await ctx.send(f"User Info:\n{response}")


@bot.command()
@commands.check(is_authorized)
async def hack(ctx, member: discord.Member):


    hacking_messages = [
        "Infecting into the mainframe...",
        "Caching data...",
        "Decrypting security protocols...",
        "Extracting personal information...",
        "Compiling user profile...",
        "Infection complete!"
    ]

    progress_message = await ctx.send("Hacking user...")  

    for message in hacking_messages:
        await sleep(2)  
        await progress_message.edit(content=message)

    height_cm = fake.random_int(min=150, max=200)
    height_feet = height_cm // 30.48  
    height_inches = (height_cm % 30.48) // 2.54  

    response = f"Successfully hacked {member.mention}! Here's the hacked information:\n\n" \
               f"Name: {fake.name()}\n" \
               f"Gender: {fake.random_element(['Male', 'Female'])}\n" \
               f"Age: {fake.random_int(min=18, max=99)}\n" \
               f"Height: {height_feet} feet {height_inches} inches\n" \
               f"Weight: {fake.random_int(min=50, max=100)} kg\n" \
               f"Hair Color: {fake.random_element(['Black', 'Brown', 'Blonde', 'Red'])}\n" \
               f"Skin Color: {fake.random_element(['Fair', 'Medium', 'Dark'])}\n" \
               f"DOB: {fake.date_of_birth(minimum_age=18, maximum_age=99).strftime('%Y-%m-%d')}\n" \
               f"Location: {fake.city()}, {fake.country()}\n" \
               f"Phone: {fake.phone_number()}\n" \
               f"E-Mail: {fake.email()}\n" \
               f"Passwords: {fake.password(length=10)}\n" \
               f"Occupation: {fake.job()}\n" \
               f"Annual Salary: ${fake.random_int(min=30000, max=100000)}\n" \
               f"Ethnicity: {fake.random_element(['Caucasian', 'African-American', 'Asian', 'Hispanic', 'Other'])}\n" \
               f"Religion: {fake.random_element(['Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Other'])}\n" \
               f"Sexuality: {fake.random_element(['Straight', 'Gay', 'Lesbian', 'Bisexual'])}\n" \
               f"Education: {fake.random_element(['High School', 'Bachelor', 'Master', 'PhD'])}"

    await progress_message.edit(content=response)


@bot.command(aliases=['av','ava'])
@commands.check(is_authorized)
async def avatar(ctx, member: Member):
    avatar_url = member.avatar_url_as(format="png")
    await ctx.send(f"Avatar of {member.mention}: {avatar_url}")


@bot.command()
@commands.check(is_authorized)
async def ping(ctx):
    
    latency = round(bot.latency * 1000)  

    
    await ctx.send(f'**~ {latency}ms**')


@bot.command(aliases=['247'])
@commands.check(is_authorized)
async def connectvc(ctx, channel_id):
    try:
        channel = bot.get_channel(int(channel_id))

        if channel is None:
            return await ctx.send("Invalid channel ID. Please provide a valid voice channel ID.")

        if isinstance(channel, discord.VoiceChannel):
            permissions = channel.permissions_for(ctx.guild.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send("I don't have permissions to connect or speak in that channel.")

            voice_channel = await channel.connect()
            await ctx.send(f"Connected to voice channel: {channel.name}")

            await channel.send("Hello, I have connected to this voice channel!")

        else:
            await ctx.send("This is not a voice channel. Please provide a valid voice channel ID.")
    except discord.errors.ClientException:
        await ctx.send("I'm already connected to a voice channel.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to perform this action.")
    except ValueError:
        await ctx.send("Invalid channel ID. Please provide a valid voice channel ID.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



@bot.command(aliases=['purge'])
@commands.check(is_authorized)
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    
    messages = await channel.history(limit=times + 1).flatten()

    
    bot_messages = filter(is_bot_message, messages)

    
    for message in bot_messages:
        await asyncio.sleep(0.75)  
        await message.delete()

    await ctx.send(f"Deleted {times} messages.")



@bot.command(aliases=['info', 'stats'])
@commands.check(is_authorized)
async def selfbot(ctx):
    version = "Raiyan Bot"
    language = "Unknown"
    author = "! Raiyan"
    total_commands = len(bot.commands)
    github_link = "https://github.com/RaiyanRafid"

    
    ram_info = psutil.virtual_memory()
    total_ram = round(ram_info.total / (1024 ** 3), 2)  
    used_ram = round(ram_info.used / (1024 ** 3), 2)  

    
    os_info = platform.platform()

    message = f"**__RAIYAN BOT__**\n\n" \
              f"**• Vers: {version}\n" \
              f"• Lang: {language}\n" \
              f"• Created By: {author}\n" \
              f"• Total Cmds: {total_commands}\n" \
              f"• Total RAM: {total_ram} GB\n" \
              f"• Used RAM: {used_ram} GB\n" \
              f"• Operating System: {os_info}\n\n" \
              f"• GitHub: {github_link} **"

    await ctx.send(message)






@bot.command(aliases=['nitro'])
@commands.check(is_authorized)
async def fakenitro(ctx):
    
    nitro_months = random.randint(1, 12)

    
    fake_link = f"discord.gift/F4K3N1TR0-{nitro_months}M"

    
    await ctx.send(f"\n{fake_link}")


@bot.command(aliases=['scan'])
@commands.check(is_authorized)
async def nickscan(ctx):
    
    for guild in bot.guilds:
        member = guild.get_member(bot.user.id)
        
        
        if member is not None and member.nick is not None:
            await ctx.send(f"Server: {guild.name}\nNickname: {member.nick}\n")


@bot.command()
@commands.check(is_authorized)
async def scrap(ctx, number: int):
    channel = ctx.channel

    
    if number <= 0 or number > 10000:
        await ctx.send("Please provide a valid number between 1 and 10,000.")
        return

    
    try:
        messages = []
        async for message in channel.history(limit=number):
            messages.append(f"{message.author}: {message.content}")

        
        content = "\n".join(messages)

        
        with open("scraped_messages.txt", "w", encoding="utf-8") as file:
            file.write(content)

        
        await asyncio.sleep(1)  
        with open("scraped_messages.txt", "rb") as file:
            await ctx.send(file=discord.File(file, filename="scraped_messages.txt"))
    except discord.Forbidden:
        await ctx.send("I don't have permission to access the channel.")
    except discord.HTTPException:
        await ctx.send("An error occurred while fetching messages.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
@commands.check(is_authorized)
async def link(ctx):
    response = (
        "```\n"
        "╔═════════════════ SOCIAL LINKS ════════════════╗\n"
        "║                                               ║\n"
        "║  🌐 WEBSITE                                  ║\n"
        "║  • Main Site: raiyanhossain.net               ║\n"
        "║                                               ║\n"
        "║  📱 SOCIAL MEDIA                              ║\n"
        "║  • Facebook: raiyanhossainrafid               ║\n"
        "║  • Instagram: raiyanhossainxyz                ║\n"
        "║  • Twitter: PROXIMITYEMPIRE                   ║\n"
        "║                                               ║\n"
        "╠═════════════════ DIRECT LINKS ════════════════╣\n"
        "║ • Website  : https://raiyanhossain.net        ║\n"
        "║ • Facebook : fb.com/raiyanhossainrafid        ║\n"
        "║ • Instagram: instagram.com/raiyanhossainxyz   ║\n"
        "║ • Twitter  : twitter.com/PROXIMITYEMPIRE      ║\n"
        "╚═══════════════════════════════════════════════╝\n"
        "```\n"
        "**🔗 Quick Access**\n"
        "• [Website](https://raiyanhossain.net)\n"
        "• [Facebook](https://www.facebook.com/raiyanhossainrafid)\n"
        "• [Instagram](https://www.instagram.com/raiyanhossainxyz)\n"
        "• [Twitter](https://twitter.com/PROXIMITYEMPIRE)"
    )
    await ctx.send(response)
  
@bot.command()
@commands.check(is_authorized)
async def pay(ctx):
    response = (
        "```\n"
        "╔═══════════════ PAYMENT METHODS ═══════════════╗\n"
        "║                                               ║\n"
        "║  BKASH                                        ║\n"
        "║  Number: 01869113329                          ║\n"
        "║  Account Type: Personal                       ║\n"
        "║                                               ║\n"
        "║  NAGAD                                        ║\n"
        "║  Number: 01869113329                          ║\n"
        "║  Account Type: Personal                       ║\n"
        "║                                               ║\n"
        "╚════════════════ INSTRUCTIONS ═════════════════╝\n"
        "• Send payment to any of the above numbers\n"
        "• After payment, please provide:\n"
        "  1. Screenshot of payment OR\n"
        "  2. Transaction ID OR\n"
        "  3. Last 4 digits of your phone number\n"
        "• Your order will be processed immediately\n"
        "```"
    )
    await ctx.send(response)
    
@bot.command()
@commands.check(is_authorized)
async def bkash(ctx):
    response = (
        "```\n"
        "╔═══════════════ BKASH PAYMENT ════════════════╗\n"
        "║                                              ║\n"
        "║  💳 Account Details                         ║\n"
        "║  • Number: 01869113329                       ║\n"
        "║  • Type: Personal                            ║\n"
        "║  • Account Name: Raiyan                      ║\n"
        "║                                              ║\n"
        "║  📝 Payment Steps                            ║\n"
        "║  1. Open Bkash App                           ║\n"
        "║  2. Select 'Send Money'                      ║\n"
        "║  3. Enter: 01869113329                       ║\n"
        "║  4. Enter Amount                             ║\n"
        "║  5. Add Reference                            ║\n"
        "║                                              ║\n"
        "╚══════════════════════════════════════════════╝\n"
        "```\n"
        "**🔍 QR Code Payment**\n"
        "Scan this QR code to pay faster: [Click here](https://img.raiyanhossain.net/img/bkash.png.jpg)\n\n"
        "**⚠️ Important**\n"
        "• After payment, send screenshot or TrxID\n"
        "• Keep payment proof until order is completed\n"
        "• For issues, contact support immediately"
    )
    await ctx.send(response)
    
@bot.command()
@commands.check(is_authorized)
async def nagad(ctx):
    response = (
        "```\n"
        "╔═══════════════ NAGAD PAYMENT ════════════════╗\n"
        "║                                              ║\n"
        "║  💳 Account Details                          ║\n"
        "║  • Number: 01869113329                       ║\n"
        "║  • Type: Personal                            ║\n"
        "║  • Account Name: Raiyan                      ║\n"
        "║                                              ║\n"
        "║  📝 Payment Steps                            ║\n"
        "║  1. Open Nagad App                           ║\n"
        "║  2. Select 'Send Money'                      ║\n"
        "║  3. Enter: 01869113329                       ║\n"
        "║  4. Enter Amount                             ║\n"
        "║  5. Add Reference                            ║\n"
        "║                                              ║\n"
        "╚══════════════════════════════════════════════╝\n"
        "```\n"
        "**🔍 QR Code Payment**\n"
        "Scan this QR code to pay faster: [Click here](https://img.raiyanhossain.net/img/payqr.png)\n\n"
        "**⚠️ Important**\n"
        "• After payment, send screenshot or TrxID\n"
        "• Keep payment proof until order is completed\n"
        "• For issues, contact support immediately"
    )
    await ctx.send(response)
        

@bot.command(aliases=['generalh'])
@commands.check(is_authorized)
async def generalhelp(ctx):
    main_help = (
        "```\n"
        "╔═════════════ GENERAL COMMANDS ════════════╗\n"
        "║                                           ║\n"
        "║  🤖 AUTO RESPONDER                        ║\n"
        "║  • addar    : Add response               ║\n"
        "║  • removear : Remove response            ║\n"
        "║  • listar   : List responses            ║\n"
        "║                                           ║\n"
        "║  💬 MESSAGES                              ║\n"
        "║  • spam   : Repeat messages              ║\n"
        "║  • asci   : ASCII art                    ║\n"
        "║  • clear  : Delete messages              ║\n"
        "║  • scrap  : Save messages                ║\n"
        "║                                           ║\n"
        "║  👤 USER                                  ║\n"
        "║  • userinfo : User details               ║\n"
        "║  • avatar   : Show avatar                ║\n"
        "║  • hack     : Simulate hack              ║\n"
        "║  • nickscan : Check nicks                ║\n"
        "║                                           ║\n"
        "║  ⚙️ UTILITY                               ║\n"
        "║  • calc      : Calculator                ║\n"
        "║  • status    : Change status             ║\n"
        "║  • ping      : Check latency             ║\n"
        "║  • selfbot   : Bot info                  ║\n"
        "║  • connectvc : Join voice                ║\n"
        "║                                           ║\n"
        "║  🎁 EXTRAS                                ║\n"
        "║  • fakenitro : Generate nitro            ║\n"
        "║  • give      : Send gift                 ║\n"
        "║  • link      : Show links                ║\n"
        "║  • pay       : Payment info              ║\n"
        "║                                           ║\n"
        "╠═════════════ EXAMPLES ════════════════════╣\n"
        "║ • spam <count> <message>                   ║\n"
        "║ • asci <text>                              ║\n"
        "║ • userinfo @user                           ║\n"
        "╚═══════════════════════════════════════════╝\n"
        "```\n"
        "**💡 Tips**\n"
        "• Default Prefix: `.`\n"
        "• Some commands have cooldowns\n"
        "• Use responsibly"
    )
    await ctx.send(main_help)
    
@bot.command(aliases=['nukeh'])
@commands.check(is_authorized)
async def nukehelp(ctx):
    main_help = (
        "```\n"
        "╔═════════════════ NUKE COMMANDS ═══════════════╗\n"
        "║                                               ║\n"
        "║  💥 MASS ACTIONS                              ║\n"
        "║  • randomban   : Mass random bans             ║\n"
        "║  • massban     : Ban multiple users           ║\n"
        "║  • massunban   : Unban multiple users         ║\n"
        "║  • massdm      : DM all members               ║\n"
        "║                                               ║\n"
        "║  🏗️ SERVER MANAGEMENT                         ║\n"
        "║  • nukechannels : Delete all channels         ║\n"
        "║  • servername   : Change server name          ║\n"
        "║  • servericon   : Change server icon          ║\n"
        "║                                               ║\n"
        "╠════════════════ PARAMETERS ═══════════════════╣\n"
        "║ • randomban <count>                           ║\n"
        "║ • massban <user_ids> [reason] [delay]         ║\n"
        "║ • massdm <message>                            ║\n"
        "║ • servername <new_name>                       ║\n"
        "╠═════════════════ CAUTION ════════════════════╣\n"
        "║ ⚠️ These commands can cause irreversible       ║\n"
        "║    damage to the server. Use with extreme     ║\n"
        "║    caution and responsibility.                ║\n"
        "╚═══════════════════════════════════════════════╝\n"
        "```\n"
        "**⚠️ Requirements**\n"
        "• Administrator permissions\n"
        "• Server management access\n"
        "• High role hierarchy\n\n"
        "**⚡ Important Notes**\n"
        "• Commands are irreversible\n"
        "• Actions are logged\n"
        "• Use at your own risk\n\n"
        "**🛡️ Safety**\n"
        "• Double-check target servers\n"
        "• Verify permissions before use\n"
        "• Keep backup of important data"
    )
    await ctx.send(main_help)
    
@bot.command(aliases=['infoh'])
@commands.check(is_authorized)
async def infohelp(ctx):
    main_help = (
        "```\n"
        "╔════════════════ INFO COMMANDS ════════════════╗\n"
        "║                                               ║\n"
        "║  🔍 TOKEN INFO                                ║\n"
        "║  • tokeninfo : Get token details              ║\n"
        "║    - Username and ID                          ║\n"
        "║    - Email and creation date                  ║\n"
        "║    - Account details                          ║\n"
        "║                                               ║\n"
        "║  🌐 NETWORK INFO                              ║\n"
        "║  • iplook : IP address lookup                ║\n"
        "║    - Country and city                        ║\n"
        "║    - ISP details                             ║\n"
        "║    - Current timezone                         ║\n"
        "║                                               ║\n"
        "║  📋 DISCORD INFO                              ║\n"
        "║  • id : Get IDs                              ║\n"
        "║    - User IDs                                ║\n"
        "║    - Server IDs                              ║\n"
        "║    - Channel/Role IDs                         ║\n"
        "║                                               ║\n"
        "║  🔢 UTILITIES                                 ║\n"
        "║  • calculation : Math operations              ║\n"
        "║    - Basic calculations                       ║\n"
        "║    - Complex formulas                         ║\n"
        "║                                               ║\n"
        "╠═════════════════ USAGE ══════════════════════╣\n"
        "║ • tokeninfo <token>                          ║\n"
        "║ • iplook <ip_address>                        ║\n"
        "║ • id <@user/server/channel/role>             ║\n"
        "╚═══════════════════════════════════════════════╝\n"
        "```\n"
        "**⚠️ Security Notice**\n"
        "• Never share token information\n"
        "• Keep IP lookups private\n"
        "• Respect user privacy\n\n"
        "**💡 Tips**\n"
        "• Use commands responsibly\n"
        "• Double-check IDs before use\n"
        "• Store sensitive info securely"
    )
    await ctx.send(main_help)

@bot.command(aliases=['hentaihelhelp'])
@commands.check(is_authorized)
async def adulthelp(ctx):
    # First message: Hentai commands
    hentai_help = (
        "```\n"
        "╔═════════════════ NSFW COMMANDS ════════════════╗\n"
        "║                                                ║\n"
        "║  🔞 HENTAI COMMANDS                            ║\n"
        "║  • hentai     : Random hentai                  ║\n"
        "║  • hrandom    : Random hentai boobs            ║\n"
        "║  • hass       : Hentai ass                     ║\n"
        "║  • hblowjob   : Hentai explicit               ║\n"
        "║  • ahegao     : Ahegao content                ║\n"
        "║  • hneko      : Hentai neko                   ║\n"
        "║  • hthigh     : Hentai thigh images           ║\n"
        "║  • midriff    : Hentai midriff                ║\n"
        "║  • paizuri    : Paizuri content               ║\n"
        "║  • hwallpaper : Anime wallpaper               ║\n"
        "╚════════════════════════════════════════════════╝\n"
        "```"
    )
    await ctx.send(hentai_help)

    # Second message: Real content
    real_help = (
        "```\n"
        "╔═════════════════ NSFW COMMANDS ════════════════╗\n"
        "║                                                ║\n"
        "║  📸 REAL CONTENT                               ║\n"
        "║  • ass        : Real ass                       ║\n"
        "║  • boobs      : Real breasts                   ║\n"
        "║  • pussy      : Real explicit                  ║\n"
        "║  • anal       : Anal content                   ║\n"
        "║  • feet       : Feet content                   ║\n"
        "║  • lesbian    : Girl content                   ║\n"
        "║  • gonewild   : Gone wild images              ║\n"
        "║  • thigh      : Thigh images                   ║\n"
        "║  • cumm       : Explicit content               ║\n"
        "╚════════════════════════════════════════════════╝\n"
        "```"
    )
    await ctx.send(real_help)

    # Third message: SFW and Quality content
    sfw_help = (
        "```\n"
        "╔═════════════════ NSFW COMMANDS ════════════════╗\n"
        "║                                                ║\n"
        "║  🎭 ANIME & SFW                                ║\n"
        "║  • neko       : Neko images                    ║\n"
        "║  • holo       : Holo images                    ║\n"
        "║  • kitsune    : Kitsune content                ║\n"
        "║  • kemono     : Kemonomimi images              ║\n"
        "║  • lewd       : Lewd content                   ║\n"
        "║  • gah        : Gah images                     ║\n"
        "║  • coffee     : Coffee images                  ║\n"
        "║  • food       : Food images                    ║\n"
        "║                                                ║\n"
        "║  🌟 QUALITY                                    ║\n"
        "║  • 4k         : 4K quality content             ║\n"
        "║  • spank      : Special content                ║\n"
        "╚════════════════════════════════════════════════╝\n"
        "```"
    )
    await ctx.send(sfw_help)

    # Fourth message: Important notices
    notice_help = (
        "**⚠️ Important Information**\n"
        "```\n"
        "╔════════════════ IMPORTANT ════════════════════╗\n"
        "║ • Use in NSFW channels only                    ║\n"
        "║ • Must be 18+ to use these commands           ║\n"
        "║ • Some content may be explicit                 ║\n"
        "╚════════════════════════════════════════════════╝\n"
        "```\n"
        "**🔒 Privacy & Safety**\n"
        "• Commands are logged for safety\n"
        "• Respect server rules and guidelines\n"
        "• Report inappropriate content"
    )
    await ctx.send(notice_help)

@bot.command(aliases=['adminh'])
@commands.check(is_authorized)
async def adminhelp(ctx):
    main_help = (
        "```\n"
        "╔════════════════ ADMIN COMMANDS ═══════════════╗\n"
        "║                                               ║\n"
        "║  🛡️ MODERATION                                ║\n"
        "║  • kick    : Kick a user                     ║\n"
        "║  • ban     : Ban a user                      ║\n"
        "║  • unban   : Unban a user                    ║\n"
        "║  • softban : Ban + instant unban             ║\n"
        "║  • mute    : Timeout a user                  ║\n"
        "║                                               ║\n"
        "║  👤 USER MANAGEMENT                           ║\n"
        "║  • forcenick     : Force nickname            ║\n"
        "║  • stopforcenick : Stop forcing nick         ║\n"
        "║                                               ║\n"
        "║  ⚙️ SERVER TOOLS                              ║\n"
        "║  • nuke      : Recreate channel              ║\n"
        "║  • savebans  : Save ban list                 ║\n"
        "║  • exportbans: Import bans                   ║\n"
        "║                                               ║\n"
        "╠═══════════════ USAGE EXAMPLES ═══════════════╣\n"
        "║ • kick @user [reason]                         ║\n"
        "║ • ban @user [reason]                          ║\n"
        "║ • mute @user [duration]                       ║\n"
        "╚═══════════════════════════════════════════════╝\n"
        "```\n"
        "**⚠️ Requirements**\n"
        "• Administrator or relevant mod permissions\n"
        "• Server member management access\n"
        "• Proper role hierarchy\n\n"
        "**💡 Tips**\n"
        "• Always provide a reason for moderation actions\n"
        "• Check role hierarchy before using commands\n"
        "• Keep logs of important actions"
    )
    await ctx.send(main_help)

@bot.command(aliases=['allcommands','allcmd'])
@commands.check(is_authorized)
async def allcmds(ctx):
    # Reload config to get latest values
    config = load_config()
    main_menu = (
        "```\n"
        "╔═════════════ RAIYAN SELFBOT ═══════════╗\n"
        "║               COMMAND HELP             ║\n"
        "╠════════════════════════════════════════╣\n"
        "║  🛠️ AVAILABLE CATEGORIES:              ║\n"
        "║                                        ║\n"
        f"║  1️⃣ GENERAL  : {config['bot']['prefix']}generalhelp            ║\n"
        f"║  2️⃣ ADMIN    : {config['bot']['prefix']}adminhelp              ║\n"
        f"║  3️⃣ INFO     : {config['bot']['prefix']}infohelp               ║\n"
        f"║  4️⃣ NUKE     : {config['bot']['prefix']}nukehelp               ║\n"
        f"║  5️⃣ ADULT    : {config['bot']['prefix']}adulthelp              ║\n"
        "║                                        ║\n"
        "╠════════════════════════════════════════╣\n"
        f"║  PREFIX: {config['bot']['prefix']}                             ║\n"
        f"║  DEV  : {config['bot']['developer']}                         ║\n"
        f"║  WEB  : {config['bot']['website']}              ║\n"
        "╚════════════════════════════════════════╝\n"
        "```"
    )
    await ctx.send(main_menu)

    details = (
        "**📌 Quick Links**\n"
        "• [🌐 Website](https://raiyanhossain.net)\n\n"
        "**⚠️ Important**\n"
        "• Some commands need special permissions\n"
        "• Keep your token secure\n"
        "• Report bugs to support"
    )
    await ctx.send(details)
    
@bot.command()
@commands.check(is_authorized)
async def give(ctx, member: discord.Member , *,link: str):
    await member.send(f"Here is your gift: [click to claim]({link})")
    await ctx.send(f"Gift sent to {member.mention}.")

    
    

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    # Check for Nitro links with improved pattern matching
    nitro_pattern = re.compile(r"(discord\.gift\/|discordapp\.com\/gifts\/|discord\.com\/gifts\/)([a-zA-Z0-9]+)")
    matches = nitro_pattern.finditer(message.content)

    for match in matches:
        code = match.group(2)
        
        # Print sniper info with timestamp
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.YELLOW}[SNIPER] [{current_time}] Nitro Gift Found in {message.guild.name if message.guild else 'DM'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[SNIPER] Code: {code}{Style.RESET_ALL}")

        headers = {
            'Authorization': BotConfig.TOKEN,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5)  # 5 second timeout
                ) as response:
                    end_time = time.time()
                    delay = round((end_time - start_time) * 1000)  # Calculate delay in ms
                    
                    data = await response.json()
                    
                    if response.status == 200:
                        print(f"{Fore.GREEN}[SUCCESS] Nitro claimed in {delay}ms!{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[INFO] Type: {data.get('subscription_plan', 'Unknown')}{Style.RESET_ALL}")
                        
                        # Send success message in both console and Discord
                        success_msg = f"🎉 Successfully claimed Nitro gift! `{code}` ({delay}ms)"
                        if isinstance(message.channel, discord.TextChannel):
                            await message.channel.send(success_msg)
                    
                    elif response.status == 429:  # Rate limit
                        retry_after = data.get('retry_after', 0)
                        print(f"{Fore.RED}[ERROR] Rate limited. Retry after {retry_after}s{Style.RESET_ALL}")
                    
                    else:
                        error_message = data.get('message', 'Unknown error')
                        print(f"{Fore.RED}[ERROR] Failed to claim: {error_message} ({delay}ms){Style.RESET_ALL}")
        
        except asyncio.TimeoutError:
            print(f"{Fore.RED}[ERROR] Request timed out after 5s{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")

    # Process other bot commands
    await bot.process_commands(message)

@bot.event
async def on_ready():
    config = load_config()  # Get latest config values
    startup_message = f"""
{Fore.CYAN}╔════════════════ RAIYAN SELFBOT ═══════════════╗{Style.RESET_ALL}
{Fore.CYAN}║                                               ║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}• Status    : Connected{Style.RESET_ALL}                      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}• Account   : {bot.user.name}{Style.RESET_ALL}                      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}• Developer : {config['bot']['developer']}{Style.RESET_ALL}                        {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}• Version   : 3.1{Style.RESET_ALL}                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.MAGENTA}• Website   : {config['bot']['website']}{Style.RESET_ALL}            {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.RED}• Prefix    : {config['bot']['prefix']}{Style.RESET_ALL}                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║                                               ║{Style.RESET_ALL}
{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(startup_message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument provided: {error}")
    else:
        raise error

@bot.event
async def on_message(message):
    if message.author != bot.user:
        return
      
    autoresponder_data = load_autoresponder_data()
    content = message.content.lower()
    if content in autoresponder_data:
        response = autoresponder_data[content]
        await message.channel.send(response)

    await bot.process_commands(message)  

infared = BotConfig.TOKEN

if __name__ == "__main__":
    bot.load_extension('admin')
    bot.load_extension('info')
    bot.load_extension('nuke')
    bot.load_extension('adult')
    bot.run(infared, bot=False)