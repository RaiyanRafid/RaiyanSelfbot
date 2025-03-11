import requests
from discord.ext import commands
from config import (
    BotConfig,
    APIConfig,
    CommandConfig,
    TimingConfig,
    DisplayConfig
)

languages = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
}

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = APIConfig.IPServices.GENERAL_API_KEY
        self.infectoken = BotConfig.TOKEN


    @commands.command(name='tokeninfo', aliases=['tdox'], brief="Shows token info", usage=".tokeninfo <user.token>")
   
    async def tokeninfo(self, ctx, _token):
        await ctx.message.delete()
        headers = {
            'Authorization': _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            language = languages.get(locale)
            creation_date = f"<t:{int(((int(user_id) >> 22) + 1420070400000) / 1000)}:R>"
        except KeyError:
            headers = {
                'Authorization': "Bot " + _token,
                'Content-Type': 'application/json'
            }
            try:
                res = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
                res = res.json()
                user_id = res['id']
                locale = res['locale']
                avatar_id = res['avatar']
                language = languages.get(locale)
                creation_date = f"<t:{int(((int(user_id) >> 22) + 1420070400000) / 1000)}:R>"
                message = (
                    f"**~ Name: {res['username']}#{res['discriminator']}  **BOT**\n"
                    f"~ ID: {res['id']}\n"
                    f"~ Email: {res['email']}\n"
                    f"~ Created on: {creation_date}`"
                )
                fields = [
                    {'name': '~ Flags', 'value': res['flags']},
                    {'name': '~ Lang', 'value': res['locale']},
                    {'name': '~ Verified', 'value': res['verified']},
                ]
                for field in fields:
                    if field['value']:
                        message += f"\n{field['name']}: {field['value']}"
                message += f"\n~ Avatar URL: https://cdn.discordapp.com/avatars/{user_id}/{avatar_id} **"
                return await ctx.send(message)
            except KeyError:
                return await ctx.send("Invalid token", delete_after=30)

        message = (
            f"**~ Name: {res['username']}#{res['discriminator']}\n"
            f"~ ID: {res['id']}\n"
            f"~ Created On: {creation_date}"
        )
        nitro_type = "None"
        if "premium_type" in res:
            if res['premium_type'] == 2:
                nitro_type = "Nitro Boost"
            elif res['premium_type'] == 3:
                nitro_type = "Nitro Basic"
        fields = [
            {'name': '~ Phone', 'value': res['phone']},
            {'name': '~ Flags', 'value': res['flags']},
            {'name': '~ Lang', 'value': res['locale']},
            {'name': '~ 2FA', 'value': res['mfa_enabled']},
            {'name': '~ Verified', 'value': res['verified']},
            {'name': '~ Nitro', 'value': nitro_type},
        ]
        for field in fields:
            if field['value']:
                message += f"\n{field['name']}: {field['value']}"
        message += f"\n~ Avatar URL: https://cdn.discordapp.com/avatars/{user_id}/{avatar_id} **"
        await ctx.send(message, delete_after=30)

    @commands.command(name='iplook', aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'], brief="Advanced IP Information", usage=".iplook <ip.address>")
    async def iplook(self, ctx, ip):
        try:
            # Using ipinfo.io API with token from config
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {APIConfig.IPServices.IPINFO_TOKEN}'
            }
            response = requests.get(f'https://ipinfo.io/{ip}/json', headers=headers)
            data = response.json()

            # Check for error in response
            if 'error' in data:
                await ctx.send(f"```❌ Error: {data['error']['message']}```", delete_after=TimingConfig.DELETE_TIMEOUT)
                return

            # Get additional abuse/threat data
            try:
                abuse_response = requests.get(
                    f'https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays={CommandConfig.IPLookup.MAX_AGE_DAYS}&verbose=true', 
                    headers={'Key': APIConfig.IPServices.ABUSEIPDB_TOKEN, 'Accept': 'application/json'})
                abuse_data = abuse_response.json().get('data', {})
            except:
                abuse_data = {}

            # Create main IP info response
            response = (
                "```\n"
                "╔════════════════ IP INFORMATION ═══════════════╗\n"
                "║                                               ║\n"
                f"║  🌐 IP Address: {ip:<33} ║\n"
                f"║  📡 Hostname:  {data.get('hostname', 'N/A'):<33} ║\n"
                f"║  🏢 Company:   {data.get('org', 'N/A'):<33} ║\n"
                f"║  🔌 ASN:       {data.get('asn', 'N/A'):<33} ║\n"
                "║                                               ║\n"
                "╠═════════════════ LOCATION ══════════════════╣\n"
                f"║  🏙️ City:      {data.get('city', 'N/A'):<33} ║\n"
                f"║  🏛️ State:     {data.get('region', 'N/A'):<33} ║\n"
                f"║  🌍 Country:   {data.get('country', 'N/A'):<33} ║\n"
                f"║  📮 Postal:    {data.get('postal', 'N/A'):<33} ║\n"
                f"║  🗺️ Coords:    {data.get('loc', 'N/A'):<33} ║\n"
                f"║  ⏰ Timezone:  {data.get('timezone', 'N/A'):<33} ║\n"
            )

            # Add network information
            response += (
                "║                                               ║\n"
                "╠════════════════ NETWORK ═══════════════════╣\n"
                f"║  📶 ASN Type:   {data.get('asn', {}).get('type', 'N/A'):<32} ║\n"
                f"║  🌐 Range:      {data.get('asn', {}).get('route', 'N/A'):<32} ║\n"
                f"║  🔄 Anycast:    {'Yes' if data.get('anycast') else 'No':<32} ║\n"
            )

            # Add abuse information if available
            if abuse_data:
                response += (
                    "║                                               ║\n"
                    "╠════════════════ SECURITY ══════════════════╣\n"
                    f"║  ⚠️ Abuse Score:   {abuse_data.get('abuseConfidenceScore', 'N/A')}%{' ' * 27} ║\n"
                    f"║  🛡️ Total Reports: {abuse_data.get('totalReports', 'N/A'):<32} ║\n"
                    f"║  📧 Abuse Contact: {data.get('abuse', {}).get('email', 'N/A'):<32} ║\n"
                )

            # Add privacy information
            privacy_section = []
            privacy = data.get('privacy', {})
            if privacy:
                response += (
                    "║                                               ║\n"
                    "╠════════════════ PRIVACY ═══════════════════╣\n"
                    f"║  🔒 VPN:        {'Yes' if privacy.get('vpn') else 'No':<32} ║\n"
                    f"║  🔐 Proxy:      {'Yes' if privacy.get('proxy') else 'No':<32} ║\n"
                    f"║  🌐 Tor:        {'Yes' if privacy.get('tor') else 'No':<32} ║\n"
                    f"║  📡 Relay:      {'Yes' if privacy.get('relay') else 'No':<32} ║\n"
                    f"║  🏢 Hosting:    {'Yes' if privacy.get('hosting') else 'No':<32} ║\n"
                    f"║  🔍 Service:    {privacy.get('service', 'N/A'):<32} ║\n"
                )

            response += (
                "║                                               ║\n"
                "╚═══════════════════════════════════════════════╝\n"
                "```"
            )

            # Add additional information if available
            additional_info = []
            
            # Add hosted domains if available
            if 'domains' in data:
                domains_info = "\n**📋 Hosted Domains**\n"
                domains = data['domains'][:5] if len(data['domains']) > 5 else data['domains']
                domains_info += "\n".join([f"• {domain}" for domain in domains])
                if len(data['domains']) > 5:
                    domains_info += f"\n• ... and {len(data['domains']) - 5} more"
                additional_info.append(domains_info)

            # Add recent abuse reports if available
            if abuse_data and abuse_data.get('reports', []):
                reports_info = "\n**⚠️ Recent Reports**\n"
                reports = abuse_data['reports'][:3]
                for report in reports:
                    reports_info += f"• {report.get('reportedAt', 'N/A')}: {report.get('comment', 'No comment')[:100]}\n"
                additional_info.append(reports_info)

            if additional_info:
                response += "\n" + "\n".join(additional_info)

            await ctx.send(response, delete_after=60)

        except requests.RequestException as e:
            await ctx.send(f"```❌ Error: Network request failed - {str(e)}```", delete_after=30)
        except Exception as e:
            await ctx.send(f"```❌ Error: {str(e)}```", delete_after=30)


    @commands.command(name='id', aliases=['snowflake'], brief="Shows dev id of target", usage=".id <target>")
   
    async def id(self, ctx, *targets):
        if not targets:
            await ctx.send(f"Your ID is: {ctx.author.id}")
        else:
            for target in targets:
                if target.lower() == "server":
                        await ctx.send("**~ ID of the server is**", delete_after=30)
                        await ctx.send(ctx.guild.id, delete_after=30)
                elif len(ctx.message.mentions) > 0:
                    for member in ctx.message.mentions:
                        await ctx.send(f"**~ ID of {member.name} is**", delete_after=30)
                        await ctx.send(member.id, delete_after=30)
                elif len(ctx.message.channel_mentions) > 0:
                    for channel in ctx.message.channel_mentions:
                        await ctx.send(f"**~ ID of {channel.name} is**", delete_after=30)
                        await ctx.send(channel.id, delete_after=30)
                elif len(ctx.message.role_mentions) > 0:
                    for role in ctx.message.role_mentions:
                        await ctx.send(f"**~ ID of {role.name} role is**", delete_after=30)
                        await ctx.send(role.id, delete_after=30)
                else:
                    await ctx.send(f"~ Cant look for this mention: {target}", delete_after=30)
      
    @commands.command(name='calculation', aliases=['c', 'mathcalc', 'compute', 'solve'], brief="Advanced Calculator", usage=".calculation <expression>")
    async def calculation(self, ctx, *, calculation):
        try:
            # Clean up the input
            calculation = calculation.replace('x', '*').replace('×', '*').replace('÷', '/')
            
            # Basic evaluation
            result = eval(calculation)
            
            # Format numbers with commas and handle decimals
            if isinstance(result, (int, float)):
                if isinstance(result, float):
                    # Round to 6 decimal places if it's a float
                    result = round(result, 6)
                formatted_result = "{:,}".format(result)
                
                # Scientific notation for very large or very small numbers
                if abs(result) > 1000000 or (abs(result) < 0.000001 and result != 0):
                    scientific = "{:e}".format(result)
                else:
                    scientific = None
                
                # Calculate percentage for decimal numbers
                if isinstance(result, float) and 0 < abs(result) < 1:
                    percentage = result * 100
                else:
                    percentage = None

                # Create response with improved formatting
                response = (
                    "```\n"
                    "╔═════════════ CALCULATION RESULT ════════════╗\n"
                    "║                                             ║\n"
                    f"║  📝 Expression: {calculation:<29} ║\n"
                    "║                                             ║\n"
                    "╠════════════════ RESULTS ══════════════════╣\n"
                    f"║  🔢 Standard:  {formatted_result:<29} ║\n"
                )
                
                # Add scientific notation for large/small numbers
                if scientific:
                    response += f"║  📊 Scientific: {scientific:<29} ║\n"
                
                # Add percentage for decimal numbers
                if percentage is not None:
                    response += f"║  📈 Percentage: {percentage:.2f}%{' ' * 24} ║\n"
                
                # Add operation type
                if '*' in calculation:
                    response += f"║  ✖️ Operation: Multiplication{' ' * 20} ║\n"
                elif '/' in calculation:
                    response += f"║  ➗ Operation: Division{' ' * 24} ║\n"
                elif '+' in calculation:
                    response += f"║  ➕ Operation: Addition{' ' * 24} ║\n"
                elif '-' in calculation:
                    response += f"║  ➖ Operation: Subtraction{' ' * 22} ║\n"
                
                response += (
                    "║                                             ║\n"
                    "╚═════════════════════════════════════════════╝\n"
                    "```\n"
                    "**💡 Tips:**\n"
                    "• Use `x` or `*` for multiplication\n"
                    "• Use `/` for division\n"
                    "• Supports complex expressions"
                )
            else:
                response = f"```\nResult: {result}```"
                
            await ctx.send(response, delete_after=60)
            
        except ZeroDivisionError:
            await ctx.send("```❌ Error: Cannot divide by zero```", delete_after=30)
        except (SyntaxError, NameError, TypeError):
            await ctx.send(
                "```❌ Error: Invalid calculation\n"
                "Make sure to use proper mathematical operators:\n"
                "• Multiplication: * or x\n"
                "• Division: /\n"
                "• Addition: +\n"
                "• Subtraction: -```", 
                delete_after=30
            )
        except Exception as e:
            await ctx.send(f"```❌ Error: {str(e)}```", delete_after=30)


def setup(bot):
    bot.add_cog(Info(bot))