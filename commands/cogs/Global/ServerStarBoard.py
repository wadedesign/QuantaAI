import nextcord
from nextcord.ext import commands


# This can become something else, but for now it's a starboard cog


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.starboard_channel_name = "starboard"
        self.star_emoji = "⭐"
        self.threshold = 3

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == self.star_emoji and reaction.count == self.threshold:
            starboard_channel = nextcord.utils.get(reaction.message.guild.text_channels, name=self.starboard_channel_name)
            if not starboard_channel:
                overwrites = {
                    reaction.message.guild.default_role: nextcord.PermissionOverwrite(read_messages=True)
                }
                starboard_channel = await reaction.message.guild.create_text_channel(self.starboard_channel_name, overwrites=overwrites)

            embed = nextcord.Embed(description=reaction.message.content, color=0xf6e146)
            embed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar.url)
            embed.set_footer(text=f"Message ID: {reaction.message.id}")
            embed.timestamp = reaction.message.created_at

            if reaction.message.attachments:
                embed.set_image(url=reaction.message.attachments[0].url)

            await starboard_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Starboard(bot))