import json
import nextcord
from nextcord.ext import commands   #!set_role_assignment ROLE_ID MESSAGE_COUNT_THRESHOLD
from logger import setup_logger

# Todo: Can utilize this for more sub commands, not utilizing the space well enough.

CONFIG_FILE = 'role_assignment_config.json'

class RoleAssignmentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_data = self.load_config_data()

    def load_config_data(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config_data(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config_data, f, indent=4)

    async def is_admin(self, user: nextcord.User):
        return user.guild_permissions.administrator

    async def update_message_count_and_check_role(self, member: nextcord.Member):
        guild_id = str(member.guild.id)
        if guild_id not in self.config_data:
            return

        config = self.config_data[guild_id]
        message_count_key = f"{member.id}_message_count"
        config[message_count_key] = config.get(message_count_key, 0) + 1

        if config[message_count_key] >= config['message_count_threshold']:
            role = member.guild.get_role(config['role_id'])
            if role not in member.roles:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return

        member = message.author
        await self.update_message_count_and_check_role(member)

    @nextcord.slash_command()
    async def set_role_assignment(self, interaction: nextcord.Interaction, role_id: int, message_count_threshold: int):
        if not await self.is_admin(interaction.user):
            await interaction.send("You don't have permission to use this command.")
            return

        guild_id = str(interaction.guild.id)
        if guild_id not in self.config_data:
            self.config_data[guild_id] = {}

        self.config_data[guild_id]['role_id'] = role_id
        self.config_data[guild_id]['message_count_threshold'] = message_count_threshold
        self.save_config_data()

        await interaction.send(f"Role assignment has been set up. Role ID {role_id} will be assigned after {message_count_threshold} messages.")


    @nextcord.slash_command(name="setuplogger", description="Sets up the logger (Admin only)")
    @commands.has_permissions(administrator=True)
    async def setuplogger(self, interaction: nextcord.Interaction):
        await setup_logger(interaction)


    @setuplogger.error
    async def setuplogger_error(interaction: nextcord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.send("You do not have the required permissions to use this command.", ephemeral=True)
    
def setup(bot):
    bot.add_cog(RoleAssignmentCog(bot))