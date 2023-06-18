import nextcord
from nextcord.ext import commands, tasks
import psutil
from datetime import datetime

class Uptime(commands.Cog, description="Uptime command"):
    def __init__(self, bot):
        self.bot = bot
        self.ts = 0
        self.tm = 0
        self.th = 0
        self.td = 0
        self.uptime_message = None
        self.uptimeCounter.start()

    def cog_unload(self):
        self.uptimeCounter.cancel()

    @tasks.loop(seconds=1)
    async def uptimeCounter(self):
        self.ts += 1
        if self.ts == 60:
            self.ts = 0
            self.tm += 1
            if self.tm == 60:
                self.tm = 0
                self.th += 1
                if self.th == 24:
                    self.th = 0
                    self.td += 1

        if self.uptime_message:
            await self.update_uptime_message()

    async def update_uptime_message(self):
        current_time = datetime.now().strftime("%m/%d/%Y %I:%M %p")

        embed = nextcord.Embed(title="Bot Uptime", color=nextcord.Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name=":globe_with_meridians: Global Statistics", value=f"Guilds: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}", inline=False)
        embed.add_field(name=":computer: System Statistics", value="\u200b", inline=False)
        embed.add_field(name=":bar_chart: CPU Usage", value=f"{psutil.cpu_percent()}%", inline=False)
        memory = psutil.virtual_memory()
        embed.add_field(name=":chart_with_upwards_trend: RAM Usage", value=f"{memory.used / (1024 * 1024):.2f} MB / {memory.total / (1024 * 1024):.2f} MB", inline=False)
        embed.add_field(name=":gear: Specifications", value="CPU: Intel Xeon E5-2670v2\nRAM: DDR3 @ 1333 MHz RAM\nStorage: RAID 10 SSD\nNetwork: 1 Gbit Multi-blend", inline=False)
        embed.add_field(name=":snake: Python Version", value="v3.11", inline=False)
        embed.add_field(name=":robot: Nextcord Version", value="^2.4.2", inline=False)
        embed.set_footer(text=f"Bot Uptime • {current_time}")

        await self.uptime_message.edit(embed=embed)

    @uptimeCounter.before_loop
    async def beforeUptimeCounter(self):
        await self.bot.wait_until_ready()
        channel_id = 1110811750724554803  # Replace with your channel ID
        channel = self.bot.get_channel(channel_id)
        self.uptime_message = await channel.send("Calculating uptime...")

    @nextcord.slash_command(name="uptime", description="Shows the uptime of the bot")
    async def uptimewadder(self, interaction: nextcord.Interaction):
        current_time = datetime.now().strftime("%m/%d/%Y %I:%M %p")

        embed = nextcord.Embed(title="Bot Uptime", color=nextcord.Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name=":globe_with_meridians: Global Statistics", value=f"Guilds: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}", inline=False)
        embed.set_footer(text=f"Bot Uptime • {current_time}")

        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(Uptime(bot))





    