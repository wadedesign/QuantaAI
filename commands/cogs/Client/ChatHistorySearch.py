import nextcord
from nextcord.ext import commands

class ChatHistorySearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def search_chat_history(self, channel: nextcord.TextChannel, query: str):
        results = []
        async for message in channel.history(limit=100):  # Adjust the limit as needed
            if query.lower() in message.content.lower():
                results.append(message)
        return results

    async def send_paginated_results(self, interaction, query, results):
        messages = [f"{message.author}: {message.content}" for message in results]
        result_messages = "\n".join(messages)
        
        if len(result_messages) <= 2000:
            await interaction.response.send_message(f"Search results for '{query}':\n{result_messages}")
        else:
            await interaction.response.send_message(f"Search results for '{query}':")
            await interaction.followup.send("\n".join(messages[:len(messages)//2]))
            await interaction.followup.send("\n".join(messages[len(messages)//2:]))

    @nextcord.slash_command(description="Search for messages containing a keyword in the chat history.")
    @commands.has_permissions(administrator=True)
    async def search(self, interaction: nextcord.Interaction, query: str):
        """Search for messages containing a keyword in the chat history."""
        channel = interaction.channel
        results = await self.search_chat_history(channel, query)

        if results:
            await self.send_paginated_results(interaction, query, results)
        else:
            await interaction.response.send_message(f"No messages found containing '{query}'.")

def setup(bot):
    bot.add_cog(ChatHistorySearchCog(bot))