import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
from nextcord import File
import os

class Helpful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def add_gif_to_embed(self, embed, gif_path):
        """Helper function to add a GIF to an embed"""
        gif_file = File(gif_path, filename='animated.gif')
        embed.set_image(url="attachment://animated.gif")
        embed.set_footer(text="GIF provided by Quanta")  # Optional: Set a footer for the embed

    @commands.command()
    async def channel_status(self, ctx, channel: nextcord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        server_id = self.bot.get_guild(self.bot.guilds[0].id)

        embed = nextcord.Embed(colour=nextcord.Colour.orange())
        embed.set_author(name="Channel Health:")

        async with ctx.channel.typing():
            count = 0
            async for message in channel.history(limit=500000, after=datetime.today() - timedelta(days=100)):
                count += 1

            if count >= 5000:
                average = "OVER 5000!"
                healthiness = "VERY HEALTHY \U0001F60D"  # Emoji: 😍
            else:
                try:
                    average = round(count / 100, 2)

                    if 0 > server_id.member_count / average:
                        healthiness = "VERY HEALTHY \U0001F60D"  # Emoji: 😍
                    elif server_id.member_count / average <= 5:
                        healthiness = "HEALTHY \U0001F642"  # Emoji: 🙂
                    elif server_id.member_count / average <= 10:
                        healthiness = "NORMAL \U0001F610"  # Emoji: 😐
                    elif server_id.member_count / average <= 20:
                        healthiness = "UNHEALTHY \U0001F615"  # Emoji: 😕
                    else:
                        healthiness = "VERY UNHEALTHY \U0001F625"  # Emoji: 😥

                except ZeroDivisionError:
                    average = 0
                    healthiness = "VERY UNHEALTHY \U0001F625"  # Emoji: 😥

            embed.add_field(name="­", value=f" Number of members: {server_id.member_count}", inline=False)
            embed.add_field(name="­", value=f'Number of messages per day on average in "{channel}" is: {average}', inline=False)
            embed.add_field(name="­", value=f"Channel health: {healthiness}", inline=False)

            # Get the path to the GIF file in your project's directory
            gif_path = os.path.join(os.getcwd(), 'images', 'quanta.gif')

            # Attach the GIF file to the embed
            self.add_gif_to_embed(embed, gif_path)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Helpful(bot))

