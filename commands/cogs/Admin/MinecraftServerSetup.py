
import asyncio
from nextcord.ext import commands, tasks
import nextcord
import requests

# ServerInfo class (done)
class ServerInfo:
    def __init__(self, ip, port, name, description):
        self.ip = ip
        self.port = port
        self.name = name
        self.description = description

    def fetch_info(self):
        try:
            response = requests.get(f"https://api.mcsrvstat.us/2/{self.ip}:{self.port}")
            response.raise_for_status()
            data = response.json()
            if data["online"]:
                info = f"Server: {self.name} ({data['ip']}:{data['port']})\n" \
                    f"Version: {data['version']}\n" \
                    f"Players: {data['players']['online']} / {data['players']['max']}\n" \
                    f"Description: {self.description}"
            else:
                info = f"Server {self.name} ({self.ip}:{self.port}) is offline."
        except requests.exceptions.RequestException as e:
            info = f"Error fetching server information: {e}"
        return info

# ServerInfo Cog class
class ServerInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_info = None
        self.server_info_channel = None
        self.server_info_message = None
        self.refresh_server_info.start()

    @nextcord.slash_command()
    async def setup_server(self, interaction: nextcord.Interaction, ip: str, port: int, channel: nextcord.TextChannel, name: str, description: str):
        """Set up the server information"""
        if interaction.user.guild_permissions.administrator:
            self.server_info = ServerInfo(ip, port, name, description)
            self.server_info_channel = channel
            await interaction.response.send_message(f"Server information will be displayed in {self.server_info_channel.mention} and refreshed every 5 minutes.")
            await self.update_server_info_message()
        else:
            await interaction.response.send_message("You do not have permission to use this command.")

    async def display_server_info(self):
        if self.server_info and self.server_info_channel:
            info = self.server_info.fetch_info()
            
            if "offline" not in info:
                response = requests.get(f"https://api.mcsrvstat.us/2/{self.server_info.ip}:{self.server_info.port}")
                data = response.json()

                # Create an embed
                embed = nextcord.Embed(
                    title=f"{self.server_info.name} ({data['ip']}:{data['port']})",
                    description=self.server_info.description,
                    color=nextcord.Color.green()
                )
                
                # Add server version
                embed.add_field(name="Version", value=data['version'], inline=True)

                # Add player count
                embed.add_field(name="Players", value=f"{data['players']['online']} / {data['players']['max']}", inline=True)

                # Add player names
                if "list" in data["players"]:
                    player_names = ", ".join(data["players"]["list"])
                    embed.add_field(name="Online Players", value=player_names, inline=False)
                else:
                    embed.add_field(name="Online Players", value="No players online", inline=False)

            else:
                embed = nextcord.Embed(
                    title=f"Server {self.server_info.ip}:{self.server_info.port}",
                    description="The server is offline.",
                    color=nextcord.Color.red()
                )

            if self.server_info_message:
                await self.server_info_message.edit(embed=embed)
            else:
                self.server_info_message = await self.server_info_channel.send(embed=embed)

    @tasks.loop(minutes=5)
    async def refresh_server_info(self):
        await self.display_server_info()

    @refresh_server_info.before_loop
    async def before_refresh_server_info(self):
        await self.bot.wait_until_ready()

    async def update_server_info_message(self):
        await self.display_server_info()

# Add the cog to your bot
def setup(bot):
    bot.add_cog(ServerInfoCog(bot))
