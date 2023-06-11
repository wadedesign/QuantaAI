import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

#! not ready for production but ALMOST THERE

class ModerationView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def prompt_user_id(self, interaction):
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        await interaction.response.send_message("Enter the user ID of the member you want to moderate:", ephemeral=True)
        response = await self.bot.wait_for("message", check=check)
        return int(response.content)

    @button(label="Mute", style=nextcord.ButtonStyle.red)
    async def mute(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = await self.prompt_user_id(interaction)
        member = interaction.guild.get_member(user_id)

        if member:
            await member.edit(mute=True)
            await interaction.channel.send(f"{interaction.user.mention} muted {member.mention}.", delete_after=5)
        else:
            await interaction.channel.send(f"{interaction.user.mention}, unable to find the specified member.", delete_after=5)

    @button(label="Kick", style=nextcord.ButtonStyle.red)
    async def kick(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = await self.prompt_user_id(interaction)
        member = interaction.guild.get_member(user_id)

        if member:
            await member.kick()
            await interaction.channel.send(f"{interaction.user.mention} kicked {member.mention}.", delete_after=5)
        else:
            await interaction.channel.send(f"{interaction.user.mention}, unable to find the specified member.", delete_after=5)

    @button(label="Ban", style=nextcord.ButtonStyle.red)
    async def ban(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = await self.prompt_user_id(interaction)
        member = interaction.guild.get_member(user_id)

        if member:
            await member.ban()
            await interaction.channel.send(f"{interaction.user.mention} banned {member.mention}.", delete_after=5)
        else:
            await interaction.channel.send(f"{interaction.user.mention}, unable to find the specified member.", delete_after=5)

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="moderate")
    @commands.has_permissions(kick_members=True, ban_members=True, mute_members=True)
    async def moderate(self, ctx: commands.Context):
        view = ModerationView(self.bot)
        await ctx.send("Click a button to mute, kick, or ban a member.", view=view)

def setup(bot):
    bot.add_cog(ModerationCog(bot))
