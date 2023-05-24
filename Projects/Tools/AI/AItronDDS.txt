import nextcord
from nextcord.ext import commands
from langchain.tools import DuckDuckGoSearchRun

class AITronDuck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search = DuckDuckGoSearchRun()

    @commands.command()
    async def search_question(self, ctx, question):
        result = self.search.run(question)

        embed = nextcord.Embed(title="Search Result", description=result)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AITronDuck(bot))
