import asyncio
import nextcord
from nextcord.ext import commands

# ** Good Command, RFP **

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

        # Animation frames using ASCII art
        animation_frames = [
            "⠋ Fetching role information...",
            "⠙ Fetching role information...",
            "⠹ Fetching role information...",
            "⠸ Fetching role information...",
            "⠼ Fetching role information...",
            "⠴ Fetching role information...",
            "⠦ Fetching role information...",
            "⠧ Fetching role information...",
            "⠇ Fetching role information...",
            "⠏ Fetching role information..."
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation_frames[0])

        # Animate the loading message
        for frame in animation_frames[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.1)

        embed = nextcord.Embed(title="Role Information", color=role.color)
        embed.add_field(name=":label: Role Name", value=role.name, inline=False)
        embed.add_field(name=":id: Role ID", value=role.id, inline=False)
        embed.add_field(name=":art: Role Color", value=str(role.color), inline=False)
        embed.add_field(name=":arrow_double_down: Role Position", value=role.position, inline=False)
        embed.add_field(name=":lock: Role Permissions", value=str(role.permissions), inline=False)
        embed.add_field(name=":calendar: Role Created At", value=role.created_at, inline=False)
        embed.add_field(name=":busts_in_silhouette: Role Members", value=str(len(role.members)), inline=False)

        await loading_message.edit(content=None, embed=embed)


def setup(bot):
    bot.add_cog(RoleInfoCog(bot))