import json
import random
import nextcord
from nextcord.ext import commands
import aiohttp


# Todo - Need to add the rest of the roleplay commands!

class WadderRolePlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @nextcord.slash_command(name="roleplay")
    async def main(self, interaction: nextcord.Interaction):
        pass   
    
    @main.subcommand()
    async def baka(self, interaction: nextcord.Interaction, user: nextcord.User = None, message: str = None):

        url = f"http://api.nekos.fun:8080/api/baka"
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            data = await response.json(content_type=None)
        gif = data["image"]

        if user is not None:
            embed_title = f"{user.name} you baka"
        else:
            embed_title = "Bakaa"

        if message is None:
            message = "** **"

        embed = nextcord.Embed(
            title=embed_title,
            description=f"{message}",
            colour=interaction.user.color,
        )
        embed.set_image(url=gif)
        await interaction.send(embed=embed)
        
    @main.subcommand()
    async def blusher(self, interaction: nextcord.Interaction):

        with open("data/RPEmotion.json") as f:
            data = json.load(f)
            gif = random.choice(data["blush"])

        embed = nextcord.Embed(
            title=f"{interaction.user.display_name} is blushing",
            colour=interaction.user.color,
        )
        embed.set_image(url=gif)
        await interaction.send(embed=embed)

        
        
            
def setup(bot):
    bot.add_cog(WadderRolePlayer(bot))