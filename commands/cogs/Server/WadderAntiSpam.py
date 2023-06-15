import time
from collections import defaultdict
from nextcord import Embed
from nextcord.ext import commands
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
spam_collection = db["spam"]

# ** Ready for Production **

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_message_count = defaultdict(int)
        self.user_last_message_time = defaultdict(float)
        self.message_limit = 5  # Adjust the limit of messages allowed in the time window
        self.time_window = 10  # Adjust the time window in seconds
        self.command_message_count = defaultdict(int)
        self.command_message_limit = 3  # Adjust the limit of command messages allowed in the time window

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        current_time = time.time()
        user_id = message.author.id
        server_id = message.guild.id

        # Check if the user has exceeded the message limit
        if current_time - self.user_last_message_time[user_id] < self.time_window:
            self.user_message_count[user_id] += 1
            if self.user_message_count[user_id] > self.message_limit:
                await message.delete()
                await message.channel.send(embed=self.create_spam_embed(message.author))
                self.save_spam_data(message.author.name, message.content, message.guild.name)
        else:
            self.user_message_count[user_id] = 1
        self.user_last_message_time[user_id] = current_time

        # Check if the user has exceeded the command message limit
        if message.content.startswith(self.bot.command_prefix):
            self.command_message_count[user_id] += 1
            if self.command_message_count[user_id] > self.command_message_limit:
                await message.delete()
                await message.channel.send(embed=self.create_spam_embed(message.author))
                self.save_spam_data(message.author.name, message.content, message.guild.name)

    def create_spam_embed(self, author):
        embed = Embed(title="QAnti-Spam", color=0xff0000)
        embed.description = f"{author.mention}, please stop spamming."
        embed.set_thumbnail(url=author.avatar.url)
        return embed

    def save_spam_data(self, author_name, message_content, server_name):
        spam_data = {
            "author_name": author_name,
            "message_content": message_content,
            "server_name": server_name,
            "timestamp": time.time()
        }
        spam_collection.insert_one(spam_data)

def setup(bot):
    bot.add_cog(AntiSpam(bot))





# TODO - Add Admin Support
# TODO - Add Logging