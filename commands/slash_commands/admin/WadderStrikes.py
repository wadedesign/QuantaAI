# added a embed

import nextcord

def setup(bot):
    @bot.slash_command(description="Issues a strike to a user for breaking server rules.")
    async def strike(interaction: nextcord.Interaction, user: nextcord.Member, reason: str):
        """
        Issues a strike to a user for breaking server rules.

        Args:
        - user (nextcord.Member): The member to issue a strike to.
        - reason (str): The reason for issuing the strike.
        """
        strike_channel = nextcord.utils.get(interaction.guild.channels, name="strike-logs")
        if not strike_channel:
            strike_category = await interaction.guild.create_category("Strike Logs")
            strike_channel = await interaction.guild.create_text_channel("strike-logs", category=strike_category)

        strike_count = 1
        strike_message = f"{user.mention} has been given a strike by {interaction.user.mention} for the following reason: {reason}\nTotal Strikes: {strike_count}"

        async for message in strike_channel.history(limit=200):
            if message.author.id == user.id:
                strike_count += 1
                strike_message = f"{user.mention} has been given a strike by {interaction.user.mention} for the following reason: {reason}\nTotal Strikes: {strike_count}"
        
        embed = nextcord.Embed(title="Strike Issued", description=strike_message, color=0xFF5733)
        await strike_channel.send(embed=embed)

        try:
            strike_count_message = await user.create_dm()
            await strike_count_message.send(f"You have been given a strike by {interaction.user.mention} for the following reason: {reason}\nTotal Strikes: {strike_count}")
        except:
            pass