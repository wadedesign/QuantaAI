import asyncio
import random
from typing import Union
import nextcord
from random import choice
from nextcord.ext import commands
from simpcalc import simpcalc
from nextcord.utils import escape_markdown
from utils.WF0 import random
from utils.WF2.WadderEmbeder import error_embed, success_embed, meh_embed
from utils.WF0.random import email_fun, passwords, DMs, nextcord_servers
from utils.WF2.WadderConfigs import (
    DAGPI_KEY, DEFAULT_BANNED_WORDS, EMOJIS, MAIN_COLOR, BIG_PP_GANG, NO_PP_GANG,
    RED_COLOR, ORANGE_COLOR, PINK_COLOR, CHAT_BID,
    CHAT_API_KEY, PINK_COLOR_2, THINKING_EMOJI_URLS, WEBSITE_LINK, INVISIBLE_COLOR, BADGE_EMOJIS, EMOJIS, RED_COLOR
)
import random
from humanfriendly import format_timespan
from owotext import OwO
from utils.WF2.WadderMessage import wait_for_msg


## Not sure I need this anymore
uwu = OwO()
async def edit_msg_multiple_times(interaction, time_, first_msg, other_msgs, final_emb):
        msg = await interaction.send(embed=nextcord.Embed(title=first_msg, color=MAIN_COLOR))
        await asyncio.sleep(time_)

        for e in other_msgs:
            embed = nextcord.Embed(title=e[0], color=MAIN_COLOR)
            if len(e) == 2:
                embed.description = e[1]
            await msg.edit(embed=embed)
            await asyncio.sleep(time_)

        await msg.edit(embed=final_emb)

PREFIX = "e!"
MAIN_COLOR = 0x459fff  # light blue kinda
RED_COLOR = 0xFF0000
ORANGE_COLOR = 0xFFA500
PINK_COLOR = 0xe0b3c7
PINK_COLOR_2 = 0xFFC0CB
STARBOARD_COLOR = 15655584
INVISIBLE_COLOR = 0x36393F
WEBSITE_LINK = "http://wadderprojects.bhweb.ws/"

class InteractiveView(nextcord.ui.View):
    def __init__(self, interaction: commands.Context):
        super().__init__(timeout=None)
        self.expr = ""
        self.calc = simpcalc.Calculate()
        self.interaction = interaction

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "1"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "2"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "3"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="➕", row=0)
    async def plus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "+"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "4"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "5"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "6"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="➗", row=1)
    async def divide(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "/"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "7"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "8"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "9"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="✖️", row=2)
    async def multiply(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "*"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "."
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "0"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except:
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "-"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "("
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += ")"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="AC", row=4)
    async def clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr = ""
        await interaction.message.edit(content=f"```\n> {self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="BACK", row=4)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr = self.expr[:-1]
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

class FreeNitroView(nextcord.ui.View):
    def __init__(self, interaction: commands.Context):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.value = None


    @nextcord.ui.button(label="Claim", custom_id='claim', style=nextcord.ButtonStyle.green)
    async def claim(self, _, interaction: nextcord.Interaction):
        await interaction.message.edit(content="https://imgur.com/NQinKJB", embed=None, view=None)





class WadderUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 1
        self.tickets = {}
        
        
    
    @nextcord.slash_command(name="wadderutils")
    async def main(self, interaction: nextcord.Interaction):
        pass
    
    @main.subcommand(description="Calculate a math expression")
    async def waddercal(self, interaction: nextcord.Interaction):
         view = InteractiveView(interaction)
         await interaction.send("```py\n> ```",view=view)

    @main.subcommand()
    async def nitro(self, interaction: nextcord.Interaction):
        view = FreeNitroView(interaction)
        time_to_fool_u = nextcord.Embed(
            title="Congratulations! You've unlocked Nitro+!",
            description="Enjoy the benefits of Nitro+ subscription for **1 Month!**\nExpires in **24 hours**\n\n[**Disclaimer**]({WEBSITE_LINK}/disclaimer)",
            color=0xFF00FF  # Set a cool purple color for the embed
        ).set_image(url="https://media.nextcordapp.net/attachments/895163964361674752/895982514093555763/images_1_-_2021-10-08T160355.540.jpeg")  # Display a larger image
        await interaction.send(embed=time_to_fool_u, view=view)


    @main.subcommand(name="whenyoudie", description="See when you're gonna die")
    async def whendie(self, interaction: nextcord.Interaction, *, user: nextcord.Member = None):
        if user is None:
            user = interaction.user

        msg = await interaction.response.send_message(embed=nextcord.Embed(title="Let's see when you're gonna die...", color=MAIN_COLOR))

        something = [
            f'{random.randint(0, 60)} Second(s)',
            f'{random.randint(1, 60)} Minute(s)',
            f'{random.randint(1, 24)} Hour(s)',
            f'{random.randint(1, 7)} Day(s)',
            f'{random.randint(1, 4)} Week(s)',
            f'{random.randint(1, 100)} Year(s)'
        ]

        thingy = random.choice(something)

        if thingy == something[0]:
            funny_text = "LOL YOU'RE DEAD"
            embed_color = RED_COLOR
        if thingy == something[1]:
            funny_text = "Well rip, you're almost dead"
            embed_color = RED_COLOR
        if thingy == something[2]:
            funny_text = "Sad"
            embed_color = RED_COLOR
        if thingy == something[3]:
            funny_text = "Ok you have some time before you die"
            embed_color = ORANGE_COLOR
        if thingy == something[4]:
            funny_text = "You're not dying that early, Yay!"
            embed_color = ORANGE_COLOR
        if thingy == something[5]:
            funny_text = "Wowie, you have a nice long life! OwO"
            embed_color = MAIN_COLOR

        embed = nextcord.Embed(
            description=f"**{escape_markdown(str(user))}** is gonna die in **{thingy}**",
            color=embed_color,
        )
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=funny_text)

        await msg.edit(embed=embed)
        
        
    @main.subcommand()
    async def aesthetic(self, interaction: nextcord.Interaction, *, args=None):
        if args is None:
            interaction.command.reset_cooldown(interaction)
            return await interaction.response.send_message(embed=("Invalid args", f"Correct usage: `{PREFIX}atc <msg> | [mode]`.\nMode can be `b` (bold), `i` (italic), or `n` (none).\n\nExample: `{PREFIX}atc uwu | n`\nOutput: `u w u`"))

        if args.count(" | ") == 0:
            m = "n"
        else:
            m = args[-1]

        s = ""
        s += "**" if m == "b" else ("_" if m == "i" else "")

        msg = args.split(" | ")[0]
        args = args.split(" | ")[:-1]
        for c in msg:
            s += c + " "
        s += "**" if m == "b" else ("_" if m == "i" else "")

        await interaction.response.send_message(s)
        
    @main.subcommand()
    async def hack(self, interaction: nextcord.Interaction, user: nextcord.Member = None):
        if user is None:
            embed = nextcord.Embed(title="Bruh!", description="Please mention who do you want to hack next time!", color=0xFF0000)
            return await interaction.response.send_message(embed=embed)

        if user == interaction.user:
            embed = nextcord.Embed(title="Bruh!", description="Don't hack yourself idiot!", color=0xFF0000)
            return await interaction.response.send_message(embed=embed)
        if user.bot:
            embed = nextcord.Embed(title="Bruh!", description="You can't hack bots.\nThey are way too powerful!", color=0xFF0000)
            return await interaction.response.send_message(embed=embed)


        email_username = ""
        for e in user.name:
            if e == " ":
                e = "_"
            email_username += e.lower()
        email_address = f"{email_username}{random.choice(email_fun).lower()}@gmail.com"
        password = random.choice(passwords)
        latest_dm = random.choice(DMs)
        most_used_nextcord_server = random.choice(nextcord_servers)

        uwu_lmao = nextcord.Embed(
            title=f"{escape_markdown(str(user.name))}'s Data {EMOJIS['hacker_pepe']}",
            description=f"""
**Email:** `{email_address}`
**Password:** `{password}`
**Most Used nextcord Server:** `{most_used_nextcord_server}`
**Latest DM:** `{latest_dm}`
            """,
            color=MAIN_COLOR
        )

        await edit_msg_multiple_times(
            interaction, 1, f"Initializing `hack.exe` {EMOJIS['hacker_pepe']}",
            [
                [f"Successfully initialized `hack.exe`, beginning hacks... {EMOJIS['loading']}"],
                [f"Logging into {user.name}'s nextcord Account... {EMOJIS['loading']}"],
                [f"Successfully Logged in! {EMOJIS['tick_yes']}", f"**Email Address:** `{email_address}`\n**Password:** `{password}`"],
                [f"Fetching DMs from friends (if there are any)... {EMOJIS['loading']}"],
                [f"Latest DM from {user.name}", latest_dm],
                [f"Fetching the most used nextcord server... {EMOJIS['loading']}"],
                [f"Most used nextcord server found {EMOJIS['tick_yes']}", most_used_nextcord_server],
                [f"Selling data... {EMOJIS['loading']}"]
            ],
            uwu_lmao
        )
        
    @main.subcommand()
    async def owo(self, interaction: nextcord.Interaction, *, message=None):
        if message is None:
            message = "Hi! you need to enter a message to owoify it!"
            return await interaction.response.send_message(uwu.whatsthis(message))

        await interaction.send(uwu.whatsthis(message))
        
        
        
        
    
def setup(bot):
    bot.add_cog(WadderUtils(bot))