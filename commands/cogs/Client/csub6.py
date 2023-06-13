import asyncio
import io
import aiohttp
import nextcord
from nextcord.ext import commands
import requests
import regex
import json
import utils

from utils.WF1 import Embed
from aiohttp import ClientConnectorError
from nextcord.ui import View, Button
# ! Def- Add way more sub commands (Change whole file)

class Stocks2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def fetch_stocks(self, url):
        response = requests.get(url)
        stock_data_pattern = regex.compile(r'const stocks = (\[.*?\]);', regex.DOTALL)
        match = stock_data_pattern.search(response.text)

        if match:
            stock_data_json = match.group(1)
            stock_data = json.loads(stock_data_json)
            return stock_data
        else:
            return []
    @nextcord.slash_command(name="sub6")
    async def main(self, interaction: nextcord.Interaction):
        pass
    @main.subcommand()
    async def stocks22(self, interaction: nextcord.Interaction):
        # Replace this URL with the actual URL of your JavaScript file
        url = 'https://github.com/wadder12/wadder12.github.io/blob/master/pages/stockgame.js'
        stocks = self.fetch_stocks(url)

        embed = nextcord.Embed(title="Stocks", color=nextcord.Color.green())
        for stock in stocks:
            embed.add_field(name=f"{stock['symbol']} - {stock['name']}", value=f"${stock['price']}", inline=False)

        await interaction.send(embed=embed)
        
    @main.subcommand(name="wadderadvice", description="To get advice from Wadder")
    async def advice(self, interaction: nextcord.Interaction):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://api.adviceslip.com/advice")
            data = await response.json(content_type=None)
            embed = nextcord.Embed(
                title=f"👍 Advice",
                description=data["slip"]["advice"],
                colour=nextcord.Color.blue(),
            )
            await interaction.send(embed=embed)
            
            
    @main.subcommand(name="wbored", description="To get bored")
    async def bored(self, interaction: nextcord.Interaction):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://www.boredapi.com/api/activity")
            data = await response.json(content_type=None)
            embed = nextcord.Embed(
                title=f"🥱 Bored", 
                description=data["activity"], 
                colour=nextcord.Color.blue()
            )
            embed.add_field(name="Type", value=data["type"])
            embed.add_field(name="Participants:", value=data["participants"])
            await interaction.send(embed=embed)
    
    @main.subcommand(name="wallpaper", description="To get wallpaper")        
    async def wallpaper(self, interaction: nextcord.Interaction):
        result = await utils.WF1.nsfw('wallpaper')

        embed = nextcord.Embed(title="🏞️ Wallpaper", color=interaction.user.top_role.color)
        embed.set_image(url=result["image"])
        await interaction.send(embed=embed)
        
        
        
        
    


    @main.subcommand(name="github", description="get github user") 
    async def github(self,interaction: nextcord.Interaction, username: str = None):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.github.com/users/{username}"
                response = await session.get(url)
                data = await response.json(content_type=None)

            name = data["name"]
            if not name:
                title = f"<:Github:885097226752385054> {data['login']}"
            else:
                title = f"<:Github:885097226752385054> {data['login']} ({data['name']})".replace("('", "").replace("',)", "")

            embed = nextcord.Embed(
                title=title,
                description=data["bio"],
                colour=nextcord.Color.blue(),
                url=data["html_url"],
            )

            location = data["location"]
            if not location:
                location = "Not Set"
            embed.add_field(name="📍 Location", value=location)

            embed.add_field(name="👥 Followers", value=data["followers"])
            embed.add_field(name="👤 Following", value=data["following"])
            embed.add_field(name="📚 Repos", value=data["public_repos"])
            embed.add_field(name="📝 Gists", value=data["public_gists"])

            company = data.get("company")
            if company:
                if company.startswith("@"):
                    company = (
                        f"[{company}](https://github.com/{company.replace('@','')})"
                    )
                embed.add_field(name="🏢 Company", value=company)

            email = data.get("email")
            if not email:
                email = "No Data"
            embed.add_field(name="📧 Email", value=email)
            embed.add_field(name="📅 Created On", value=data["created_at"].split("T")[0])
            embed.add_field(name="📅 Last Update", value=data["updated_at"].split("T")[0])
            embed.set_thumbnail(url=data["avatar_url"])

            button = nextcord.ui.View()
            button.add_item(
                item=Button(
                    emoji="<:Github:885097226752385054>",
                    label=f" {data['login']}",
                    url=data["html_url"],
                )
            )

            twitter = data.get("twitter_username")
            if twitter:
                button.add_item(
                    item=Button(
                        emoji="<:Twitter:885114838727151616>",
                        label=data["twitter_username"],
                        url=f"https://twitter.com/{twitter}",
                    )
                )

            await interaction.send(embed=embed, view=button)

        except KeyError:
            embed = nextcord.Embed(
                title=f"<:oh:881566351783780352> Data Not Found",
                colour=nextcord.Color.red(),
                description=f"{interaction.user.mention} I don't seem to find data for `{username}`",
            )
            embed.set_footer(text=f"Join My Server For Additional Help!")
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
            await interaction.send(embed=embed)

        except:
            raise    
        
    @main.subcommand(name="pypi", description="To get info about a python module")     
    async def pypi(self, interaction: nextcord.Interaction, module: str = None):
        with open("data/MediaData.json") as f:
            data = json.load(f)
            gif = data["pypi"]
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://pypi.org/pypi/{module}/json"
                response = await session.get(url)
                data = await response.json(content_type=None)
                pkg = data["info"]

            embed = nextcord.Embed(
                title=f"<:pypi:884892626099265587> {pkg['name']}",
                url=pkg["package_url"],
                description=pkg["summary"],
                colour=nextcord.Color.blue(),
            )

            author = pkg.get("author")
            if author:
                embed.add_field(name="🧑‍💻 Author", value=pkg["author"], inline=False)

            embed.add_field(
                name="🕔 Latest Release",
                value=f"[{pkg['version']}]({pkg['release_url']})",
            )

            keyword = pkg["keywords"]
            if not keyword:
                keyword = "No Data"
            embed.add_field(name="📃 Keywords", value=keyword, inline=False)

            embed.set_thumbnail(url=gif)
            button = nextcord.ui.View()

            urls = pkg.get("project_urls")
            if urls:
                for i in pkg["project_urls"].items():
                    Link = Button(label=f"{i[0]}", url=f"{i[1]}")
                    button.add_item(Link)

            await interaction.send(embed=embed, view=button)

        except json.JSONDecodeError:
            embed = await Embed.datanotfound(self, interaction)
            await interaction.send(embed=embed)

        except:
            raise    
        
        
    @main.subcommand(name="voicechannel", description="To get info about a voice channel")
    async def voicechannelinfo(self, interaction: nextcord.Interaction, *, channel: nextcord.VoiceChannel = None):
        try:
            channel = channel or interaction.author.voice.channel
            if not channel.user_limit:
                channel.user_limit = "Infinite"

            # Define the computer animation frames
            animation = [
                "```ini\n[Gathering channel information...     ]```",
                "```ini\n[Gathering channel information...•    ]```",
                "```ini\n[Gathering channel information...••   ]```",
                "```ini\n[Gathering channel information...•••  ]```",
                "```ini\n[Gathering channel information...•••• ]```",
                "```ini\n[Gathering channel information...•••••]```",
                "```ini\n[Gathering channel information... ••••]```",
                "```ini\n[Gathering channel information...  •••]```",
                "```ini\n[Gathering channel information...   ••]```",
                "```ini\n[Gathering channel information...    •]```",
                "```ini\n[Gathering channel information...     ]```",
                "```ini\n[Gathering channel information...    ]```",
                "```ini\n[Gathering channel information...•   ]```",
                "```ini\n[Gathering channel information...••  ]```",
                "```ini\n[Gathering channel information...••• ]```",
                "```ini\n[Gathering channel information...••••]```",
                "```ini\n[Gathering channel information...•••••]```",
                "```ini\n[Gathering channel information...•••• ]```",
                "```ini\n[Gathering channel information...•••  ]```",
                "```ini\n[Gathering channel information...••   ]```",
                "```ini\n[Gathering channel information...•    ]```",
            ]

            # Send the initial loading message
            loading_message = await interaction.response.send_message(animation[0])

            # Animate the loading message
            for frame in animation:
                await loading_message.edit(content=frame)
                await asyncio.sleep(0.5)

            # Create the embed
            embed = nextcord.Embed(
                title=f"{channel.name} Info",
                description=f"Here is some info about {channel.mention}\n"
                            f":id:**Channel ID:** `{channel.id}`\n🌀**Channel Type:** {channel.type}",
                colour=nextcord.Color.blue(),
            )
            embed.add_field(name=f"📰 Name", value=f"{channel.name}")
            embed.add_field(name=f"📃 Category", value=f"{channel.category}")
            embed.add_field(
                name=f"🔉 Audio Bitrate", value=f"{round((channel.bitrate)/1000)} Kilo"
            )
            embed.add_field(name=f"🔢 Channel Position", value=f"{channel.position+1}")
            embed.add_field(name=f"👤 Member Limit", value=f"{channel.user_limit}")
            date = channel.created_at.timestamp()
            embed.add_field(name=f"📆 Created On", value=f"<t:{round(date)}:D>")

            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon)

            # Update the loading message with the channel information embed
            await loading_message.edit(content="Channel Information", embed=embed)

        except AttributeError:
            embed = await Embed.missingrequiredargument(self, interaction)
            await interaction.send(embed=embed)

    
    @main.subcommand(name="textchannelinfo", description="To get info about a text channel")
    async def textchannelinfo(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel

        # Define the computer animation frames
        animation = [
            "```ini\n[Gathering channel information...     ]```",
            "```ini\n[Gathering channel information...•    ]```",
            "```ini\n[Gathering channel information...••   ]```",
            "```ini\n[Gathering channel information...•••  ]```",
            "```ini\n[Gathering channel information...•••• ]```",
            "```ini\n[Gathering channel information...•••••]```",
            "```ini\n[Gathering channel information... ••••]```",
            "```ini\n[Gathering channel information...  •••]```",
            "```ini\n[Gathering channel information...   ••]```",
            "```ini\n[Gathering channel information...    •]```",
            "```ini\n[Gathering channel information...     ]```",
            "```ini\n[Gathering channel information...    ]```",
            "```ini\n[Gathering channel information...•   ]```",
            "```ini\n[Gathering channel information...••  ]```",
            "```ini\n[Gathering channel information...••• ]```",
            "```ini\n[Gathering channel information...••••]```",
            "```ini\n[Gathering channel information...•••••]```",
            "```ini\n[Gathering channel information...•••• ]```",
            "```ini\n[Gathering channel information...•••  ]```",
            "```ini\n[Gathering channel information...••   ]```",
            "```ini\n[Gathering channel information...•    ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Create the embed
        embed = nextcord.Embed(
            title=f"{str(channel.name).title()} Info",
            description=f"Here is some info about {channel.mention}\n"
                        f":id:**Channel ID:** `{channel.id}`\n🌀**Channel Type:** {channel.type}",
            colour=nextcord.Color.blue(),
        )
        embed.add_field(name=f"📰 Name", value=f"{channel.name}")
        embed.add_field(name=f"📃 Category", value=f"{channel.category}")
        embed.add_field(name=f"📜 Topic", value=f"{channel.topic}")
        embed.add_field(name=f"🔢 Position", value=f"{channel.position + 1}")
        embed.add_field(name=f"⌛ Slowmode", value=f"{channel.slowmode_delay} seconds")
        embed.add_field(name=f"👤 Members", value=f"{len(channel.members)}")
        embed.add_field(name=f"🔞 NSFW", value=f"{channel.is_nsfw()}")
        date = channel.created_at.timestamp()
        embed.add_field(name=f"📆 Created On", value=f"<t:{round(date)}:D>")

        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon)

        # Update the loading message with the channel information embed
        await loading_message.edit(content="Channel Information", embed=embed)

    
  
## ** /wpoller "What is your favorite color?" "Red" "Green" "Blue"
##**               question                        options
    
    @main.subcommand(name="wpoller", description="To create a poll wip") 
    async def wpoll(self, interaction: nextcord.Interaction, question: str = None, options: str = None, required=False, default=0):
        if len(options) == 0:
            embed = nextcord.Embed(title=question, colour=nextcord.Color.blue())
            message = await interaction.respond(embed=embed)

            # await message.delete()
            await message.add_reaction("🔼")
            await message.add_reaction("🔽")
            return

        elif len(options) <= 1:
            embed = await utils.WF1.Embed.missingrequiredargument(self, interaction)
            await interaction.send(embed=embed)
            return

        elif len(options) > 10:
            embed = nextcord.Embed(
                title=f"<:oh:881566351783780352> Excessive Required Argument",
                colour=nextcord.Color.red(),
                description=f"*You can have upto **10 options only**"
                f'\n\nCorrect Usage: `/ poll "[question]" "(options)"*`',
            )
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
            embed.set_footer(text=f"Join My Server For Additional Help!")
            await interaction.send(embed=embed)
            return

        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ["🔼", "🔽"]
        else:
            reactions = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

        description = []
        for x, option in enumerate(options):
            description += "\n {} {}".format(reactions[x], option)

        embed = nextcord.Embed(
            title=question, colour=nextcord.Color.blue(), description="".join(description)
        )
        message = await interaction.response.send_message(embed=embed, fetch=True)

        # Add reactions to the message
        for reaction in reactions[: len(options)]:
            await message.add_reaction(reaction)

    @main.subcommand(name="wembed", description="To create an embed wip") 
    async def wembed(self, interaction: nextcord.Interaction, *, message: str = None):
        # Define the computer animation frames
        animation = [
            "```md\n# Creating embed... [     ]```",
            "```md\n# Creating embed... [•    ]```",
            "```md\n# Creating embed... [••   ]```",
            "```md\n# Creating embed... [•••  ]```",
            "```md\n# Creating embed... [•••• ]```",
            "```md\n# Creating embed... [•••••]```",
            "```md\n# Creating embed... [ ••••]```",
            "```md\n# Creating embed... [  •••]```",
            "```md\n# Creating embed... [   ••]```",
            "```md\n# Creating embed... [    •]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:] + animation[::-1]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.3)

        # Create the embed
        embed = nextcord.Embed(title="Custom Embed", color=nextcord.Color.blue())
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.description = message if message else "No message provided."

        # Add a timestamp
        embed.timestamp = nextcord.utils.utcnow()

        # Add a footer
        embed.set_footer(text="Embed created by QuantaAI", icon_url="http://wadderprojects.bhweb.ws/assets/images/logo/logo-no-background.png")

        # Send the embed
        await loading_message.edit(content="Embed Created", embed=embed)

    
    @main.subcommand(name="addemoji", description="To add an emoji to the server wip")  #! Unhandled application command error: Command raised an exception: InvalidArgument: Unsupported image type given
    async def addemoji(self,  interaction: nextcord.Interaction, emojiurl: str = None , name:  str = None, required=True, default=None):
        try:
            if emojiurl.startswith("https:"):

                response = requests.get(emojiurl)
                emojis = await interaction.guild.create_custom_emoji(
                    name=name, image=response.content
                )
                emoji = self.bot.get_emoji(emojis.id)

                if emoji.animated:
                    description = f"{interaction.user.mention} Added emoji:\n`<a:{emoji.name}:{emoji.id}>`"
                else:
                    description = f"{interaction.user.mention} Added emoji:\n`<:{emoji.name}:{emoji.id}>`"

                embed = nextcord.Embed(
                    title=f"New Emoji Added!",
                    description=description,
                    colour=nextcord.Color.blue(),
                )
                embed.set_image(url=emoji.url)
                await interaction.send(embed=embed)

            else:
                emoid = (emojiurl)[-19:-1]

                if "a" in emojiurl:
                    link = f"https://cdn.nextcordapp.com/emojis/{emoid}.gif?v=1"
                else:
                    link = f"https://cdn.nextcordapp.com/emojis/{emoid}.png?v=1"

                emoji = await interaction.guild.create_custom_emoji(name=name, image=link)
                emoji = self.bot.get_emoji(emoid)

                embed = nextcord.Embed(
                    title=f"New Emoji Added!",
                    description=f"{interaction.user.mention} Added New Emoji!",
                    colour=nextcord.Color.blue(),
                )
                embed.set_image(url=emoji.url)
                await interaction.send(embed=embed)
                await interaction.send(link)

        except TypeError:
            embed = await Embed.datanotfound(self, interaction)
            await interaction.send(embed=embed)
    
    
    @main.subcommand(name="wroleinfo", description="To get info about a role wip")
    async def roleinfo(self, interaction: nextcord.Interaction, role: nextcord.Role = None):
        role = role or interaction.user.top_role

        # Define the computer animation frames
        animation = [
            "```diff\n- Gathering role information...```",
            "```diff\n+ Gathering role information...```",
            "```diff\n- Gathering role information...```",
            "```diff\n+ Gathering role information...```",
            "```diff\n- Gathering role information...```",
            "```diff\n+ Gathering role information...```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:] + animation[::-1]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        embed = nextcord.Embed(
            title=f"{role.name} Info",
            description=f"Here is some info about {role.mention}"
            f"\n:id: **Role ID:** `{role.id}`",
            colour=nextcord.Color.blue(),
        )

        embed.add_field(name=f"✏ Name", value=f"{role.name}")
        embed.add_field(name=f"🔢 Position", value=f"{role.position}")
        embed.add_field(name=f"❄ Role Color", value=f"{role.color}")
        embed.add_field(name=f"🔶 Displayed Separately", value=f"{role.hoist}")
        embed.add_field(name=f"👥 Members", value=f"{len(role.members)}")
        embed.add_field(name=f"🎩 Mentionable", value=f"{role.mentionable}")

        perm_list = (", ".join([perm[0] for perm in role.permissions if perm[1]]).title().replace("_", " "))
        
        if "Administrator" in perm_list:
            perm_list = "**Administrator**"
        if not perm_list:
            perm_list = "None"
        embed.add_field(name="Permissions", value=perm_list, inline=False)

        date = role.created_at.timestamp()
        embed.add_field(name=f"📆 Created On", value=f"<t:{round(date)}:D>")
        
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon)

        # Update the loading message with the role information embed
        await loading_message.edit(content="Role Information", embed=embed)

    
    
    
    
    
    
    
def setup(bot):
    bot.add_cog(Stocks2(bot))


