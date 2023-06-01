import aiohttp
import nextcord
from nextcord.ext import commands
from numbers import Number
from random import randint

BaseCog = getattr(commands, "Cog", object)


## ! Make more sub commands of this! ##


class XKCD(BaseCog):
    """Display XKCD entries"""

    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(name='dev3')
    async def dev3(self, interaction: nextcord.Interaction):
       pass

    @dev3.subcommand(name="xkcd", description="To get xkcd comics")
    async def xkcd(self, interaction: nextcord.Interaction, *, entry_number=None):
        await interaction.response.defer()


        # Creates random number between 0 and 2190 (number of xkcd comics at time of writing) and queries xkcd
        headers = {"content-type": "application/json"}
        url = "https://xkcd.com/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd_latest = await response.json()
                xkcd_max = xkcd_latest.get("num") + 1

        if entry_number is not None and int(entry_number) > 0 and int(entry_number) < xkcd_max:
            i = int(entry_number)
        else:
            i = randint(0, xkcd_max)
        headers = {"content-type": "application/json"}
        url = "https://xkcd.com/" + str(i) + "/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd = await response.json()

        # Build Embed
        embed = nextcord.Embed()
        embed.title = xkcd["title"] + " (" + xkcd["day"] + "/" + xkcd["month"] + "/" + xkcd["year"] + ")"
        embed.url = "https://xkcd.com/" + str(i)
        embed.description = xkcd["alt"]
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text="Powered by xkcd")
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(XKCD(bot))