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

    @uptimeCounter.before_loop
    async def beforeUptimeCounter(self):
        await self.bot.wait_until_ready()

    @nextcord.slash_command(name="uptime", description="Shows the uptime of the bot")
    async def uptimewadder(self, interaction: nextcord.Interaction):
        guild_count_emoji = "🏰"
        global_users_emoji = "👥"
        cpu_emoji = "💻"
        ram_emoji = "🔒"
        nodejs_emoji = "📦"
        discordjs_emoji = "💬"

        current_time = datetime.now().strftime("%m/%d/%Y %I:%M %p")

        embed = nextcord.Embed(title="Bot Uptime", color=nextcord.Color.blue())
        embed.add_field(name="Global Statistics", value=f"{guild_count_emoji} Guild Count - {len(self.bot.guilds)}", inline=False)
        embed.add_field(name="\u200b", value=f"{global_users_emoji} Global Users - {len(self.bot.users)}", inline=False)
        embed.add_field(name="System Statistics", value="\u200b", inline=False)
        embed.add_field(name=f"{cpu_emoji} CPU", value=f"Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz", inline=False)
        embed.add_field(name=f"{cpu_emoji} CPU Usage", value=f"{psutil.cpu_percent()}%", inline=False)
        memory = psutil.virtual_memory()
        embed.add_field(name=f"{ram_emoji} RAM Usage", value=f"{memory.used / (1024 * 1024):.2f} MB / {memory.total / (1024 * 1024):.2f} MB", inline=False)
        embed.add_field(name=f"{nodejs_emoji} Node.JS Version", value="v17.9.1", inline=False)
        embed.add_field(name=f"{discordjs_emoji} Discord.js Version", value="^13.1.0", inline=False)
        embed.set_footer(text=f"Bot Uptime • {current_time}")

        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(Uptime(bot))



    