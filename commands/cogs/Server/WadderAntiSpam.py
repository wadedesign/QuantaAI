import time
from collections import defaultdict
from nextcord.ext import commands

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_message_count = defaultdict(int)
        self.user_last_message_time = defaultdict(float)
        self.message_limit = 5  # Adjust the limit of messages allowed in the time window
        self.time_window = 10  # Adjust the time window in seconds

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        current_time = time.time()
        user_id = message.author.id

        # Check if the user has exceeded the message limit
        if current_time - self.user_last_message_time[user_id] < self.time_window:
            self.user_message_count[user_id] += 1
            if self.user_message_count[user_id] > self.message_limit:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, please stop spamming.")
        else:
            self.user_message_count[user_id] = 1
        self.user_last_message_time[user_id] = current_time

def setup(bot):
    bot.add_cog(AntiSpam(bot))
