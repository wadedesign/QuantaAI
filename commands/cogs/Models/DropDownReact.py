import json
import nextcord
from nextcord.ext import commands
from nextcord.ui import Select, View
from nextcord.interactions import Interaction


# pretty good, would like it to static in the discord

class Dropdown(Select):
    def __init__(self, options):
        super().__init__(placeholder='Select a role', options=options)

    async def callback(self, interaction: Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message(f'Role not found for ID: {role_id}', ephemeral=True)
            return

        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f'Removed role {role.name}', ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f'Assigned role {role.name}', ephemeral=True)

class DropdownMenu(View):
    def __init__(self, options):
        super().__init__()
        self.add_item(Dropdown(options))

class DropdownCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_file = 'data/dropdown_roles.json'
        self.selection = self.load_roles()

    def load_roles(self):
        try:
            with open(self.roles_file, 'r') as f:
                roles_data = json.load(f)
            selection = [nextcord.SelectOption(**role_data) for role_data in roles_data]
        except FileNotFoundError:
            selection = [nextcord.SelectOption(label='No role added', value='0', description='Add a role to the dropdown using /addrole')]
        
        return selection

    def save_roles(self):
        roles_data = [select_option.to_dict() for select_option in self.selection]
        with open(self.roles_file, 'w') as f:
            json.dump(roles_data, f)

    @nextcord.slash_command(name='test', description='test command', dm_permission=False, default_member_permissions=8)
    async def test(self, interaction: Interaction):
        view = DropdownMenu(self.selection)
        await interaction.response.send_message('test', view=view)

    @nextcord.slash_command(name='create', description='Create new self assignable roles', dm_permission=False, default_member_permissions=8)
    async def create(self, interaction: Interaction,
                     channel: nextcord.TextChannel = nextcord.SlashOption(
                        description='Channel where the role dropdown will be',
                        required=True
                     ),
                     name: str = nextcord.SlashOption(
                         description='Name of the placeholder of the dropdown',
                         required=False
                     ),
                    ):
        await channel.send(view=DropdownMenu(self.selection))
        await interaction.response.send_message(f'Dropdown created at {channel.mention}', ephemeral=True)

    @nextcord.slash_command(name='addrole', description='Add a role to the dropdown', dm_permission=False, default_member_permissions=8)
    async def addrole(self, interaction: Interaction,
                      role: nextcord.Role = nextcord.SlashOption(
                          description='Role to add to the dropdown',
                          required=True
                      )):
        self.selection.append(nextcord.SelectOption(label=role.name, value=str(role.id), description=f'Role: {role.name}'))
        self.save_roles()
        await interaction.response.send_message(f'Role {role.name} added to the dropdown', ephemeral=True)

def setup(bot):
    bot.add_cog(DropdownCommands(bot))
