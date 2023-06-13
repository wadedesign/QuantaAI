import asyncio
import os
import random

import nextcord
from nextcord.ext import commands
from datetime import timedelta
from nextcord.utils import get
import asyncpraw
from nextcord import Embed
from nextcord.ext.commands import Context
from datetime import datetime
import plotly.graph_objects as go
import os 


class WadderCommandsV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="quanta1")
    async def main(self, interaction: nextcord.Interaction):
        pass    



    @main.subcommand(name="detect_alts", description="Detects possible alt accounts in the server.")
    @commands.has_permissions(administrator=True)
    async def detect_alts(self, interaction: nextcord.Interaction):
        members = interaction.guild.members
        possible_alts = {}

        account_creation_difference = timedelta(days=1)  # Change this value to adjust the account creation time difference
        join_time_difference = timedelta(hours=6)  # Change this value to adjust the join time difference

        for member in members:
            for other_member in members:
                if member != other_member:
                    creation_time_diff = abs(member.created_at - other_member.created_at)
                    join_time_diff = abs(member.joined_at - other_member.joined_at)

                    if creation_time_diff <= account_creation_difference and join_time_diff <= join_time_difference:
                        if member.display_name not in possible_alts:
                            possible_alts[member.display_name] = set()
                        possible_alts[member.display_name].add(member)
                        possible_alts[member.display_name].add(other_member)

        alt_message = "Possible alt accounts:\n"
        for display_name, member_set in possible_alts.items():
            if len(member_set) > 1:
                alt_message += f"{display_name}: {', '.join(str(member) for member in member_set)}\n"

        await interaction.send(alt_message)
        
        
        
    @main.subcommand(name="rmessage", description="Sends a message to all members with a specific role.")
    @commands.has_permissions(administrator=True)
    async def rmessage(self, interaction: nextcord.Interaction, role: nextcord.Role, *, message):

        sentCounter = 0
        notSentCounter = 0

        role = get(interaction.guild.roles, id=role.id)

        for user in interaction.guild.members:
            try:
                if role in user.roles:
                    if user.dm_channel is None:
                        await user.create_dm()
                await user.dm_channel.send(message)
                print(f"sent to {user.name}")
                await asyncio.sleep(1)
                sentCounter += 1
            except Exception as e:
                print(e)
                notSentCounter += 1
            await interaction.send(
            f"Message sent to **{str(sentCounter)}** members and not sent to **{str(notSentCounter)}** members"
            )
            
    @main.subcommand()
    async def yesnopoll(self, interaction: nextcord.Interaction,poll: str = nextcord.SlashOption(name="poll", description="The poll to be created",required=True)):
        embed = nextcord.Embed(title=poll,description=f"Total Votes: 0\n\n{'🟩' * 10}\n\n(from: {interaction.user})",colour=nextcord.Colour.purple())
        await interaction.send("Creating Poll.", ephemeral=True)
        msg1 = await interaction.channel.send(embed=embed)
        await msg1.add_reaction('✅')
        await msg1.add_reaction('❌')
        
    @main.subcommand()
    async def hotcalc(self, interaction: nextcord.Interaction, user: nextcord.Member = None):
        if user is None:
            user = interaction.user

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await interaction.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
        
        
    @main.subcommand()
    async def slots(self, interaction: nextcord.Interaction):
        """ Roll the slot machine """
        a, b, c = [random.choice("🍎🍊🍐🍋🍉🍇🍓🍒") for _ in range(3)]

        if (a == b == c):
            results = "All matching, you won! 🎉"
        elif (a == b) or (a == c) or (b == c):
            results = "2 in a row, you won! 🎉"
        else:
            results = "No match, you lost 😢"

        await interaction.send(f"**[ {a} {b} {c} ]\n{interaction.user.name}**, {results}")
        
        
    @main.subcommand()
    async def roulette(self, interaction: nextcord.Interaction, picked_colour: str = None):
        """ Colours roulette """
        colour_table = ["blue", "red", "green", "yellow"]
        if not picked_colour:
            pretty_colours = ", ".join(colour_table)
            return await interaction.send(f"Please pick a colour from: {pretty_colours}")

        picked_colour = picked_colour.lower()
        if picked_colour not in colour_table:
            return await interaction.send("Please give correct color")

        chosen_color = random.choice(colour_table)
        msg = await interaction.send("Spinning 🔵🔴🟢🟡")
        await asyncio.sleep(1)
        result = f"Result: {chosen_color.upper()}"

        if chosen_color == picked_colour:
            await msg.edit(content=f"> {result}\nCongrats, you won 🎉!")
        else:
            await msg.edit(content=f"> {result}\nBetter luck next time")
            
    @main.subcommand()
    @commands.guild_only()
    async def mods(self, interaction: nextcord.Interaction):
        """Check which mods are online on the current guild"""

        # Show loading animation
        loading_message = await interaction.response.send_message("Checking moderator status...")

        animation_frames = [
            "⚙️ Checking moderator status",
            "⚙️ Checking moderator status.",
            "⚙️ Checking moderator status..",
            "⚙️ Checking moderator status..."
        ]

        for frame in animation_frames:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        all_status = {
            "online": {"users": [], "emoji": "🟢", "display_name": "Online"},
            "idle": {"users": [], "emoji": "🟡", "display_name": "Idle"},
            "dnd": {"users": [], "emoji": "🔴", "display_name": "Do Not Disturb"},
            "offline": {"users": [], "emoji": "⚫", "display_name": "Offline"}
        }

        for user in interaction.guild.members:
            user_perm = interaction.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(user.mention)

        embed = nextcord.Embed(title=f"Mods in {interaction.guild.name}", color=0x00FF00)

        for status, data in all_status.items():
            if data["users"]:
                mod_list = ", ".join(data["users"])
                embed.add_field(name=f"{data['emoji']} {data['display_name']} ({len(data['users'])})", value=mod_list, inline=False)

        embed.set_footer(text="Powered by YourBot")
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_author(name="Moderator Status", icon_url=interaction.author.avatar.url)

        await interaction.followup.send_message(embed=embed)

        
        
    # Invite command

    @main.subcommand(description="Add the bot to your server")
    async def invite(self, interaction: nextcord.Interaction):
        # Show loading animation
        loading_message = await interaction.response.send_message("Generating invitation link...")

        # Define the computer animation frames
        animation = [
            "⚙️ Generating invitation link",
            "⚙️ Generating invitation link.",
            "⚙️ Generating invitation link..",
            "⚙️ Generating invitation link..."
        ]

        # Animate the loading message
        for frame in animation:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        embed = nextcord.Embed(
            title="Add the bot to your server",
            description="Click the link below to add the bot to your server. Thanks!",
            url="https://nextcord.com/api/oauth2/authorize?client_id=1072418891680202824&permissions=8&scope=bot%20applications.commands",
            color=0x00ff00
        )
        embed.set_footer(text="Add Wadder")

        # Set the thumbnail using the provided image URL
        image_url = "https://example.com/waddericon.png"  # Replace with your image URL
        embed.set_thumbnail(url=image_url)

        await interaction.send(embed=embed)

        
        
        
        
    @main.subcommand()
    @commands.has_permissions(manage_roles=True, manage_channels=True)
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    async def verifysetup(self, interaction: nextcord.Interaction):
        await interaction.send("I am now setting up the Unverified Role and verification channel. This may take a few seconds. PLEASE DO NOT RERUN THIS COMMAND!")
        guild = interaction.guild
        unverifiedRole = nextcord.utils.get(guild.roles, name="Unverified")

        if unverifiedRole:
            await interaction.send("The Unverified Role already exists. No need to rerun this command")
            return

        if not unverifiedRole:
            unverifiedRole = await guild.create_role(name="Unverified")

            for channel in guild.channels:
                await channel.set_permissions(unverifiedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        await asyncio.sleep(2)

        channel = await guild.create_text_channel('verify')

        guild = interaction.guild
        channel = nextcord.utils.get(guild.text_channels, name="verify")
        role = nextcord.utils.get(guild.roles, name="@everyone")
        await channel.set_permissions(role, send_messages=False, read_messages=False)

        await asyncio.sleep(2)

        guild = interaction.guild
        channel = nextcord.utils.get(guild.text_channels, name="verify")
        role = nextcord.utils.get(guild.roles, name="Unverified")
        bot_mention = self.bot.user.mention  # Get the bot mention
        server_name = guild.name  # Get the server name
        await channel.send(f"WELCOME TO {server_name}\n\nTo prevent spam and abuse, be sure to verify yourself here by typing **/verify** with {bot_mention}")
        await channel.set_permissions(role, send_messages=True, read_messages=True)
        await interaction.send("The **Unverified** role and the **verify** text channel have been set up.")

    @verifysetup.error
    async def verifysetup_error(interaction, error):
        if isinstance(error, commands.BotMissingPermissions):
            await interaction.send("HEY! YOU NEED TO HAVE THE **MANAGE_CHANNELS** AND **MANAGE_ROLE** PERMISSION TO CONTINUE")
        if isinstance(error, commands.MissingPermissions):
            await interaction.send('SYSTEM ERROR: I require the **MANAGE_CHANNELS** and **MANAGE_ROLES** Permission. Recommended to give me Admin to prevent errors.')
        else:
            raise error
        
        
    @main.subcommand()
    async def verify(self, interaction: nextcord.Interaction):
        mutedRole = nextcord.utils.get(interaction.guild.roles, name="ROLENAMEHERE")
        await interaction.user.remove_roles(mutedRole)
        await interaction.send("You have been verified and have access to the rest of the server.")
        embed = nextcord.Embed(title="SUCCESSFULLY VERIFIED", description=f"Thank you for verifying yourself into the server. Now you can access the rest of the server now.", color=(65535))
        await interaction.user.send(embed=embed)
        return

#**/embedwiz title="My Awesome Embed" description="This is a cool embed!" color="FF5733" footer="My Footer" footer_icon="https://example.com/my_footer_icon.png" image="https://example.com/my_image.png" thumbnail="https://example.com/my_thumbnail.png"
#**/embedwiz title="Weather Update" url="https://weather.example.com" description="Today's weather forecast" color="00BFFF" footer="WeatherBot" footer_icon="https://example.com/weather_icon.png" image="https://example.com/weather_image.jpg" thumbnail="https://example.com/weather_thumbnail.jpg" timestamp="now" body="Temperature: 72°F\nHumidity: 45%"

    @main.subcommand(name="embedwiz", description="Create an embed using a wizard")
    async def wde(
            self,
            interaction: nextcord.Interaction,
            title: str = None,
            url: str = None,
            description: str = None,
            color: str = None,  # Change the type hint for color to str
            footer: str = None,
            footer_icon: str = None,
            image: str = None,
            thumbnail: str = None,
            timestamp: str = None,
            body: str = None,
        ):
        if color == "none":
            color = nextcord.Color.default()
        elif color == "random":
            color = nextcord.Color.random()
        elif color == "black":
            color = nextcord.Color(0x000000)
        elif color is not None:
            try:
                color = int(color, 16) if color.startswith("0x") else int(color, 10)
            except ValueError:
                color = interaction.user.color
        else:
            color = interaction.user.color

        embed = nextcord.Embed(
            title=title,
            url=url,
            description=description,
            color=color,
        )

        if footer:
            embed.set_footer(text=footer, icon_url=footer_icon)

        if image:
            embed.set_image(url=image)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if timestamp:
            if timestamp == "now":
                embed.timestamp = datetime.utcnow()
            else:
                try:
                    embed.timestamp = datetime.fromtimestamp(int(timestamp))
                except ValueError:
                    try:
                        embed.timestamp = datetime.fromisoformat(timestamp)
                    except ValueError:
                        pass

        if body:
            if body == "prompt":
                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                await interaction.send("Please enter the body text for your embed:")
                msg = await self.bot.wait_for("message", check=check)
                body = msg.content

            embed.add_field(name="\u200b", value=body, inline=False)

        await interaction.send(embed=embed)
    
    
    @main.subcommand(name="messagestats", description="Get message statistics for the last 100 messages")
    async def message_stats(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        messages = await interaction.channel.history(limit=100).flatten()  # Fetches the latest 100 messages

        users = {}
        for message in messages:
            if message.author.bot:  # Skip messages sent by bots
                continue

            if message.author.id not in users:
                users[message.author.id] = 1
            else:
                users[message.author.id] += 1

        usernames = []
        message_counts = []
        for user_id, count in users.items():
            user = await self.bot.fetch_user(user_id)
            usernames.append(user.name)
            message_counts.append(count)

        # Create a bar chart using Plotly
        fig = go.Figure(data=go.Bar(x=usernames, y=message_counts))
        fig.update_layout(
            title="Message Statistics",
            xaxis_title="User",
            yaxis_title="Number of Messages",
        )

        # Save the chart as an image
        chart_filename = "message_stats.png"
        fig.write_image(chart_filename)

        # Create an embed to display the message statistics
        embed = nextcord.Embed(title="Message Statistics", color=nextcord.Color.blue())
        embed.add_field(name="User", value=' '.join([f':bust_in_silhouette: {name}' for name in usernames]), inline=True)
        embed.add_field(name="Message Count", value=' '.join([f':speech_balloon: {count}' for count in message_counts]), inline=True)

        # Send the chart image and the embed as a message
        with open(chart_filename, "rb") as file:
            chart_image = nextcord.File(file)
            await interaction.send(file=chart_image, embed=embed)

        # Remove the chart image file
        os.remove(chart_filename)

       

            
    
          
        
    

def setup(bot):
    bot.add_cog(WadderCommandsV1(bot))
