import nextcord
import json
from nextcord.ext import commands
from nextcord.ui import Button, View

VERIFICATION_DATA_FILE = 'data/verification_data.json'


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
        self.verification_data = self.load_verification_data()

    def load_verification_data(self):
        try:
            with open(VERIFICATION_DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_verification_data(self):
        with open(VERIFICATION_DATA_FILE, 'w') as f:
            json.dump(self.verification_data, f, indent=4)

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
        for guild_id, guild_data in self.verification_data.items():
            guild = self.bot.get_guild(int(guild_id))
            if guild:
                channel_id = guild_data.get('channel_id')
                if channel_id:
                    channel = guild.get_channel(int(channel_id))
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
        guild_data = self.verification_data.get(str(guild.id), {})
        role_id = guild_data.get('role_id')

        if role_id:
            verified_role = guild.get_role(role_id)
            if verified_role not in member.roles:
                await member.add_roles(verified_role)
                dm_channel = await member.create_dm()
                await dm_channel.send("You've been successfully verified! You can now access the server channels.")
                await interaction.followup.send("You've been successfully verified!", ephemeral=True)
            else:
                await interaction.followup.send("You're already verified.", ephemeral=True)
        else:
            await interaction.followup.send("The verification role for this server has not been set.", ephemeral=True)

    @nextcord.slash_command(name='setverification', description='Set the verification role for the server.')
    async def set_verification_role(self, interaction: nextcord.Interaction, role_id: int):
        if await self.is_admin(interaction.author):
            if str(interaction.guild.id) not in self.verification_data:
                self.verification_data[str(interaction.guild.id)] = {}

            self.verification_data[str(interaction.guild.id)]['role_id'] = role_id

            if 'channel_id' not in self.verification_data[str(interaction.guild.id)]:
                channel = await self.create_verification_channel(interaction.guild)
                self.verification_data[str(interaction.guild.id)]['channel_id'] = channel.id

            self.save_verification_data()
            await interaction.send(f"Verification role successfully set to role ID {role_id}. A verification channel with a button has been created.")
        else:
            await interaction.send("You don't have permission to use this command.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.find_verification_channels()

def setup(bot):
    bot.add_cog(VerificationCog(bot))