import nextcord
from nextcord.ext import commands

class RoleInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_admin(self, user: nextcord.User):
        return user.guild_permissions.administrator

    @nextcord.slash_command()
    async def role_info(self, interaction: nextcord.Interaction, role: nextcord.Role):
        """Provide information about a specified role (Admin only)."""

        if not await self.is_admin(interaction.user):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        role_info = (
            f"**Role Name:** {role.name}\n"
            f"**Role ID:** {role.id}\n"
            f"**Role Color:** {role.color}\n"
            f"**Role Position:** {role.position}\n"
            f"**Role Permissions:** {role.permissions}\n"
            f"**Role Created At:** {role.created_at}\n"
            f"**Role Members:** {len(role.members)}"
        )

        await interaction.response.send_message(role_info)

def setup(bot):
    bot.add_cog(RoleInfoCog(bot))