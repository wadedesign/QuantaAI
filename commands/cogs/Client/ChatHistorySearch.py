import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
chat_history_collection = db["chat_history"]


class ChatHistorySearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def search_chat_history(self, channel: nextcord.TextChannel, query: str):
        results = []
        async for message in channel.history(limit=100):  # Adjust the limit as needed
            if query.lower() in message.content.lower():
                results.append(message)
        return results

    async def save_chat_history(self, results):
        chat_data = []
        for message in results:
            chat_data.append({
                "author": str(message.author),
                "content": message.content
            })
        chat_history_collection.insert_many(chat_data)

    async def send_paginated_results(self, interaction, query, results):
        messages = [f"{message.author}: {message.content}" for message in results]
        result_messages = "\n".join(messages)

        if len(result_messages) <= 2000:
            await interaction.response.send_message(f"✉️ Search results for '{query}':\n{result_messages}")
        else:
            await interaction.response.send_message(f"✉️ Search results for '{query}':")
            await interaction.followup.send("📃 " + "\n".join(messages[:len(messages)//2]))
            await interaction.followup.send("📃 " + "\n".join(messages[len(messages)//2:]))

    @nextcord.slash_command(name='chatsearch', description="Search for messages containing a keyword in the chat history.")
    @commands.has_permissions(administrator=True)
    async def search(self, interaction: nextcord.Interaction, query: str):
        """Search for messages containing a keyword in the chat history."""
        channel = interaction.channel
        results = await self.search_chat_history(channel, query)

        if results:
            await self.save_chat_history(results)
            await self.send_paginated_results(interaction, query, results)
        else:
            await interaction.response.send_message(f"❌ No messages found containing '{query}'.")


def setup(bot):
    bot.add_cog(ChatHistorySearchCog(bot))

