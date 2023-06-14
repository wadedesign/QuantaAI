import json
import math
import random
import time
import nextcord
from nextcord.ext import commands, tasks
import aiosqlite
import nextcord
import json
import asyncio
import datetime
import time
import random
import os
import discord
import asyncio
from dotenv import load_dotenv
import random as rn
import string

from nextcord.ext import commands
from nextcord.utils import get
import datetime
from datetime import timedelta
from datetime import date
import time
import asyncio
from nextcord.ext import commands
import nextcord
import inspect
import importlib
import sys
import traceback
import re
import unicodedata
import datetime
import unicodedata
from random import randint
from random import choice as randchoice
mentions_transforms = {
    '@everyone': '@\u200beveryone',
    '@here': '@\u200bhere'
}

mention_pattern = re.compile('|'.join(mentions_transforms.keys()))

def convert(date):
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 *24}
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


async def stop_giveaway(self, g_id, data):
    channel = self.bot.get_channel(data["channel_id"])
    giveaway_message = await channel.fetch_message(int(g_id))
    users = await giveaway_message.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))
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
        color=self.color,
        description="Congratulations {} you won the giveaway !".format(", ".join(users_mention))
    ) \
        .set_footer(icon_url=self.bot.user.avatar.url, text="Giveaway Ended !")
    await giveaway_message.edit(embed=result_embed)
    ghost_ping = await channel.send(", ".join(users_mention))
    await ghost_ping.delete()
    giveaways = json.load(open("data/giveaways.json", "r"))
    del giveaways[g_id]
    json.dump(giveaways, open("data/giveaways.json", "w"), indent=4)

class CloudStorage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = {}  # A dictionary to store file data
        self.color = 0x2F3136
        self.giveaway_task.start()
        
        
        
    @tasks.loop(seconds=5)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        giveaways = json.load(open("data/giveaways.json", "r"))

        if len(giveaways) == 0:
            return

        for giveaway in giveaways:
            data = giveaways[giveaway]
            if int(time.time()) > data["end_time"]:
                await stop_giveaway(self, giveaway, data)
    
    @nextcord.slash_command(name="tools1")
    async def main(self, interaction: nextcord.Interaction):
        pass    
    @main.subcommand()
    async def upload(self, interaction: nextcord.Interaction, filename):
        """Upload a file to the cloud storage"""
        attachment = interaction.message.attachments[0]
        file_data = await attachment.read()
        self.storage[filename] = file_data
        await interaction.send(f"File {filename} uploaded successfully!")
        
    @main.subcommand()
    async def download(self, interaction: nextcord.Interaction, filename):
        """Download a file from the cloud storage"""
        if filename not in self.storage:
            await interaction.send(f"File {filename} not found in the cloud storage.")
        else:
            file_data = self.storage[filename]
            await interaction.send(file=nextcord.File(file_data, filename=filename))
            
    @main.subcommand()
    async def share(self, interaction: nextcord.Interaction, filename, user: nextcord.Member):
        """Share a file with another user"""
        if filename not in self.storage:
            await interaction.send(f"File {filename} not found in the cloud storage.")
        else:
            file_data = self.storage[filename]
            await user.send(file=nextcord.File(file_data, filename=filename))
            await interaction.send(f"File {filename} shared with {user.name} successfully!")
    
    @main.subcommand()
    async def delete(self, interaction: nextcord.Interaction, filename):
        """Delete a file from the cloud storage"""
        if filename not in self.storage:
            await interaction.send(f"File {filename} not found in the cloud storage.")
        else:
            del self.storage[filename]
            await interaction.send(f"File {filename} deleted from the cloud storage.")
    @main.subcommand()
    async def grant_access(self, interaction: nextcord.Interaction, filename, user: nextcord.Member):
        """Grant access to a file for a specific user"""
        if filename not in self.storage:
            await interaction.send(f"File {filename} not found in the cloud storage.")
        else:
            # Add user to the access list for the file
            if 'access_list' not in self.storage[filename]:
                self.storage[filename]['access_list'] = []
            self.storage[filename]['access_list'].append(user.id)
            await interaction.send(f"Access granted to file {filename} for user {user.name}")
            
    @main.subcommand()
    async def revoke_access(self, interaction: nextcord.Interaction, filename, user: nextcord.Member):
        """Revoke access to a file for a specific user"""
        if filename not in self.storage:
            await interaction.send(f"File {filename} not found in the cloud storage.")
        else:
            # Remove user from the access list for the file
            if 'access_list' in self.storage[filename]:
                if user.id in self.storage[filename]['access_list']:
                    self.storage[filename]['access_list'].remove(user.id)
                    await interaction.send(f"Access revoked to file {filename} for user {user.name}")
                else:
                    await interaction.send(f"User {user.name} does not have access to file {filename}")
            else:
                await interaction.send(f"No access list found for file {filename}")
                
                
                
    @main.subcommand(description="mine sweeper")
    async def minesweeper(self, interaction: nextcord.Interaction, grid_size = 5):
        """Generate and post a new minesweeper game - grid size can range from 3x3 to 9x9"""

        try: grid_size = int(grid_size)
        except: grid_size = 10
        grid_size = max(min(grid_size,10),3)

        # Percent chance each entry could be a mine
        mine_perc = 20

        # Use 0 -> 8 for the neighbors, and X for bombs
        while True:
            rows = []
            # Populate the bombs
            for x in range(grid_size):
                row = []
                for y in range(grid_size):
                    row.append("X" if random.randint(1,100) <= mine_perc else "0")
                rows.append(row)
            if any(("X" in r for r in rows)): break # We got at least 1
        # Walk the rows and count neighboring bombs
        for x in range(len(rows)):
            for y in range(len(rows[x])):
                if rows[x][y] == "X": continue # Already a bomb, no need to count
                noisy_neighbors = 0
                valid_x = [x]
                valid_y = [y]
                if x-1 >= 0: valid_x.append(x-1)
                if x+1 < len(rows): valid_x.append(x+1)
                if y-1 >= 0: valid_y.append(y-1)
                if y+1 < len(rows[x]): valid_y.append(y+1)
                # Walk the values around our target and count the bombs
                for a in valid_x:
                    for b in valid_y:
                        if rows[a][b] == "X": noisy_neighbors += 1
                # Change the value to reflect the neighbors
                rows[x][y] = str(noisy_neighbors)
        # Walk our list once more replacing the values as needed
        pretty_dict = {
            "0":"||0️⃣||",
            "1":"||1️⃣||",
            "2":"||2️⃣||",
            "3":"||3️⃣||",
            "4":"||4️⃣||",
            "5":"||5️⃣||",
            "6":"||6️⃣||",
            "7":"||7️⃣||",
            "8":"||8️⃣||",
            "X":"||💥||"
        }
        messages = []
        pretty_rows = []
        max_emojis = 99 # Weird limit from discord
        for x in rows:
            if (len(pretty_rows)+1)*len(x) > max_emojis: # Over the limit
                messages.append(pretty_rows)
                pretty_rows = [] # Reset
            row = ""
            for y in x:
                row += pretty_dict.get(y,"")
            pretty_rows.append(row)
        # Catch any leftovers
        if pretty_rows: messages.append(pretty_rows)

        for i,m in enumerate(messages):
            msg = "{}{}".format(
                "" if i!=0 else "__**Minesweeper {}x{}**:__\n".format(
                    grid_size,grid_size,
                ),
                "\n".join(m)
            )
            await interaction.send(msg)        
    # Add other methods for access control and security features
    
    


    @main.subcommand(name="qwhisper",description="Owner sends a message to a user")
    @commands.is_owner()
    async def whisper(self, interaction: nextcord.Interaction, user: nextcord.User, *, msg: str):
        """Dm users."""

        # Define the hacking-themed emoji animation frames
        frames = ["💻 Hacking in progress...", "🔎 Accessing user database...", "⚙️ Bypassing security protocols...",
                "🔓 Decrypting user messages...", "💬 Composing secret message...", "✉️ Sending message...",
                "✅ Message sent successfully! 💥", "🎉 Hacking complete!"]

        loading_message = await interaction.response.send_message(frames[0])

        for frame in frames[1:]:
            await loading_message.edit(content=f"{frame}")
            time.sleep(random.uniform(0.5, 1.5))

        try:
            e = nextcord.Embed(colour=nextcord.Colour.red())
            e.title = "You've received a message from a hacker!"
            e.add_field(name="Hacker:", value=interaction.user, inline=False)
            e.add_field(name="Time:", value=datetime.datetime.now().strftime("%A, %B %d %Y at %I:%M %p").replace("PM", "pm").replace("AM", "am"), inline=False)
            e.add_field(name="Message:", value=msg, inline=False)
            e.set_thumbnail(url=interaction.user.avatar.url)
            await user.send(embed=e)
        except nextcord.Forbidden:
            await loading_message.edit(content=f':x: Failed to send message to user with ID `{user.id}`.')
        else:
            await loading_message.edit(content=f'Successfully sent message to {user.id}')
            
            
    


    
    
    @main.subcommand()
    async def userstats23(self,interaction: nextcord.Interaction, target_user: nextcord.Member = None, private = None):
        
        import matplotlib
        import matplotlib.pyplot as plt
        
        if private == "private":
            private = True

        if target_user is None:
            user = interaction.user
        else:
            user = target_user

        await interaction.send("Retrieving the messages from " + user.display_name + "...")
        dayMonthList = []
        dateList = []
        channelList = []

        if private:
            toSend = interaction.user
        else:
            toSend = interaction

        # Goes through every channel to find the user's messages
        for channel in interaction.guild.text_channels:


            try:

                # Goes through the messages of this channel
                async for msg in channel.history(limit=10000):
                    msgDate = msg.created_at

                    now = date.today()
                    then = msgDate.date()
                    limit = now - timedelta(days=30)

                    # If the message is older than 30 days, our job is done here
                    if then < limit:
                        break

                    # If the message is from the user, then it's the data we want
                    elif msg.author == user:
                        dateList.append(then)
                        channelList.append(msg.channel.name)

            # The bot might not have access to certain channels
            except discord.errors.Forbidden:
                pass

        # Sorting the dateList
        dateList.sort()

        for dates in dateList:
            day = dates.day
            monthName = dates.strftime("%b")
            dayMonth = str(day) + " - " + monthName
            dayMonthList.append(dayMonth)

        # Now that we retrieved the data, we prepare graphs out of it
        dayNb = []
        channelNb = []

        # A list of unique days that still keeps order
        uniqueDayMonth = list(sorted(set(dayMonthList), key=dayMonthList.index))
        uniqueChannel = list(sorted(set(channelList), key=channelList.index))

        # List of messages/month ordered by the unique days list
        for dayMonth in uniqueDayMonth:
            dayNb.append(dayMonthList.count(dayMonth))

        # List of nb of messages/channel ordered by the channel list
        for channel in uniqueChannel:
            channelNb.append(channelList.count(channel))

        # Creates the msg/day graph
        matplotlib.rcParams.update({'font.size': 14})
        fig = plt.figure(figsize=[12, 7])
        plt.style.use("dark_background")

        # Creates the messages/day plot
        ax = fig.add_subplot(211)
        ax.set_facecolor("#36393E")
        ax.bar(uniqueDayMonth, dayNb, color="#7289DA")
        ax.set_title("messages/day from " + user.display_name + " in the last 30 days")

        # Final touches
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Creates the messages/channel plot
        ax2 = fig.add_subplot(212)
        ax2.set_facecolor("#36393E")
        ax2.bar(uniqueChannel, channelNb, color="#7289DA")
        ax2.set_title("messages/channel from " + user.display_name + " in the last 30 days")

        # Final touches
        plt.xticks(rotation=35)
        plt.tight_layout()

        # Randomly generated plot ID to prevent mixing up plots between users
        plotID = str(rn.randrange(1, 10000000))
        output_folder = "output"
        filename = f"Plot_id{plotID}.png"
        output_path = os.path.join(output_folder, filename)

        plt.savefig(output_path, transparent=False, facecolor="#36393E", edgecolor='none')

        matplotlib.rcParams.update({'font.size': 12})

        if private:
            await interaction.send("The data has been processed! Check your DMs! (private stats)")

        await toSend.send("Here are the stats for " + user.mention + " 's messages: (Click to enhance)")
        await toSend.send(file=nextcord.File(output_path))
        os.remove(output_path)

        plt.clf()
        plt.close()
        fig.clf()


    
    

    @main.subcommand()
    async def invites(self, interaction: nextcord.Interaction, user:nextcord.Member=None):
        if user is None:
            total_invites = 0
            for i in await interaction.guild.invites():
                if i.inviter == interaction.user:
                    total_invites += i.uses
            await interaction.send(f"You've invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")
        else:
            total_invites = 0
            for i in await interaction.guild.invites():
                if i.inviter == user:
                    total_invites += i.uses

            await interaction.send(f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")
            
    @main.subcommand(name='listusers')
    async def listusers(self, interaction: nextcord.Interaction):
        """Displays the list of connected users"""
        if not interaction.user.voice:
            return await interaction.send("You are not connected to a voice channel :mute:")
        members = interaction.user.voice.channel.members
        memnames = []
        for member in members:
            memnames.append(member.name)
        await interaction.send(f"Members in {interaction.user.voice.channel.name}:\n```\n" + "\n".join(memnames) +"\n```") 
            
            
            
    @main.subcommand(
        name="giveaway")
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, interaction: nextcord.Interaction):
        init = await interaction.send(embed=nextcord.Embed(
            title="🎉 New Giveaway ! 🎉",
            description="Please answer the following questions to finalize the creation of the Giveaway",
            color=self.color)
                       .set_footer(icon_url=self.bot.user.avatar.url, text=self.bot.user.name))

        questions = [
            "What would be the prize of the giveaway?",
            "What would the giveaway channel be like? (Please mention the giveaway channel)",
            "What would be the duration of the giveaway ? Example: (1d | 1h | 1m | 1s)",
            "How many winners do you want for this Giveaway ?"
        ]

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        index = 1
        answers = []
        question_message = None
        for question in questions:
            embed = nextcord.Embed(
                title="Giveaway 🎉",
                description=question,
                color=self.color
            ).set_footer(icon_url=self.bot.user.avatar.url, text="Giveaway !")
            if index == 1:
                question_message = await interaction.send(embed=embed)
            else:
                await question_message.edit(embed=embed)

            try:
                user_response = await self.bot.wait_for("message", timeout=120, check=check)
                await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.send(embed=nextcord.Embed(
                    title="Error",
                    color=self.color,
                    description="You took too long to answer this question"
                ))
                return
            else:
                answers.append(user_response.content)
                index += 1
        try:
            channel_id = int(answers[1][2:-1])
        except ValueError:
            await interaction.send("You didn't mention the channel correctly, do it like {}.".format(interaction.channel.mention))
            return

        try:
            winners = abs(int(answers[3]))
            if winners == 0:
                await interaction.send("You did not enter an postive number.")
                return
        except ValueError:
            await interaction.send("You did not enter an integer.")
            return
        prize = answers[0].title()
        channel = self.bot.get_channel(channel_id)
        converted_time = convert(answers[2])
        if converted_time == -1:
            await interaction.send("You did not enter the correct unit of time (s|m|d|h)")
        elif converted_time == -2:
            await interaction.send("Your time value should be an integer.")
            return
        await init.delete()
        await question_message.delete()
        giveaway_embed = nextcord.Embed(
            title="🎉 {} 🎉".format(prize),
            color=self.color,
            description=f'» **{winners}** {"winner" if winners == 1 else "winners"}\n'
                        f'» Hosted by {interaction.user.mention}\n\n'
                        f'» **React with 🎉 to get into the giveaway.**\n'
        )\
            .set_footer(icon_url=self.bot.user.avatar.url, text="Ends at")

        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time[0])
        giveaway_message = await channel.send(embed=giveaway_embed)
        await giveaway_message.add_reaction("🎉")
        now = int(time.time())
        giveaways = json.load(open("data/giveaways.json", "r"))
        data = {
            "prize": prize,
            "host": interaction.user.id,
            "winners": winners,
            "end_time": now + converted_time[0],
            "channel_id": channel.id
        }
        giveaways[str(giveaway_message.id)] = data
        json.dump(giveaways, open("data/giveaways.json", "w"), indent=4)

    @main.subcommand(
        name="gstop"
    )
    @commands.has_permissions(manage_guild=True)
    async def gstop(self, interaction: nextcord.Interaction, message_id):
        await interaction.message.delete()
        giveaways = json.load(open("data/giveaways.json", "r"))
        if not message_id in giveaways.keys(): return await interaction.send(
            embed=nextcord.Embed(title="Error",
                                description="This giveaway ID is not found.",
                                color=self.color))
        await stop_giveaway(self, message_id, giveaways[message_id])

    @commands.Cog.listener()
    async def on_command_error(self, interaction: commands.Context, error):
        if isinstance(error, (commands.CommandNotFound, nextcord.HTTPException)):
            return

        if isinstance(error, commands.MissingPermissions):
            return await interaction.send(embed=nextcord.Embed(
                title="Error",
                description="You don't have the permission to use this command.",
                color=self.color))
        if isinstance(error, commands.MissingRequiredArgument):
            return await interaction.send(embed=nextcord.Embed(
                title="Error",
                description=f"You forgot to provide an argument, please do it like: `{interaction.command.name} {interaction.command.usage}`",
                color=self.color))
  
    
    
def setup(bot):
    bot.add_cog(CloudStorage(bot))