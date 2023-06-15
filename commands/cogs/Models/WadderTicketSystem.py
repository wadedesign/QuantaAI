import nextcord
from nextcord.ext import commands
import asyncio
import os
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
tickets_collection = db["tickets"]


# ** RFP ** Quick make the ticket include the user who made it in the embed


# works now!!!!

class AddUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Add User to Ticket",
            timeout=400,
        )
        self.channel = channel
        self.user = nextcord.ui.TextInput(
            label="User ID",
            min_length=2,
            max_length=30,
            required=True,
            placeholder="User ID (Must be INT)"
        )
        self.add_item(self.user)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send(f"Invalid User ID, make sure the user is in the guild")
        overwrites = nextcord.PermissionOverwrite()
        overwrites.read_messages = True
        await self.channel.set_permissions(user, overwrite=overwrites)
        await interaction.send(f"{user.mention} added to the ticket", ephemeral=True)


class RemoveUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Add User to Ticket",
            timeout=400,
        )

        self.channel = channel
        self.user = nextcord.ui.TextInput(
            label="User ID",
            min_length=2,
            max_length=30,
            required=True,
            placeholder="User ID (Must be INT)"
        )

        self.add_item(self.user)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send(f"Invalid User ID, make sure the user is in the guild")
        overwrites = nextcord.PermissionOverwrite()
        overwrites.read_messages = False
        await self.channel.set_permissions(user, overwrite=overwrites)
        await interaction.send(f"{user.mention} removed from the ticket", ephemeral=True)


class CreateTicket(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(label="Create Ticket", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket:blurple")
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.response.send_message("Ticket Being Created...", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
        }
        channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.name}-ticket",
            overwrites=overwrites
        )
        await msg.edit(f"Channel Created: {channel.mention}")
        embed = nextcord.Embed(
            title="Ticket Created",
            description=f"{interaction.user.mention} create a ticket! Click one of the buttons below to alter the settings",
            color=0x00FFFF
        )
        await channel.send(embed=embed, view=TicketSettings(channel))

        # Save ticket data to MongoDB
        ticket_data = {
            "guild_id": interaction.guild.id,
            "channel_id": channel.id,
            "user_id": interaction.user.id
        }
        tickets_collection.insert_one(ticket_data)

    async def on_timeout(self):
        # Remove the view if it times out
        self.stop()


class TicketSettings(nextcord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=None)
        self.channel = channel

    @nextcord.ui.button(label="Close Ticket", style=nextcord.ButtonStyle.blurple, custom_id="ticket_settings:red")
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        messages = await interaction.channel.history(limit=None, oldest_first=True).flatten()
        contents = [message.content for message in messages]  # Get all the messages
        final = ""
        for msg in contents:
            msg = msg + "\n"
            final = final + msg
        with open('data/transcripts.txt', 'w') as f:
            f.write(final)
        print("Transcripts saved to file.")

        await interaction.response.send_message("Ticket Being Closed...", ephemeral=True)
        await interaction.channel.delete()
        print("Channel deleted.")

        file_path = 'data/transcripts.txt'
        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return

        try:
            await interaction.user.send(f"Ticket Closed: {interaction.channel.mention}", file=nextcord.File(file_path))
            print("Transcripts sent to user.")
        except nextcord.HTTPException as e:
            print("Error sending transcripts to user:", e)

        os.remove(file_path)
        print("Transcripts file removed.")

        # Remove ticket data from MongoDB
        tickets_collection.delete_one({"channel_id": interaction.channel.id})

        # Save ticket transcripts to MongoDB
        transcript_data = {
            "channel_id": interaction.channel.id,
            "transcripts": contents
        }
        transcripts_collection = db["transcripts"]
        transcripts_collection.insert_one(transcript_data)

    @nextcord.ui.button(label="Add User", style=nextcord.ButtonStyle.green, custom_id="ticket_settings:green")
    async def add_user(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(AddUser(interaction.channel))

    @nextcord.ui.button(label="Remove User", style=nextcord.ButtonStyle.gray, custom_id="ticket_settings:gray")
    async def remove_user(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RemoveUser(interaction.channel))


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False
        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            self.bot.add_view(CreateTicket(self.bot))
            self.bot.add_view(TicketSettings(self.channel))
        self.persistent_views_added = True
        print("Added persistent view")

        # Retrieve existing ticket data from MongoDB
        ticket_documents = tickets_collection.find()
        for ticket_document in ticket_documents:
            guild = self.bot.get_guild(ticket_document["guild_id"])
            channel = guild.get_channel(ticket_document["channel_id"])
            user = guild.get_member(ticket_document["user_id"])
            if guild and channel and user:
                view = TicketSettings(channel)
                await channel.send("Ticket in progress:", view=view)

    @commands.command(name="ticket", description="Setup the ticket system")
    @commands.has_permissions(manage_guild=True)
    async def setup_tickets(self, ctx: commands.Context):
        embed = nextcord.Embed(title="Ticket System", description="Click the Create Ticket Button ", color=0x00FFFF)
        await ctx.send(embed=embed, view=CreateTicket(self.bot))

    @commands.command(name="setrole", description="Set the role to be added to the ticket")
    @commands.has_permissions(manage_guild=True)
    async def setrole(self, ctx: commands.Context, role: nextcord.Role):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT role FROM roles WHERE guild = ?", (ctx.guild.id,))
            role2 = await cursor.fetchone()
            if role2:
                await cursor.execute("UPDATE roles SET role = ? WHERE guild = ?", (role.id, ctx.guild.id))
                await ctx.send(f"Tickets Auto-Assign Role Updated!")
            else:
                await cursor.execute("INSERT INTO roles VALUES (?, ?)", (role.id, ctx.guild.id))
                await ctx.send(f"Tickets Auto-Assign Role added!")
        await self.bot.db.commit()


def setup(bot):
    bot.add_cog(TicketSystem(bot))
