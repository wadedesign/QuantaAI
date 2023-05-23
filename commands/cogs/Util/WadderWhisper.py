import nextcord
import datetime

from nextcord.ext import commands

class Pm(commands.Cog):
    """PM People Using The Bot"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def whisper(self, ctx, user_id: int, *, msg: str):
        """Dm users."""
        user = await self.bot.fetch_user(user_id)
        try:
            e = nextcord.Embed(colour=nextcord.Colour.red())
            e.title = "You've recieved a message from a developer!"
            e.add_field(name="Developer:", value=ctx.message.author, inline=False)
            e.add_field(name="Time:", value=datetime.datetime.now().strftime("%A, %B %-d %Y at %-I:%M%p").replace("PM", "pm").replace("AM", "am"), inline=False)
            e.add_field(name="Message:", value=msg, inline=False)
            e.set_thumbnail(url=ctx.message.author.avatar_url)
            await user.send(embed=e)
        except:
            await ctx.send(':x: Failed to send message to user_id `{}`.'.format(user_id))
        else:
            await ctx.send('Succesfully sent message to {}'.format(user_id))

def setup(bot):
    bot.add_cog(Pm(bot))



