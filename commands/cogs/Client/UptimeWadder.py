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
        
        # Prepare values
        global_users = len(self.bot.users)
        global_guilds = len(self.bot.guilds)
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 * 1024)
        memory_total = memory.total / (1024 * 1024)
        
        # Create embed
        embed = nextcord.Embed(title="Bot Uptime 🤖", color=nextcord.Color.blue())
        
        # System Info
        embed.add_field(name="💻 System Info", value="QuantaAI", inline=True)
        embed.add_field(name="CPU", value=f"🖥️ **Intel Xeon E5-2670v2** - Usage: **{cpu_usage}%**", inline=True)
        embed.add_field(name="RAM", value=f"💾 **DDR3 @ 1333 MHz** - Usage: **{memory_used:.2f} MB / {memory_total:.2f} MB**", inline=True)
        embed.add_field(name="Storage", value="💽 **RAID 10 SSD**", inline=True)
        embed.add_field(name="Network", value="🌐 **1 Gbit Multi-blend**", inline=True)
        
        # Bot Info
        embed.add_field(name="🤖 Bot Info", value="Dif", inline=True)
        embed.add_field(name="Python Version", value="🐍 **v3.11**", inline=True)
        embed.add_field(name="Nextcord Version", value="🤖 **^2.4.2**", inline=True)
        
        # Global Statistics
        embed.add_field(name="🌍 Global Statistics", value="Dif", inline=True)
        embed.add_field(name="Guild Count", value=f"🌐 **{global_guilds}**", inline=True)
        embed.add_field(name="User Count", value=f"👥 **{global_users}**", inline=True)
        
        # Set footer
        embed.set_footer(text=f"🕒 Last Updated • {current_time}")

        # Send the embed
        await self.uptime_message.edit(embed=embed)



    @uptimeCounter.before_loop
    async def beforeUptimeCounter(self):
        await self.bot.wait_until_ready()
        channel_id = 1110811750724554803  # Replace with your channel ID
        channel = self.bot.get_channel(channel_id)
        self.uptime_message = await channel.send("Calculating uptime...")



def setup(bot):
    bot.add_cog(Uptime(bot))





    