import random
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

class RPSView(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    @button(label="Rock", style=nextcord.ButtonStyle.primary)
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.play(interaction, "rock")

    @button(label="Paper", style=nextcord.ButtonStyle.primary)
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.play(interaction, "paper")

    @button(label="Scissors", style=nextcord.ButtonStyle.primary)
    async def scissors(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.play(interaction, "scissors")

    async def play(self, interaction, user_choice):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)

        if user_choice == bot_choice:
            result = "It's a tie!"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"

        await interaction.response.send_message(f"You chose {user_choice}, the bot chose {bot_choice}. {result}")

class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="rps", description="Start a new game of Rock Paper Scissors")
    async def rps(self, interaction: nextcord.Interaction):
        rps_view = RPSView(interaction)
        await interaction.response.send_message("Choose Rock, Paper, or Scissors:", view=rps_view)

def setup(bot):
    bot.add_cog(RockPaperScissors(bot))
