import nextcord
import json
import asyncio
import datetime
import time
import random
from nextcord.ext import commands, tasks
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
giveaways_collection = db["giveaways"]

def convert(date):
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    i = {"s": "Secondes", "m": "Minutes", "h": "Heures", "d": "Jours"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])
    except:
        return -2
    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]


async def stop_giveaway(bot, g_id, data):
    channel = bot.get_channel(data["channel_id"])
    giveaway_message = await channel.fetch_message(int(g_id))
    users = await giveaway_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    if len(users) < data["winners"]:
        winners_number = len(users)
    else:
        winners_number = data["winners"]

    winners = random.sample(users, winners_number)
    users_mention = []
    for user in winners:
        users_mention.append(user.mention)
    result_embed = nextcord.Embed(
        title="🎉 {} 🎉".format(data["prize"]),
        color=0x2F3136,
        description="Congratulations {} you won the giveaway !".format(", ".join(users_mention))
    ) \
        .set_footer(icon_url=bot.user.avatar_url, text="Giveaway Ended !")
    await giveaway_message.edit(embed=result_embed)
    ghost_ping = await channel.send(", ".join(users_mention))
    await ghost_ping.delete()
    giveaways_collection.delete_one({"_id": g_id})

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_task.start()

    def cog_unload(self):
        self.giveaway_task.cancel()

    @tasks.loop(seconds=5)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        giveaways = giveaways_collection.find()
        current_time = int(time.time())

        for giveaway in giveaways:
            if current_time > giveaway["end_time"]:
                await stop_giveaway(self.bot, str(giveaway["_id"]), giveaway)

    @commands.command(name="giveaway")
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx: commands.Context):
        init = await ctx.send(embed=nextcord.Embed(
            title="🎉 New Giveaway ! 🎉",
            description="Please answer the following questions to finalize the creation of the Giveaway",
            color=0x2F3136)
            .set_footer(icon_url=self.bot.user.avatar_url, text=self.bot.user.name))

        questions = [
            "What would be the prize of the giveaway?",
            "What would the giveaway channel be like? (Please mention the giveaway channel)",
            "What would be the duration of the giveaway ? Example: (1d | 1h | 1m | 1s)",
            "How many winners do you want for this Giveaway ?"
        ]

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        index = 1
        answers = []
        question_message = None
        for question in questions:
            embed = nextcord.Embed(
                title="Giveaway 🎉",
                description=question,
                color=0x2F3136
            ).set_footer(icon_url=self.bot.user.avatar_url, text="Giveaway !")
            if index == 1:
                question_message = await ctx.send(embed=embed)
            else:
                await question_message.edit(embed=embed)

            try:
                user_response = await self.bot.wait_for("message", timeout=120, check=check)
                await user_response.delete()
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(
                    title="Error",
                    color=0x2F3136,
                    description="You took too long to answer this question"
                ))
                return
            else:
                answers.append(user_response.content)
                index += 1
        try:
            channel_id = int(answers[1][2:-1])
        except ValueError:
            await ctx.send("You didn't mention the channel correctly, do it like {}.".format(ctx.channel.mention))
            return

        try:
            winners = abs(int(answers[3]))
            if winners == 0:
                await ctx.send("You did not enter a positive number.")
                return
        except ValueError:
            await ctx.send("You did not enter an integer.")
            return

        prize = answers[0].title()
        channel = self.bot.get_channel(channel_id)
        converted_time = convert(answers[2])
        if converted_time == -1:
            await ctx.send("You did not enter the correct unit of time (s|m|d|h)")
        elif converted_time == -2:
            await ctx.send("Your time value should be an integer.")
            return

        await init.delete()
        await question_message.delete()
        giveaway_embed = nextcord.Embed(
            title="🎉 {} 🎉".format(prize),
            color=0x2F3136,
            description=f'» **{winners}** {"winner" if winners == 1 else "winners"}\n'
                        f'» Hosted by {ctx.author.mention}\n\n'
                        f'» **React with 🎉 to enter the giveaway.**\n'
        ) \
            .set_footer(icon_url=self.bot.user.avatar_url, text="Ends at")

        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time[0])
        giveaway_message = await channel.send(embed=giveaway_embed)
        await giveaway_message.add_reaction("🎉")
        now = int(time.time())
        data = {
            "_id": str(giveaway_message.id),
            "prize": prize,
            "host": ctx.author.id,
            "winners": winners,
            "end_time": now + converted_time[0],
            "channel_id": channel.id
        }
        giveaways_collection.insert_one(data)

    @commands.command(name="gstop", usage="{giveaway_id}")
    @commands.has_permissions(manage_guild=True)
    async def gstop(self, ctx: commands.Context, message_id):
        await ctx.message.delete()
        giveaway = giveaways_collection.find_one({"_id": message_id})
        if not giveaway:
            return await ctx.send(embed=nextcord.Embed(
                title="Error",
                description="This giveaway ID is not found.",
                color=0x2F3136))
        await stop_giveaway(self.bot, message_id, giveaway)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, (commands.CommandNotFound, nextcord.HTTPException)):
            return

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=nextcord.Embed(
                title="Error",
                description="You don't have permission to use this command.",
                color=0x2F3136))
        
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=nextcord.Embed(
                title="Error",
                description=f"You forgot to provide an argument, please use it like: `{ctx.command.name} {ctx.command.usage}`",
                color=0x2F3136))

def setup(bot):
    bot.add_cog(Giveaways(bot))
