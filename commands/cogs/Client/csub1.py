import asyncio
import io
import random
import aiohttp
import nextcord
from nextcord.ext import commands
from numbers import Number
from random import randint
from pymongo import MongoClient
import urllib.parse

import requests

BaseCog = getattr(commands, "Cog", object)


# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
nba_collection = db["nba_players"]

## ! Make more sub commands of this! ##

version1="1.0 Beta"
version2 ="`optimization upgrade, chat gpt improvements, chat gpt in mp work, dalle avalaible work in mp too, mention bot in mp work, report work in mp, version work in mp and ping work in mp`"

version3="Bot V.0906-23.beta"
version4 ="`optimization upgrade, chat gpt and mention bot help in text channels`"


class XKCD(BaseCog):
    """Display XKCD entries"""

    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = "https://nextcord.com/api/webhooks/1120068450052735016/c-CKTSRuo4YtBWOdUwRDEL-mO5DnOJbpIFGxgyRo7kjQbJ_3CHaqdYLdovEX4ZJOF8Eu" # Remplacez WEBHOOK

        
    @nextcord.slash_command(name='dev3')
    async def main(self, interaction: nextcord.Interaction):
       pass

    @main.subcommand(name="xkcd", description="To get xkcd comics")
    async def xkcd(self, interaction: nextcord.Interaction, *, entry_number=None):

        # Define the computer animation frames
        animation = [
            "```yaml\n[Fetching xkcd comic...     ]```",
            "```yaml\n[Fetching xkcd comic...•    ]```",
            "```yaml\n[Fetching xkcd comic...••   ]```",
            "```yaml\n[Fetching xkcd comic...•••  ]```",
            "```yaml\n[Fetching xkcd comic...•••• ]```",
            "```yaml\n[Fetching xkcd comic...•••••]```",
            "```yaml\n[Fetching xkcd comic... ••••]```",
            "```yaml\n[Fetching xkcd comic...  •••]```",
            "```yaml\n[Fetching xkcd comic...   ••]```",
            "```yaml\n[Fetching xkcd comic...    •]```",
            "```yaml\n[Fetching xkcd comic...     ]```",
            "```yaml\n[Fetching xkcd comic...    ]```",
            "```yaml\n[Fetching xkcd comic...•   ]```",
            "```yaml\n[Fetching xkcd comic...••  ]```",
            "```yaml\n[Fetching xkcd comic...••• ]```",
            "```yaml\n[Fetching xkcd comic...••••]```",
            "```yaml\n[Fetching xkcd comic...•••••]```",
            "```yaml\n[Fetching xkcd comic...•••• ]```",
            "```yaml\n[Fetching xkcd comic...•••  ]```",
            "```yaml\n[Fetching xkcd comic...••   ]```",
            "```yaml\n[Fetching xkcd comic...•    ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Fetch the xkcd comic
        headers = {"content-type": "application/json"}
        url_latest = "https://xkcd.com/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url_latest, headers=headers) as response:
                xkcd_latest = await response.json()
                xkcd_max = xkcd_latest.get("num") + 1

        if entry_number is not None and int(entry_number) > 0 and int(entry_number) < xkcd_max:
            i = int(entry_number)
        else:
            i = random.randint(0, xkcd_max)

        url = f"https://xkcd.com/{i}/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd = await response.json()

        # Delete the loading message
        await loading_message.delete()

        # Build Embed
        embed = nextcord.Embed()
        embed.title = f"{xkcd['title']} ({xkcd['day']}/{xkcd['month']}/{xkcd['year']})"
        embed.url = f"https://xkcd.com/{i}"
        embed.description = xkcd["alt"]
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text="Powered by xkcd")
        await interaction.send(embed=embed)


        
    @main.subcommand(name="nba", description="To get NBA players")
    async def nba_player(self, interaction: nextcord.Interaction, name: str):
        search_url = "https://free-nba.p.rapidapi.com/players"
        search_params = {
            "search": name,
            "per_page": 5
        }

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
        }

        search_response = requests.get(search_url, headers=headers, params=search_params)
        search_results = search_response.json()["data"]

        if not search_results:
            await interaction.send("No players found with that name.")
            return

        player_ids = [player["id"] for player in search_results]
        player_data = []

        for player_id in player_ids:
            player_url = f"https://free-nba.p.rapidapi.com/players/{player_id}"
            player_response = requests.get(player_url, headers=headers)
            player_data.append(player_response.json())

        nba_collection.insert_many(player_data)

        for player in player_data:
            player_name = player['first_name'] + " " + player['last_name']
            player_team = player['team']['full_name']
            player_stats = (
                str(player['height_feet'])
                + " ft "
                + str(player['height_inches'])
                + " in, "
                + str(player['weight_pounds'])
                + " lbs"
            )

            image_search_url = "https://api.unsplash.com/search/photos"
            image_search_params = {
                "query": player_name,
                "per_page": 1,
                "client_id": "8_x4s8mZvLnV6ZzBsiEfWIdq8ZL_utvXX5MdtyDgm34"
            }

            image_response = requests.get(image_search_url, params=image_search_params)
            image_data = image_response.json()["results"]

            if image_data:
                player_image = image_data[0]["urls"]["small"]
            else:
                player_image = None

            embed = nextcord.Embed(title="NBA Player Information", description=f"Player: {player_name}", color=0x00ff00)
            embed.add_field(name="Team", value=player_team, inline=False)
            embed.add_field(name="Stats", value=player_stats, inline=False)

            if player_image:
                embed.set_thumbnail(url=player_image)

            await interaction.send(embed=embed)
            
    '''         
    @main.subcommand()
    async def qversion(self, interaction: nextcord.Interaction):
        if isinstance(interaction.channel, nextcord.TextChannel):
            await interaction.response.defer()
        embed = nextcord.Embed(title="Versions du Bot", color=nextcord.Color.random())
        embed.set_author(name=f"Demandé par {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.add_field(name="", value="")
        embed.add_field(name="Last Version", value=version1)
        embed.add_field(name="Update Logs", value=version2)
        embed.add_field(name="", value="")
        embed.add_field(name="Old Version", value=version3)
        embed.add_field(name="Update Logs", value=version4)
        embed.add_field(name="", value="")
        embed.add_field(name="Preview Version", value="Bot V.0103-23.alpha")
        embed.add_field(name="Update Logs", value="`Optimisation, First update and alot of new command`")
        embed.add_field(name="Date format", value="`MM/DD/YY`")
        with open("images/quantaai/png/logo-black.png", "rb") as f:
            image_data = f.read()
        embed.set_thumbnail(url="attachment://logo-black.png")
        await interaction.send(embed=embed, file=nextcord.File(io.BytesIO(image_data), "logo-black.png"))
    '''
    @main.subcommand(name="qreport")
    async def report(self, interaction: nextcord.Interaction, *, message: str):
        """Report a bug"""
        
        data = {
            "content": f"**Bug reported!**\n\nBy: **{interaction.user.name}#{interaction.user.discriminator}**\nID: **{interaction.user.id}**\nMention: {interaction.user.mention}\nContent: {message}\n\n**{version1}**"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(self.webhook_url, json=data, headers=headers)
        if response.status_code == 204:
            embedc = nextcord.Embed(title="Bug Report", description="Thank you for reporting this bug.", color=nextcord.Color.green())
            embedc.add_field(name="", value="We will fix it as soon as possible.", inline=False)
            embedc.set_author(name=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            embedc.set_footer(text=version1)
            await interaction.send(embed=embedc)
        else:
            embedc1 = nextcord.Embed(title="Report Error", description="Error sending the message.", color=nextcord.Color.red())
            embedc1.add_field(name="", value="Please try again later.", inline=False)
            embedc1.set_author(name=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            embedc1.set_footer(text=version1)
            await interaction.send(embed=embedc1)
'''
    @main.subcommand()
    async def helps(self, interaction: nextcord.Interaction):

        embed_message = nextcord.Embed(
            title="Helps",
            description="Toutes les commandes",
            color=nextcord.Color.random()
        )

        embed_message.set_author(
            name=f"Demandé par {interaction.user.name}",
            icon_url=interaction.user.avatar
        )

        embed_message.add_field(name="helps", value="help show this message =help")
        embed_message.add_field(name="ping", value="ping the bot =ping")
        embed_message.add_field(name="version, v", value="Bot version =version",)
        embed_message.add_field(name="stop", value="stop the bot =stop (only owner)")
        embed_message.add_field(name="report", value="report only for report a bug or make a feedback =report [something to send]")
        embed_message.set_footer(text=version1)

        embed_message2 = nextcord.Embed(
            title="Helps Soundboard",
            description="Toutes les commandes de Soundboard",
            color=nextcord.Color.random()
        )

        embed_message2.set_author(
            name=f"Demandé par {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        
        embed_message2.add_field(name="slist", value="slist list all soundboard =slist 4")
        embed_message2.add_field(name="splay", value="splay make play soundboard =splay [number]")
        embed_message2.add_field(name="sjoin", value="sjoin make join bot =sjoin [need to be in a vc]")
        embed_message2.add_field(name="sleave", value="sleave make leave bot =sleave")
        embed_message2.add_field(name="sstop", value="stop bot making soundboard =sstop")
        embed_message2.add_field(name="srandom", value="srandom play a random soundboard between 1 and 5 minutes =srandom")
        embed_message2.add_field(name="srandomskip", value="skip skip random soundboard =srandomskip [only when a sound is playing]")
        embed_message2.add_field(name="srandomstop", value="stops stop random soundboard =srandomstop")
        embed_message2.add_field(name="vkick", value="vkick kick user in a vc =vkick [@ID] (admin perms only)")
        embed_message2.add_field(name="tts", value="tts make bot say something with googletts voice in vc =tts [langue] [texte]")
        
        
        embed_message3 = nextcord.Embed(
        title="Helps Leveling",
        description="Toutes les commandes de Leveling",
        color=nextcord.Color.random()
        )

        embed_message3.set_author(
            name=f"Demandé par {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        

        embed_message3.add_field(name="level, lvl", value="level see your ranking =level [@ user]")
        embed_message3.add_field(name="resetlevel, rsl", value="resetlevel reset member level =resetlevel [@ user] (messages perms only)")
        embed_message3.add_field(name="levelsettings, lvls", value="levelsettings enable or disable leveling system (admins perms only)")
        
        embed_message4 = nextcord.Embed(
        title="Helps Mods",
        description="Toutes les commandes Mods",
        color=nextcord.Color.random()
        )

        embed_message4.set_author(
            name=f"Demandé par {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        
      
        embed_message4.add_field(name="clear, prune", value="clear messages =clear [number] (messages perms only) max 70 messages")
        embed_message4.add_field(name="cleanraidsimple, clr", value="clear raid with channel name =cleanraidsimple [channel name] (messages perms only)")
        embed_message4.add_field(name="cleanraidmultiple, clrs", value="clear raid with datetime =cleanraidmultiple [Y-m-d-H:M] (messages perms only)")
        embed_message4.add_field(name="kick", value="kick members =kick [@ user or ID] (kick perms only)")
        embed_message4.add_field(name="ban", value="ban members =ban [@ user or ID] (ban perms only)")
        embed_message4.add_field(name="unban", value="unban members =unban [@ user or ID] (ban perms only)")
        
        embed_message5 = nextcord.Embed(
        title="Helps Utility",
        description="Toutes les commandes d'Utility",
        color=nextcord.Color.random()
        )

        embed_message5.set_author(
            name=f"Demandé par {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        
      
        embed_message5.add_field(name="gpt", value="use gpt in nextcord =gpt [Something to ask]")
        embed_message5.add_field(name="dalle", value="use dalle in nextcord =dalle [Something to ask]")
        embed_message5.add_field(name="spam", value="spam in chat =spam [Number of Times] [Something to say] (admin perms only)")
        embed_message5.add_field(name="repeat, say", value="Repeat messages =repeat [Something to repeat]")
        embed_message5.add_field(name="8ball, magicball", value="8ball game =8ball [Something to answer]")
        embed_message5.add_field(name="hilaire", value="hilaire game =hilaire")
        embed_message5.add_field(name="mp, dm", value="mp send mp to user =mp [@ user] (admins perms only)")
        embed_message5.add_field(name="deldms, delmp", value="deldms clear dms with bot =deldms (admin perms only)")
        
        embed_message6 = nextcord.Embed(
            title="Helps MP",
            description="Commandes disponible en MP",
            color=nextcord.Color.random()
        )

        embed_message6.set_author(
            name=f"Demandé par {interaction.user.name}",
            icon_url=interaction.user.avatar
        )

        embed_message6.add_field(name="helps", value="help show this message =help")
        embed_message6.add_field(name="ping", value="ping the bot =ping")
        embed_message6.add_field(name="version, v", value="Bot version =version",)
        embed_message6.add_field(name="stop", value="stop the bot =stop (only owner)")
        embed_message6.add_field(name="report", value="report only for report a bug or make a feedback =report [something to send]")
        embed_message6.add_field(name="gpt", value="use gpt in nextcord =gpt [Something to ask]")
        embed_message6.add_field(name="dalle", value="use dalle in nextcord =dalle [Something to ask]")
       
              
        with open("images/quantaai/png/logo-black.png", "rb") as f:
            image_data = f.read()
        embed_message6.set_thumbnail(url="attachment://logo-black.png")

        await interaction.send(embed=embed_message)
        await interaction.send(embed=embed_message4)
        await interaction.send(embed=embed_message5)
        await interaction.send(embed=embed_message2)
        await interaction.send(embed=embed_message3)
        await interaction.send(embed=embed_message6, file=nextcord.File(io.BytesIO(image_data), "logo-black.png"))
'''
def setup(bot):
    bot.add_cog(XKCD(bot))
    
    