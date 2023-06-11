# selectmenucog.py
import json
import nextcord
from nextcord.ext import commands
import os

# ! This is a WIP cog, it is not finished yet

class Dropdown(nextcord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Select an option", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        selected_value = self.values[0]
        await interaction.response.send_message(f"Selected {selected_value}")

        # Check if the selected value is a role ID
        if selected_value.isdigit():
            role = interaction.guild.get_role(int(selected_value))
            if role:
                member = interaction.user
                await member.add_roles(role)
                await interaction.followup.send(f"{member.mention}, you have been given the {role.name} role.")


class DropdownView(nextcord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.add_item(Dropdown(options))

class SelectMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "role_settings.json")

        # Check if the file exists, create it if it doesn't
        if not os.path.exists(self.role_settings_file):
            with open(self.role_settings_file, 'x') as f:
                f.write('{}')

        with open(self.role_settings_file, "r") as f:
            self.role_settings = json.load(f)
            
        def save_role_settings(self):
            with open(self.role_settings_file, "w") as f:
                json.dump(self.role_settings, f)    
            
            

    @commands.has_permissions(administrator=True)
    @commands.command(name="setroles")
    async def setuproles(self, ctx, channel: nextcord.TextChannel):
        self.role_settings[str(ctx.guild.id)] = {
            "channel_id": channel.id
        }
        self.save_role_settings()
        await ctx.send(f"Roles message will be sent to {channel.mention}")

    @nextcord.slash_command(name="language", description="Choose a programming language")
    async def language(self, interaction: nextcord.Interaction):
        language_options = [
            nextcord.SelectOption(label="Python", description="Python is a programming language", value="Python", emoji="🐍"),
            nextcord.SelectOption(label="Java", description="Java is a programming language", value="Java", emoji="☕"),
            nextcord.SelectOption(label="C#", description="C# is a programming language", value="C#", emoji="🔶"),
        ]
        view = DropdownView(language_options)
        await interaction.response.send_message("Choose a programming language:", view=view)
        
    @nextcord.slash_command(name="roles", description="Get server roles that don't have admin permissions")
    async def roles(self, interaction: nextcord.Interaction):
        if str(interaction.guild.id) not in self.role_settings:
            await interaction.response.send_message("Roles setup has not been completed. Please ask an admin to set it up.")
            return

        channel_id = self.role_settings[str(interaction.guild.id)]["channel_id"]
        channel = interaction.guild.get_channel(channel_id)

        role_options = [nextcord.SelectOption(label=role.name, description=f"Role ID: {role.id}", value=str(role.id)) for role in interaction.guild.roles if not role.permissions.administrator]
        view = DropdownView(role_options)
        await channel.send("Choose a role that doesn't have admin permissions:", view=view)
        await interaction.response.send_message(f"Roles message has been sent to {channel.mention}")



def setup(bot):
    bot.add_cog(SelectMenuCog(bot))