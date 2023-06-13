import json
import random
import nextcord
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from utils.WF0.errors import print_error
from utils.WF0.functions import format_name, get_random_color, load_json, split_by_slice, get_custom_emoji2
from utils.WF0.paginator import Paginator
import io
import typing
from asyncdagpi import Client as AsyncD

import asyncdagpi
import asyncio
import datetime
import functools
import json
import os
import pprint
import random
import re
from operator import attrgetter
from typing import Any, AnyStr, Callable, Coroutine, Dict, Iterable, List, Union

import nextcord
import numpy as np
import rich
from nextcord.ext import commands
from rich.console import Console
from rich.syntax import Syntax



VALID_JSON_TYPES = Union[str, int, bool, list, dict, None]

# !Add more sub commands (Change whole file)

def is_image(url: str) -> bool:
    """If a image is a valid image or not.

    Examples
    ________
    >>> url = "https://i.imgur.com/a/MzgxNjI.jpg"
    >>> is_image(url)
    True
    >>> url = "https://www.google.com"
    >>> is_image(url)
    False

    Parameters
    ----------
    url : str
        The url to validate

    Returns
    -------
    bool
        The image is a valid image or not
    """
    # We cast it to bool just to make sure that it is True/False
    return bool(re.match(r"(https?:\/\/.*\.(?:png|jpg))", url))

async def get_image(
    interaction: nextcord.Interaction,
    item: Union[nextcord.Member, nextcord.Emoji, nextcord.PartialEmoji, None, str] = None,
):
    if isinstance(item, str) and not is_image(item):
        item = f"https://twemoji.maxcdn.com/v/latest/72x72/{ord(item):x}.png"
        if (await interaction.bot.session.get(item)).status == 200:
            return item

    if isinstance(item, nextcord.Member):
        return str(item.avatar.with_format("png"))

    elif isinstance(item, str):
        if is_image(item):
            return item

    if hasattr(item, "url"):
        return item.url

    if item is None:
        return str(interaction.user.avatar.with_format("png"))




class ServerEmojisCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.claptraps = load_json("data/claptraps.json")

    def get_custom_emoji2(bot, name):
        for guild in bot.guilds:
            for emoji in guild.emojis:
                if emoji.name == name:
                    return emoji
        return None


    async def send_long_message(self, interaction, content, max_length=2000):
        if len(content) <= max_length:
            await interaction.response.send_message(content)
        else:
            parts = [content[i:i + max_length] for i in range(0, len(content), max_length)]
            for i, part in enumerate(parts):
                if i == 0:
                    await interaction.response.send_message(part)
                else:
                    await interaction.followup.send(part)

    @nextcord.slash_command(name="sub2")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="qemojis", description="get emoji from server")
    async def list_emojis(self, interaction: nextcord.Interaction):
        """List all emojis available on the server."""
        # Define the computer animation frames
        animation = [
            "```yaml\n[Listing emojis...     ]```",
            "```yaml\n[Listing emojis...•    ]```",
            "```yaml\n[Listing emojis...••   ]```",
            "```yaml\n[Listing emojis...•••  ]```",
            "```yaml\n[Listing emojis...•••• ]```",
            "```yaml\n[Listing emojis...•••••]```",
            "```yaml\n[Listing emojis... ••••]```",
            "```yaml\n[Listing emojis...  •••]```",
            "```yaml\n[Listing emojis...   ••]```",
            "```yaml\n[Listing emojis...    •]```",
            "```yaml\n[Listing emojis...     ]```",
            "```yaml\n[Listing emojis...    ]```",
            "```yaml\n[Listing emojis...•   ]```",
            "```yaml\n[Listing emojis...••  ]```",
            "```yaml\n[Listing emojis...••• ]```",
            "```yaml\n[Listing emojis...••••]```",
            "```yaml\n[Listing emojis...•••••]```",
            "```yaml\n[Listing emojis...•••• ]```",
            "```yaml\n[Listing emojis...•••  ]```",
            "```yaml\n[Listing emojis...••   ]```",
            "```yaml\n[Listing emojis...•    ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        emojis = interaction.guild.emojis
        if emojis:
            emoji_list = "\n".join([f"{emoji.name}: {emoji}" for emoji in emojis])
            await self.send_long_message(interaction, f"Emojis on this server:\n{emoji_list}")
        else:
            await loading_message.edit(content="There are no emojis on this server.")


    @main.subcommand(name="wanted", description="Wanted poster")
    async def wanted(self,interaction: nextcord.Interaction, user: nextcord.Member = None):
        if user == None:
            user = interaction.user
        file_path = os.path.abspath("images/wanted.jpg")
        wanted = Image.open(file_path)
        
        data = BytesIO(await user.display_avatar.read())
        pfp = Image.open(data)
        pfp = pfp.resize((177, 177))
        wanted.paste(pfp, (73, 235))
        wanted.save("profile.jpg")
        await interaction.send(file=nextcord.File("profile.jpg"))
        
    @main.subcommand(name="claptrap", description="Claptrap quotes")
    async def claptrap(self, interaction: nextcord.Interaction):
        # Define the computer animation frames
        animation = [
            "```yaml\n[Generating Claptrap quote...     ]```",
            "```yaml\n[Generating Claptrap quote...•    ]```",
            "```yaml\n[Generating Claptrap quote...••   ]```",
            "```yaml\n[Generating Claptrap quote...•••  ]```",
            "```yaml\n[Generating Claptrap quote...•••• ]```",
            "```yaml\n[Generating Claptrap quote...•••••]```",
            "```yaml\n[Generating Claptrap quote... ••••]```",
            "```yaml\n[Generating Claptrap quote...  •••]```",
            "```yaml\n[Generating Claptrap quote...   ••]```",
            "```yaml\n[Generating Claptrap quote...    •]```",
            "```yaml\n[Generating Claptrap quote...     ]```",
            "```yaml\n[Generating Claptrap quote...    ]```",
            "```yaml\n[Generating Claptrap quote...•   ]```",
            "```yaml\n[Generating Claptrap quote...••  ]```",
            "```yaml\n[Generating Claptrap quote...••• ]```",
            "```yaml\n[Generating Claptrap quote...••••]```",
            "```yaml\n[Generating Claptrap quote...•••••]```",
            "```yaml\n[Generating Claptrap quote...•••• ]```",
            "```yaml\n[Generating Claptrap quote...•••  ]```",
            "```yaml\n[Generating Claptrap quote...••   ]```",
            "```yaml\n[Generating Claptrap quote...•    ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        if not isinstance(self.claptraps, list):
            print_error("The [yellow]claptraps.json[/] file is not a list.")
            return await loading_message.edit(content="An error occurred. Check the console for more information.")

        # Update the loading message with a random Claptrap quote
        await loading_message.edit(content=random.choice(self.claptraps))

        
    @main.subcommand()
    async def boosters(self, interaction: nextcord.Interaction):
        """Sends all the boosters of this server"""
        people_who_boosted = sorted(interaction.guild.premium_subscribers, key=lambda member: member.joined_at)

        if not people_who_boosted:
            await interaction.response.send_message("There are no boosters in this server.")
            return

        peoples = commands.Paginator(max_size=500, prefix="```ini\n", suffix="```")
        for n, i in enumerate(people_who_boosted):
            peoples.add_line(f"[{n}] {i.name} ID: [{i.id}]")

        for page in peoples.pages:
            embed = nextcord.Embed(title=f"{len(people_who_boosted)} Boosters", description=page)
            await interaction.response.send_message(embed=embed)
            
            
    @main.subcommand()
    async def memberlist(self, interaction: nextcord.Interaction):
        """See all the members of this server sorted by their top role"""
        people = sorted(interaction.guild.members, key=lambda member: member.top_role, reverse=True)

        peoples = commands.Paginator(max_size=500, prefix="```ini\n", suffix="```")
        for num, i in enumerate(people, 1):
            peoples.add_line(f"[{num}] {i.name}\n    [ID] {i.id} [TOP ROLE] {i.top_role.name}")

        embeds = []
        for page in peoples.pages:
            embeds.append(nextcord.Embed(title=f"{len(people)} Members", description=page))

        paginator = Paginator(embeds)
        await paginator.send_initial_message(interaction, interaction.channel)
        
    @main.subcommand()
    async def firstjoins(self, interaction: nextcord.Interaction):
        """See all the members of this server sorted by their join time"""
        embeds = []
        people = sorted(interaction.guild.members, key=lambda member: member.joined_at)

        for chunk in split_by_slice(people, 5):
            embed = nextcord.Embed()
            for people in chunk:
                embed.add_field(
                    name=f"{people.name} (ID: {people.id})",
                    value=f'Created at: {nextcord.utils.format_dt(people.created_at, "F")} ({nextcord.utils.format_dt(people.created_at, "R")})\n'
                    f'Joined at: {nextcord.utils.format_dt(people.joined_at, "F")} ({nextcord.utils.format_dt(people.joined_at, "R")})',
                    inline=False,
                )
            embeds.append(embed)

        paginator = Paginator(embeds)
        await paginator.send_initial_message(interaction, interaction.channel)
        
        
        
    @main.subcommand()
    async def newjoins(self, interaction: nextcord.Interaction): #! member has no len()
        """See the newest members of this server"""
        people = sorted(interaction.guild.members, key=lambda member: member.joined_at, reverse=True)

        embeds = []
        for chunk in split_by_slice(people, 5):
            embed = nextcord.Embed(title=f"{len(people)} Members")
            for people in chunk:
                embed.add_field(
                    name=f"{people.name} (ID: {people.id})",
                    value=f'Created at: {nextcord.utils.format_dt(people.created_at, "F")} ({nextcord.utils.format_dt(people.created_at, "R")})\n'
                    f'Joined at: {nextcord.utils.format_dt(people.joined_at, "F")} ({nextcord.utils.format_dt(people.joined_at, "R")})',
                )
            embeds.append(embed)

        paginator = Paginator(embeds)
        await paginator.send_initial_message(interaction, interaction.channel)

    @main.subcommand()
    async def bots(self, interaction: nextcord.Interaction):
        """See all the bots in this server sorted by their join date"""
        people = filter(lambda member: member.bot, interaction.guild.members)
        people = sorted(people, key=lambda member: member.joined_at)

        peoples = commands.Paginator(max_size=500, prefix="```ini\n", suffix="```")
        for n, i in enumerate(people, 1):
            peoples.add_line(f"[{n}] {i.name} [ID] {i.id}")

        embeds = []
        for page in peoples.pages:
            embeds.append(nextcord.Embed(title=f"{len(people)} Bots", description=page))

        paginator = Paginator(embeds)
        await paginator.send_initial_message(interaction, interaction.channel)
        
        
    @main.subcommand()
    async def wserverinfo(self, interaction: nextcord.Interaction):
        """See the information of the current server"""
        guild = interaction.guild
        guild_owner = self.bot.get_user(guild.owner_id)

        features = "\n".join(format_name(f) for f in guild.features)

        server_boost_level = get_custom_emoji2(self.bot, 'server.boost_level')
        server_boosts = get_custom_emoji2(self.bot, 'server.boosts')
        server_boosters = get_custom_emoji2(self.bot, 'server.boosters')
        server_text_channel = get_custom_emoji2(self.bot, 'server.text_channel')
        server_voice_channel = get_custom_emoji2(self.bot, 'server.voice_channel')
        server_category_channel = get_custom_emoji2(self.bot, 'server.category_channel')

        embed = nextcord.Embed(
            title=f"Server Information for {guild.name}",
            description=(
                f"Name: {guild.name}\n"
                f"Created At: {nextcord.utils.format_dt(guild.created_at, 'F')} ({nextcord.utils.format_dt(guild.created_at, 'R')})"
                f"ID: {guild.id}\nOwner: {guild_owner}\n"
                f"Icon Url: [click here]({guild.icon.url})\n"
                f"Region: {str(guild.region)}\n"
                f"Verification Level: {str(guild.verification_level)}\n"
                f"Members: {len(guild.members)}\n"
                f"{server_boost_level} Boost Level: {guild.premium_tier}\n"
                f"{server_boosts} Boosts: {guild.premium_subscription_count}\n"
                f"{server_boosters} Boosters: {len(guild.premium_subscribers)}\n"
                f"Total Channels: {len(guild.channels)}\n"
                f"{server_text_channel} Text Channels: {len(guild.text_channels)}\n"
                f"{server_voice_channel} Voice Channels: {len(guild.voice_channels)}\n"
                f"{server_category_channel} Categories: {len(guild.categories)}\n"
                f"Roles: {len(guild.roles)}\n"
                f"Emojis: {len(guild.emojis)}/{guild.emoji_limit}\n"
                f"Upload Limit: {round(guild.filesize_limit / 1048576)} Megabytes (MB)\n"
                f"**Features:** {features}"
            ),
        )
        embed.set_thumbnail(url=guild.icon.url)
        await interaction.send(embed=embed)
        
    @main.subcommand()
    async def fox(self, interaction: nextcord.Interaction):
        "Sends a random high quality fox picture"
        url = "https://randomfox.ca/floof/"

        async with self.bot.session.get(url) as response:
            parsed_json = await response.json()
        img_url = parsed_json["image"]
        await interaction.send(embed=nextcord.Embed(title="Heres a fox picture").set_image(url=img_url))
        
    @main.subcommand()
    async def truthordare(self, interaction: nextcord.Interaction, questype: str = "random"):
        levels = ["Disgusting", "Stupid", "Normal", "Soft", "Sexy", "Hot"]

        async with self.bot.session.get(
            "https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json"
        ) as r:
            fj = json.loads(await r.text())

        if questype == "random":
            number = random.randint(0, 553)
            picked = fj[number]
            level = levels[int(picked["level"])]
            summary = picked["summary"]
            questiontype = picked["type"]
        else:
            return
        embed = nextcord.Embed(color=0x2F3136)
        embed.set_author(name=summary)
        embed.add_field(name="Level", value=level)
        embed.add_field(name="Type", value=questiontype)
        await interaction.send(embed=embed)
        
    





def setup(bot):
    bot.add_cog(ServerEmojisCog(bot))
