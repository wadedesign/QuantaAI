import httpx
import nextcord
from nextcord.ext import commands

# ! Def- Add way more sub commands (Change whole file) 

class DnD5eCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://www.dnd5eapi.co/api"

    async def fetch_data(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    @nextcord.slash_command()
    async def dnd5e(self, interaction: nextcord.Interaction, endpoint: str, query: str):
        query = query.replace(" ", "-").lower()
        url = f"{self.base_url}/{endpoint}/{query}"
        data = await self.fetch_data(url)

        if data:
            name = data.get("name", "No name")
            desc = data.get("desc", data.get("description", "No description"))
            if isinstance(desc, list):
                desc = desc[0]
            await interaction.response.send_message(f"**{name}**\n{desc}")
        else:
            await interaction.response.send_message(f"{endpoint.capitalize()} not found.")

def setup(bot):
    bot.add_cog(DnD5eCog(bot))
