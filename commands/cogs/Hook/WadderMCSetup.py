import nextcord
from nextcord.ext import commands
import requests
import asyncio


class ServerStats2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_url = "https://api.mcstatus.io/v2/status/java/208.52.147.254:25565"
        self.server_stats = None
        self.refresh_task = self.bot.loop.create_task(self.refresh_server_status())

    async def refresh_server_status(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.get_server_stats()
            embed = self.get_stats_embed()
            await self.send_server_status_to_channel(embed)
            await asyncio.sleep(180)  # Refresh every 3 minutes

    async def get_server_stats(self):
        response = requests.get(self.server_url)
        if response.status_code == 200:
            self.server_stats = response.json()
            return True
        return False

    def get_stats_embed(self):
        if self.server_stats["online"]:
            embed = nextcord.Embed(title="Server Status", color=nextcord.Color.green())
            embed.add_field(name="Status", value="Online")
            embed.add_field(name="Current version", value=self.server_stats['version']['name_raw'])
            embed.add_field(name="Players online", value=f"{self.server_stats['players']['online']}/{self.server_stats['players']['max']}")
            embed.add_field(name="MOTD", value=self.server_stats['motd']['clean'])

            if 'list' in self.server_stats['players']:
                players = "\n".join([f"👤 {player['name_raw']}" for player in self.server_stats['players']['list']])
                embed.add_field(name="Players", value=players, inline=False)

            return embed
        else:
            embed = nextcord.Embed(title="Server Status", color=nextcord.Color.red())
            embed.add_field(name="Status", value="Offline")
            return embed

    async def send_server_status_to_channel(self, embed):
        channel_id = 1090816795650301952 # replace with the channel ID you want to send the message to
        channel = self.bot.get_channel(channel_id)
        if channel:
            # Check if previous status message exists
            async for message in channel.history():
                if message.author == self.bot.user and message.embeds and message.embeds[0].title == "Server Status":
                    await message.edit(embed=embed)
                    return

            # Send the new status message if no previous message was found
            await channel.send(embed=embed)

  

def setup(bot):
    bot.add_cog(ServerStats2(bot))