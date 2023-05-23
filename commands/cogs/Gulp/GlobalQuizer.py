
# more questions can be added by adding more buttons

import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

class QuizView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @button(label="Question 1", style=nextcord.ButtonStyle.green)
    async def question_1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        await interaction.response.send_message("What is the capital of France?", ephemeral=True)
        answer = await self.bot.wait_for("message", check=check)
        
        if answer.content.lower() == "paris":
            await interaction.channel.send(f"{interaction.user.mention}, your answer is correct!", delete_after=5)
        else:
            await interaction.channel.send(f"{interaction.user.mention}, your answer is incorrect. The correct answer is Paris.", delete_after=5)

    @button(label="Question 2", style=nextcord.ButtonStyle.green)
    async def question_2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        await interaction.response.send_message("What is the square root of 9?", ephemeral=True)
        answer = await self.bot.wait_for("message", check=check)
        
        if answer.content.lower() == "3":
            await interaction.channel.send(f"{interaction.user.mention}, your answer is correct!", delete_after=5)
        else:
            await interaction.channel.send(f"{interaction.user.mention}, your answer is incorrect. The correct answer is 3.", delete_after=5)

class QuizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quiz")
    async def quiz(self, ctx: commands.Context):
        view = QuizView(self.bot)
        await ctx.send("Click a button to answer a question!", view=view)

def setup(bot):
    bot.add_cog(QuizCog(bot))
