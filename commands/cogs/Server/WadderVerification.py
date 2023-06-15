import nextcord
import json
from nextcord.ext import commands
from nextcord.ui import Button, View
from pymongo import MongoClient
import urllib.parse

# ! redo the button and embed lol!

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
verification_collection = db["verification"]


class VerifyButton(Button):
    def __init__(self, verification_cog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verification_cog = verification_cog

    async def callback(self, interaction: nextcord.Interaction):
        await self.verification_cog.verify_member(interaction)


class VerificationView(View):
    def __init__(self, verification_cog):
        super().__init__()
        self.add_item(VerifyButton(verification_cog, label='Verify', style=nextcord.ButtonStyle.green))


class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_collection = verification_collection

    def get_verification_data(self, guild_id):
        return self.verification_collection.find_one({"guild_id": guild_id})

    def save_verification_data(self, verification_data):
        self.verification_collection.replace_one({"guild_id": verification_data["guild_id"]}, verification_data, upsert=True)

    async def is_admin(self, user: nextcord.User):
        return user.guild_permissions.administrator

    async def create_verification_channel(self, guild: nextcord.Guild):
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        }
        channel = await guild.create_text_channel('🔐・verification', overwrites=overwrites)
        view = VerificationView(self)
        await channel.send("Click the button below to get verified:", view=view)
        return channel

    async def find_verification_channels(self):
        for guild in self.bot.guilds:
            verification_data = self.get_verification_data(guild.id)
            if verification_data and verification_data.get('channel_id'):
                channel_id = verification_data['channel_id']
                channel = guild.get_channel(channel_id)
                if channel:
                    async for message in channel.history(limit=100):
                        if message.author == self.bot.user and message.content.startswith("Click the button below"):
                            # Edit the existing verification message
                            view = VerificationView(self)
                            await message.edit(content="Click the button below to get verified:", view=view)
                            break
                    else:
                        # No existing verification message found, create a new one
                        view = VerificationView(self)
                        await channel.send("Click the button below to get verified:", view=view)

    async def verify_member(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        member = interaction.user
        guild = interaction.guild
        verification_data = self.get_verification_data(guild.id)

        if verification_data and verification_data.get('role_id'):
            role_id = verification_data['role_id']
            verified_role = guild.get_role(int(role_id))
            if verified_role:
                if verified_role in member.roles:
                    await member.remove_roles(verified_role)
                    await interaction.followup.send("Verification role has been removed.", ephemeral=True)
                else:
                    await member.add_roles(verified_role)
                    await interaction.followup.send("You've been successfully verified!", ephemeral=True)
            else:
                await interaction.followup.send("The verification role does not exist in the server.", ephemeral=True)
        else:
            await interaction.followup.send("The verification role for this server has not been set.", ephemeral=True)

    @nextcord.slash_command(name="svrole", description="Set or remove the verification role for the server.")
    async def set_verification_role(self, interaction: nextcord.Interaction, role_id: str):
        if await self.is_admin(interaction.user):
            verification_data = self.get_verification_data(interaction.guild.id)
            if not verification_data:
                verification_data = {"guild_id": interaction.guild.id}

            if role_id == "remove":
                if verification_data.get('role_id'):
                    del verification_data['role_id']
                    await interaction.send("Verification role has been removed.")
                else:
                    await interaction.send("There was no verification role set to remove.")
            else:
                verification_data['role_id'] = role_id

                if 'channel_id' not in verification_data:
                    channel = await self.create_verification_channel(interaction.guild)
                    verification_data['channel_id'] = channel.id

                self.save_verification_data(verification_data)
                await interaction.send(f"Verification role successfully set to role ID {role_id}. A verification channel with a button has been created.")
        else:
            await interaction.send("You don't have permission to use this command.")

    @nextcord.slash_command(name="print_roles")
    async def print_roles(self, interaction: nextcord.Interaction):
        guild = interaction.guild
        roles = guild.roles
        for role in roles:
            print(f"{role.name}: {role.id}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.find_verification_channels()


def setup(bot):
    bot.add_cog(VerificationCog(bot))
