import asyncio
import nextcord
from nextcord.ext import commands


# Works well, need to add admin privilages!

def setup(bot):
    @bot.slash_command(name="moderate", description="A command for various moderation actions")
    async def moderate(interaction: nextcord.Interaction):
        pass

    @moderate.subcommand(name="kick", description="Kick a member from the server")
    @commands.has_permissions(administrator=True)
    async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = None):
        await member.kick(reason=reason)
        embed = nextcord.Embed(
            title=f"<:moderation:881782591060062288> Member Kicked!",
            colour=nextcord.Color.blue(),
            description=f"**{member.mention} has been kicked By** {interaction.user.mention}.\n**Reason:** {reason}.",
        )
        await interaction.respond(embed=embed)

    @moderate.subcommand(name="mute", description="Mute a member")
    @commands.has_permissions(administrator=True)
    async def mute(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = None):
        # Assuming you have a role called "Muted" that restricts the member's permissions
        muted_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await member.add_roles(muted_role)
        await interaction.response.send_message(f"{member.name} has been muted for reason: {reason}")

    @moderate.subcommand(name="ban", description="Ban a member from the server")
    @commands.has_permissions(administrator=True)
    async def ban(interaction: nextcord.Interaction, member: nextcord.Member, *, reason : str = None):
        await member.ban(reason=reason)
        embed = nextcord.Embed(
            title=f"<:moderation:881782591060062288> Member Banned!",
            colour=nextcord.Color.blue(),
            description=f"**{member.mention} has been banned By** {interaction.user.mention}.\n**Reason:** {reason}.",
        )
        await interaction.send(embed=embed)

    @moderate.subcommand(name="unmute", description="Unmute a member")
    @commands.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def unmute(interaction: nextcord.Interaction, member: nextcord.Member):
        muted_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f"{member.name} has been unmuted")

    @moderate.subcommand(name="warn", description="Warn a member")
    @commands.has_permissions(administrator=True)
    async def warn(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = None):
        await interaction.response.send_message(f"{member.name} has been warned for reason: {reason}")

    @moderate.subcommand(name="unban", description="Unban a member")
    @commands.has_permissions(administrator=True)
    async def unban(interaction: nextcord.Interaction, user_id: int):
        user = await bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user.name} has been unbanned")
        
        
    @moderate.subcommand(name="clear", description="Clear messages in a channel")
    @commands.has_permissions(administrator=True)
    async def clear(interaction: nextcord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount+1)
        await interaction.response.send_message(f"{amount} messages have been cleared")
    
    
    @moderate.subcommand(name="tempmute", description="Temporarily mute a member")
    @commands.has_permissions(administrator=True)
    async def tempmute(interaction: nextcord.Interaction, member: nextcord.Member, duration: int, duration_unit: str, reason: str = None):
        # Assuming you have a role called "Muted" that restricts the member's permissions
        muted_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await member.add_roles(muted_role)
        time_to_mute = duration * (60 if duration_unit == "minutes" else 3600 if duration_unit == "hours" else 86400)
        await asyncio.sleep(time_to_mute)
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f"{member.name} has been unmuted after {duration} {duration_unit} for reason: {reason}")
        
        
    @moderate.subcommand(name="nickname", description="Change a member's nickname")
    @commands.has_permissions(administrator=True)
    async def nickname(interaction: nextcord.Interaction, member: nextcord.Member, nickname: str):
        await member.edit(nick=nickname)
        await interaction.response.send_message(f"{member.name}'s nickname has been changed to {nickname}")
        
        
    @moderate.subcommand(name="assignrole", description="Assign a role to a member")
    @commands.has_permissions(administrator=True)
    async def assignrole(interaction: nextcord.Interaction, member: nextcord.Member, role: nextcord.Role):
        await member.add_roles(role)
        await interaction.response.send_message(f"{member.name} has been assigned the {role.name} role")

    @moderate.subcommand(name="removerole", description="Remove a role from a member")
    @commands.has_permissions(administrator=True)
    async def removerole(interaction: nextcord.Interaction, member: nextcord.Member, role: nextcord.Role):
        await member.remove_roles(role)
        await interaction.response.send_message(f"{role.name} has been removed from {member.name}")

    @moderate.subcommand(name="lock", description="Lock a channel")
    @commands.has_permissions(administrator=True)
    async def lock(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message(f"{channel.name} has been locked")
        
    @moderate.subcommand(name="unlock", description="Unlock a channel")
    @commands.has_permissions(administrator=True)
    async def unlock(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message(f"{channel.name} has been unlocked")
        
        
    @moderate.subcommand(name="slowmode", description="Set the slowmode of a channel")
    @commands.has_permissions(administrator=True)
    async def slowmode(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None, seconds: int = 0):
        channel = channel or interaction.channel
        await channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"{channel.name} has been set to slowmode for {seconds} seconds")
        
        
    @moderate.subcommand(name="move", description="Move a member to a different voice channel")
    @commands.has_permissions(administrator=True)
    async def move(interaction: nextcord.Interaction, member: nextcord.Member, channel: nextcord.VoiceChannel):
        await member.move_to(channel)
        await interaction.response.send_message(f"{member.name} has been moved to {channel.name}")
        
        
    @moderate.subcommand(name="deafen", description="Deafen a member")
    @commands.has_permissions(administrator=True)
    async def deafen(interaction: nextcord.Interaction, member: nextcord.Member):
        await member.edit(deafen=True)
        await interaction.response.send_message(f"{member.name} has been deafened")
        
        
    @moderate.subcommand(name="undeafen", description="Undeafen a member")
    @commands.has_permissions(administrator=True)
    async def undeafen(interaction: nextcord.Interaction, member: nextcord.Member):
        await member.edit(deafen=False)
        await interaction.response.send_message(f"{member.name} has been undeafened")
        
    @moderate.subcommand(name="hide", description="Hide a channel")
    @commands.has_permissions(administrator=True)
    async def hide(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.response.send_message(f"{channel.name} has been hidden")
        
        
    @moderate.subcommand(name="unhide", description="Unhide a channel")
    @commands.has_permissions(administrator=True)
    async def unhide(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, view_channel=True)
        await interaction.response.send_message(f"{channel.name} has been unhidden")
        
        
    @moderate.subcommand(name="restrict", description="Restrict a member from sending messages in a channel")
    @commands.has_permissions(administrator=True)
    async def restrict(interaction: nextcord.Interaction, member: nextcord.Member, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        # Assuming you have a role called "Restricted" that restricts the member's ability to send messages
        restricted_role = nextcord.utils.get(interaction.guild.roles, name="Restricted")
        await member.add_roles(restricted_role)
        overwrite = nextcord.PermissionOverwrite(send_messages=False)
        await channel.set_permissions(member, overwrite=overwrite)
        await interaction.response.send_message(f"{member.name} has been restricted from sending messages in {channel.name}")
        
        
        
    @moderate.subcommand(name="unrestrict", description="Unrestrict a member from sending messages in a channel")
    @commands.has_permissions(administrator=True)
    async def unrestrict(interaction: nextcord.Interaction, member: nextcord.Member, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        # Assuming you have a role called "Restricted" that restricts the member's ability to send messages
        restricted_role = nextcord.utils.get(interaction.guild.roles, name="Restricted")
        await member.remove_roles(restricted_role)
        overwrite = nextcord.PermissionOverwrite(send_messages=None)
        await channel.set_permissions(member, overwrite=overwrite)
        await interaction.response.send_message(f"{member.name} has been unrestricted from sending messages in {channel.name}")
        
        
    @moderate.subcommand(name="hidecategory", description="Hide a category")
    @commands.has_permissions(administrator=True)
    async def hidecategory(interaction: nextcord.Interaction, category: nextcord.CategoryChannel):
        await category.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.response.send_message(f"{category.name} has been hidden")
        
        
    @moderate.subcommand(name="unhidecategory", description="Unhide a category")
    @commands.has_permissions(administrator=True)
    async def unhidecategory(interaction: nextcord.Interaction, category: nextcord.CategoryChannel):
        await category.set_permissions(interaction.guild.default_role, view_channel=True)
        await interaction.response.send_message(f"{category.name} has been unhidden")
        
   
        
        
        