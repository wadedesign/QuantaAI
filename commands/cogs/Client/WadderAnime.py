import ast
import asyncio
from bs4 import BeautifulSoup
import nextcord
from nextcord.ext import commands

class Anime(commands.Cog):
    """Anime commands"""

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Sends a waifu")
    async def waifu(self, interaction: nextcord.Interaction):
        """Sends [Waifu](https://www.dictionary.com/e/fictional-characters/waifu) pictures"""

        async with interaction.channel.typing():
            while True:
                try:
                    async with self.bot.session.get("https://mywaifulist.moe/random") as resp:
                        response = await resp.text()
                    soup = BeautifulSoup(response, "html.parser")
                    image_url = ast.literal_eval(
                        "{" + str(soup.find("script", type="application/ld+json")).split("\n      ")[3].split(",")[0] + "}"
                    )["image"]
                    name = ast.literal_eval(
                        "{" + str(soup.find("script", type="application/ld+json")).split("\n      ")[4].split(",")[0] + "}"
                    )["name"]
                    gender = ast.literal_eval(
                        "{" + str(soup.find("script", type="application/ld+json")).split("\n      ")[5].split(",")[0] + "}"
                    )["gender"]

                    if gender != "male":
                        break
                except IndexError:
                    continue

            embed = nextcord.Embed(title=name.replace("&quot;", '"'), color=0x2F3136)
            embed.set_image(url=image_url)

        message = await interaction.response.send_message(embed=embed, ephemeral=False)
        await message.add_reaction("\u2764\ufe0f")

        def check(r, u):  # r = nextcord.Reaction, u = nextcord.Member or nextcord.User.
            return u.id == interaction.user.id and r.message.channel.id == interaction.channel.id

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=10)
        except asyncio.TimeoutError:
            try:
                return await message.clear_reactions()
            except nextcord.Forbidden:
                return await message.remove_reaction("\u2764\ufe0f", interaction.guild.me)
        else:
            if str(reaction.emoji) == "\u2764\ufe0f":
                embed.set_footer(icon_url=interaction.user.avatar.url, text=f"Claimed by {interaction.user.name}")
                await message.edit(embed=embed)
                return await interaction.followup.send(
                    f":couple_with_heart: {interaction.user.mention} is now married with"
                    f"**{name.replace('&quot;', '')}** :couple_with_heart:"
                )

def setup(bot):
    """Adds the cog to the bot"""
    bot.add_cog(Anime(bot))







