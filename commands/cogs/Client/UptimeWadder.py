import nextcord
from nextcord.ext import commands, tasks
import asyncio
import random
import aiohttp
import psutil

# ! Could add more sub commands to this

class Uptime(commands.Cog, description="Uptime command"):
    def __init__(self, bot):
        self.bot = bot
        self.ts = 0
        self.tm = 0
        self.th = 0
        self.td = 0
        self.uptimeCounter.start()

    def cog_unload(self):
        self.uptimeCounter.cancel()

    @tasks.loop(seconds=1)
    async def uptimeCounter(self):
        self.ts += 2
        if self.ts == 60:
            self.ts = 0
            self.tm += 1
            if self.tm == 60:
                self.tm = 0
                self.th += 1
                if self.th == 24:
                    self.th = 0
                    self.td += 1

    @uptimeCounter.before_loop
    async def beforeUptimeCounter(self):
        await self.bot.wait_until_ready()

    @nextcord.slash_command(name="uptime", description="Shows the uptime of the bot")
    async def uptimewadder(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Uptime", description="Here is the uptime of the bot", color=nextcord.Color.blue())
        embed.add_field(name="Days", value=self.td, inline=True)
        embed.add_field(name="Hours", value=self.th, inline=True)
        embed.add_field(name="Minutes", value=self.tm, inline=True)
        embed.add_field(name="Seconds", value=self.ts, inline=True)
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=True)
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%", inline=True)
        embed.add_field(name="Disk", value=f"{psutil.disk_usage('/').percent}%", inline=True)
        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(Uptime(bot))

    