import nextcord
import json
from nextcord.ext import commands
from nextcord.ui import Button, View
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
verification_collection = db["verification"]

# ! This is not ready for production

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
        channel = await guild.create_text_channel('verification', overwrites=overwrites)
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
                    # Delete all previous verification messages in the channel
                    async for message in channel.history(limit=100):
                        if message.author == self.bot.user and message.content.startswith("Click the button below"):
                            await message.delete()

                    # Send a new verification message with a button
                    view = VerificationView(self)
                    await channel.send("Click the button below to get verified:", view=view)

    async def verify_member(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        member = interaction.user
        guild = interaction.guild
        verification_data = self.get_verification_data(guild.id)

        if verification_data and verification_data.get('role_id'):
            role_id = verification_data['role_id']
            verified_role = guild.get_role(role_id)
            if verified_role and verified_role not in member.roles:
                await member.add_roles(verified_role)
                dm_channel = await member.create_dm()
                await dm_channel.send("You've been successfully verified! You can now access the server channels.")
                await interaction.followup.send("You've been successfully verified!", ephemeral=True)
            else:
                await interaction.followup.send("You're already verified.", ephemeral=True)
        else:
            await interaction.followup.send("The verification role for this server has not been set.", ephemeral=True)

    @commands.command(name="svrole")
    async def set_verification_role(self, ctx: commands.Context, role_id: int):
        if await self.is_admin(ctx.author):
            verification_data = self.get_verification_data(ctx.guild.id)
            if not verification_data:
                verification_data = {"guild_id": ctx.guild.id}

            verification_data['role_id'] = role_id

            if 'channel_id' not in verification_data:
                channel = await self.create_verification_channel(ctx.guild)
                verification_data['channel_id'] = channel.id

            self.save_verification_data(verification_data)
            await ctx.send(f"Verification role successfully set to role ID {role_id}. A verification channel with a button has been created.")
        else:
            await ctx.send("You don't have permission to use this command.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.find_verification_channels()

def setup(bot):
    bot.add_cog(VerificationCog(bot))
