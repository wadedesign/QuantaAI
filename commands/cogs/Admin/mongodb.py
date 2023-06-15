import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
message_collection = db["messagesquanta"]
user_collection = db["usersquanta"]
server_collection = db["serversquanta"]


class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:  # Ignore messages from bots
            # Log the message
            message_data = {
                "message_id": message.id,
                "content": message.content,
                "author_id": message.author.id,
                "channel_id": message.channel.id,
                "server_id": message.guild.id if message.guild else None
            }
            message_collection.insert_one(message_data)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Log the server
        server_data = {
            "server_id": guild.id,
            "server_name": guild.name,
            "owner_id": guild.owner.id,
            "member_count": guild.member_count
        }
        server_collection.insert_one(server_data)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # Remove the server data from the database when the bot is removed from a server
        server_collection.delete_one({"server_id": guild.id})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Log the user who joins the server
        user_data = {
            "user_id": member.id,
            "username": member.name,
            "server_id": member.guild.id
        }
        user_collection.insert_one(user_data)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Remove the user data from the database when a user leaves the server
        user_collection.delete_one({"user_id": member.id, "server_id": member.guild.id})


def setup(bot):
    bot.add_cog(LoggingCog(bot))
