import discord
from discord.ext import commands
import requests
from datetime import datetime
import json
import os
import asyncio

class Hentai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_file = "command_stats.json"
        self.command_usage = self.load_stats()
        self.last_used = {}

    def load_stats(self) -> dict:
        """Load statistics from JSON file"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
                # Convert string timestamps back to datetime objects
                for cmd in stats:
                    if "last_used" in stats[cmd]:
                        try:
                            stats[cmd]["last_used"] = datetime.fromisoformat(stats[cmd]["last_used"])
                        except (ValueError, TypeError):
                            stats[cmd]["last_used"] = None
                return stats
            return {}
        except Exception as e:
            print(f"Error loading stats: {e}")
            return {}

    def save_stats(self):
        """Save statistics to JSON file"""
        try:
            stats_to_save = {}
            for cmd, data in self.command_usage.items():
                stats_to_save[cmd] = {
                    "total": data["total"],
                    "users": data["users"],
                    "last_used": self.last_used[cmd].isoformat() if cmd in self.last_used else None
                }
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats_to_save, f, indent=4)
        except Exception as e:
            print(f"Error saving stats: {e}")

    async def update_stats(self, command_name: str):
        """Update command usage statistics for selfbot"""
        if command_name not in self.command_usage:
            self.command_usage[command_name] = {"total": 0}
        
        self.command_usage[command_name]["total"] += 1
        self.last_used[command_name] = datetime.now()
        
        # Save stats after each update
        self.save_stats()

    async def send_image(self, ctx, api_endpoint: str):
        """Helper method to handle image sending"""
        try:
            # Send the image link in a new message
            async with ctx.channel.typing():
                r = requests.get(f"https://nekobot.xyz/api/image?type={api_endpoint}")
                r.raise_for_status()
                data = r.json()
                try:
                    # Try to delete the command message, but don't raise if it fails
                    await ctx.message.delete()
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    pass
                await ctx.send(data['message'])
        except Exception as e:
            # If error occurs, send error message
            try:
                error_msg = await ctx.send(f"An error occurred: {str(e)}")
                await asyncio.sleep(5)
                await error_msg.delete()
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass

    # HENTAI CATEGORY
    @commands.command(
        name="hrandom",
        aliases=['hboobs', 'hb', 'randhentai'],
        usage=".hrandom",
        description="Random hentai boobs"
    )
    async def hrandom(self, ctx):
        await self.update_stats("hrandom")
        await self.send_image(ctx, "hboobs")

    @commands.command(
        name="hass",
        aliases=['has', 'hbooty', 'hentaiass'],
        usage=".hass",
        description="Random hentai ass"
    )
    async def hass(self, ctx):
        await self.update_stats("hass")
        await self.send_image(ctx, "hass")

    # REAL CONTENT CATEGORY
    @commands.command(
        name="ass",
        aliases=['booty', 'realass', 'rass'],
        usage=".ass",
        description="Random real ass"
    )
    async def ass(self, ctx):
        await self.update_stats("ass")
        await self.send_image(ctx, "ass")

    @commands.command(
        name="boobs",
        aliases=['breasts', 'realboobs', 'rboobs'],
        usage=".boobs",
        description="Real breasts content"
    )
    async def boobs(self, ctx):
        await self.update_stats("boobs")
        await self.send_image(ctx, "boobs")

    # SPECIAL CONTENT CATEGORY
    @commands.command(
        name="4k",
        aliases=['4knsfw', 'hd', 'hdnsfw'],
        usage=".4k",
        description="4K quality NSFW content"
    )
    async def fk(self, ctx):
        await self.update_stats("4k")
        await self.send_image(ctx, "4k")

    @commands.command(
        name="hentai",
        aliases=['hen', 'hent', 'randomh'],
        usage=".hentai",
        description="Random hentai content"
    )
    async def hentai(self, ctx):
        await self.update_stats("hentai")
        await self.send_image(ctx, "hentai")

    # ANIME CATEGORY
    @commands.command(
        name="neko",
        aliases=['catgirl', 'nekomimi'],
        usage=".neko",
        description="Neko girl images"
    )
    async def neko(self, ctx):
        await self.update_stats("neko")
        await self.send_image(ctx, "neko")

    @commands.command(
        name="kitsune",
        aliases=['foxgirl', 'kitsu'],
        usage=".kitsune",
        description="Kitsune girl images"
    )
    async def kitsune(self, ctx):
        await self.update_stats("kitsune")
        await self.send_image(ctx, "hkitsune")

    # STATISTICS COMMAND
    @commands.command(
        name="adultstats",
        aliases=['astat', 'astats', 'nsfw_stats'],
        usage=".adultstats [command_name]",
        description="View NSFW command usage statistics"
    )
    async def command_stats(self, ctx, command_name: str = None):
        if not self.command_usage:
            try:
                await ctx.message.delete()
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass
            msg = await ctx.send("No commands have been used yet!")
            await asyncio.sleep(5)
            try:
                await msg.delete()
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass
            return

        try:
            await ctx.message.delete()
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        if command_name:
            if command_name in self.command_usage:
                stats = self.command_usage[command_name]
                last_used = self.last_used.get(command_name, "Never")
                if isinstance(last_used, datetime):
                    last_used = last_used.strftime("%Y-%m-%d %H:%M:%S")
                
                response = (
                    "```\n"
                    f"Statistics for {command_name}:\n"
                    f"Total uses: {stats['total']}\n"
                    f"Last used: {last_used}\n"
                    "```"
                )
            else:
                response = f"No statistics available for command: {command_name}"
        else:
            response = "```\nCommand Usage Statistics:\n\n"
            sorted_commands = sorted(
                self.command_usage.items(),
                key=lambda x: x[1]['total'],
                reverse=True
            )
            for cmd, stats in sorted_commands:
                last_used = self.last_used.get(cmd, "Never")
                if isinstance(last_used, datetime):
                    last_used = last_used.strftime("%Y-%m-%d %H:%M:%S")
                response += f"{cmd}:\n"
                response += f"  Uses: {stats['total']} | Last: {last_used}\n"
            response += "\nUse .adultstats <command> for detailed command statistics```"

        await ctx.send(response)

    @commands.command(
        name="pussy",
        usage="",
        description="Random pussy"
    )
    
    async def pussy(self, ctx):
        await self.send_image(ctx, "pussy")

    @commands.command(
        name="cumm",
        usage="",
        description="Baby gravy!"
    )
    
    async def cumm(self, ctx):
        await self.send_image(ctx, "pgif")

    @commands.command(
        name="hblowjob",
        usage="",
        description="Self explainable"
    )
    
    async def blowjob(self, ctx):
        await self.send_image(ctx, "blowjob")

    @commands.command(
        name="ahegao",
        usage="",
        description="Ahegao"
    )
    
    async def ahegao(self, ctx):
        await self.send_image(ctx, "hanal")

    @commands.command(
        name="lewd",
        usage="",
        description="Lewd loli"
    )
    
    async def lewd(self, ctx):
        await self.send_image(ctx, "kanna")

    @commands.command(
        name="feet",
        usage="",
        description="Random feet"
    )
    async def feet(self, ctx):
        await self.send_image(ctx, "feet")

    @commands.command(
        name="lesbian",
        usage="",
        description="Girls rule!"
    )
    async def lesbian(self, ctx):
        await self.send_image(ctx, "pussy")

    @commands.command(name="spank",usage="", description="NSFW for butts")
    async def spank(self, ctx):
        await self.send_image(ctx, "tentacle")

    @commands.command(name="hwallpaper", usage="", description="99% SFW")
    async def hwallpaper(self, ctx):
        await self.send_image(ctx, "yaoi")

    @commands.command(name="midriff", usage="", description="Hentai midriff images")
    async def midriff(self, ctx):
        await self.send_image(ctx, "hmidriff")

    @commands.command(name="holo", usage="", description="Holo images")
    async def holo(self, ctx):
        await self.send_image(ctx, "holo")

    @commands.command(name="hneko", usage="", description="Hentai neko")
    async def hneko(self, ctx):
        await self.send_image(ctx, "hneko")

    @commands.command(name="kemono", usage="", description="Kemonomimi images")
    async def kemono(self, ctx):
        await self.send_image(ctx, "kemonomimi")

    @commands.command(name="anal", usage="", description="Anal images")
    async def anal(self, ctx):
        await self.send_image(ctx, "anal")

    @commands.command(name="gonewild", usage="", description="Gone wild images")
    async def gonewild(self, ctx):
        await self.send_image(ctx, "gonewild")

    @commands.command(name="thigh", usage="", description="Thigh images")
    async def thigh(self, ctx):
        await self.send_image(ctx, "thigh")

    @commands.command(name="hthigh", usage="", description="Hentai thigh images")
    async def hthigh(self, ctx):
        await self.send_image(ctx, "hthigh")

    @commands.command(name="gah", usage="", description="Gah images")
    async def gah(self, ctx):
        await self.send_image(ctx, "gah")

    @commands.command(name="coffee", usage="", description="Coffee images")
    async def coffee(self, ctx):
        await self.send_image(ctx, "coffee")

    @commands.command(name="food", usage="", description="Food images")
    async def food(self, ctx):
        await self.send_image(ctx, "food")

    @commands.command(name="paizuri", usage="", description="Paizuri images")
    async def paizuri(self, ctx):
        await self.send_image(ctx, "paizuri")

def setup(bot):
    bot.add_cog(Hentai(bot))