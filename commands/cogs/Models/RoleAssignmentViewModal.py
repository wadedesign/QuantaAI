import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

# ! not ready for production

class RoleAssignmentView(View):
    def __init__(self, bot, roles):
        super().__init__(timeout=None)
        self.bot = bot
        self.roles = roles

    async def on_timeout(self):
        try:
            await self.message.delete()
        except:
            pass

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user.bot:
            await interaction.response.send_message("Bots cannot use this view.", ephemeral=True)
            return False
        return True

    @button(label="Assign Role", style=nextcord.ButtonStyle.green)
    async def assign_role(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = await self.select_role(interaction)
        if role is None:
            await interaction.response.send_message("No roles available.", ephemeral=True)
            return
        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"{member.mention}, {role.name} role removed.", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention}, {role.name} role added.", ephemeral=True)

    async def select_role(self, interaction: nextcord.Interaction) -> nextcord.Role:
        role_options = [nextcord.SelectOption(label=role.name, value=str(role.id)) for role in self.roles]
        role_select = nextcord.ui.Select(
            placeholder="Select a role",
            min_values=0,
            max_values=1,
            options=role_options
        )
        view = nextcord.ui.View(timeout=60)
        view.add_item(role_select)
        message = await interaction.response.send_message("Please select a role to assign or remove.", view=view)
        try:
            select_interaction = await view.wait_for("select", timeout=30)
        except asyncio.TimeoutError:
            await message.delete()
            return None
        finally:
            view.stop()
        role_id = int(select_interaction.selected_values[0])
        return interaction.guild.get_role(role_id)

class RoleAssignmentCog2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_assignments = {
            "Sports": ["Basketball", "Football", "Soccer", "Tennis"],
            "Hobbies": ["Gaming", "Reading", "Music", "Travel"],
            "Skills": ["Programming", "Design", "Writing", "Public Speaking"]
        }

    @commands.command(name="roles")
    @commands.has_permissions(administrator=True)
    async def roles(self, ctx: commands.Context):
        roles = [role for role in ctx.guild.roles if role.name in self.get_role_names()]
        view = RoleAssignmentView(self.bot, roles)
        message = await ctx.send("Select a role to assign or remove.", view=view)
        view.message = message

    def get_role_names(self):
        role_names = []
        for roles in self.role_assignments.values():
            role_names += roles
        return role_names

    @commands.command(name="setuproles")
    @commands.has_permissions(administrator=True)
    async def setup_roles(self, ctx: commands.Context):
        category = await ctx.guild.create_category("Role Assignments")
        for role_category, role_names in self.role_assignments.items():
            category = await ctx.guild.create_category(role_category, name=role_category)
        for role_name in role_names:
            role = await ctx.guild.create_role(name=role_name)
            await role.edit(position=category.position+1)
            await role.edit(reason="Role assignment setup.", mentionable=True)
            await role_category.create_text_channel(name=role_name, topic=f"Channel for {role_name} discussion.", overwrites={
                ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                role: nextcord.PermissionOverwrite(read_messages=True)
            })   
            
            
def setup(bot):
    bot.add_cog(RoleAssignmentCog2(bot))
    
    # needs work! 