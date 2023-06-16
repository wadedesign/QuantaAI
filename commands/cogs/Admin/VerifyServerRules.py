import nextcord
from nextcord.ext import commands
from nextcord.ui import View, button

class VerifyServerRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)
    async def vsrules(self, interaction: nextcord.Interaction):
        def check(button, user):
            return user == interaction.user and button.custom_id == 'verify_button'

        # Create the embed for the rules
        rules_embed = nextcord.Embed(title="Server Rules", description="Please read and follow the rules below:")

        # Prompt the user to input the rules one by one
        await interaction.send('Please input the rules one by one. Type "quit" to finish:')
        rules = []
        while True:
            rule = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user)
            if rule.content.lower() == 'quit':
                break
            rules.append(rule.content)

        # Add the rules to the embed
        for i, rule in enumerate(rules):
            rules_embed.add_field(name=f"Rule {i+1}", value=rule, inline=False)

        # Prompt the user to specify the channel to send the rules to
        await interaction.send('Please specify the channel to send the rules to (mention the channel):')
        channel_input = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel_mentions)
        channel = channel_input.channel_mentions[0]

        # Prompt the user to specify the role to assign to verified users
        await interaction.send('Please specify the role to assign to verified users:')
        role_input = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user)
        role_name = role_input.content
        print(f'Role name: {role_name}')
        role = nextcord.utils.get(interaction.guild.roles, name=role_name)
        print(f'Role: {role}')

        # Send the rules as an embed to the specified channel
        rules_message = await channel.send(embed=rules_embed)

        # Create the verify button
        verify_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label='Verify', custom_id='verify_button')

        # Add the verify button to the rules message
        action_row = nextcord.ui.ActionRow(verify_button)
        await rules_message.edit(content=f'React with the button below to gain access to other areas of the Discord server.', embed=None, view=nextcord.ui.View(action_row))

        # Wait for the user to click the verify button
        button, user = await self.bot.wait_for('button_click', check=check)
        await user.add_roles(role)
        await interaction.send(f'{user.mention} has been verified and now has access to other areas of the server.')

def setup(bot):
    bot.add_cog(VerifyServerRules(bot))
