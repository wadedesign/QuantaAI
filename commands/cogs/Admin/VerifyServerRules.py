import nextcord
from nextcord.ext import commands

# error 53 object has no attriubute id 

class VerifyServerRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)
    async def vsrules(self, interaction: nextcord.Interaction):
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) == '✅'

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

        # Add the verification check mark
        await rules_message.add_reaction('✅')
        await interaction.send(f'The rules have been sent to {channel.mention}. React with ✅ on the rules message to gain access to other areas of the Discord server.')

        # Wait for the user to react to the rules message
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        await user.add_roles(role)
        await interaction.send(f'{user.mention} has been verified and now has access to other areas of the server.')

def setup(bot):
    bot.add_cog(VerifyServerRules(bot))