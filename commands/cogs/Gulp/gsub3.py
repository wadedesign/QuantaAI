import random
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

class NumberGuessView(View):
    def __init__(self, ctx, number):
        super().__init__()
        self.ctx = ctx
        self.number = number

    @button(label="End Game", style=nextcord.ButtonStyle.red)
    async def end_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"The game has been ended. The number was: {self.number}")
        self.stop()

class NumberGuess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @nextcord.slash_command(name="numberguess", description="Start a new game of Number Guess")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="start", description="Start a new game of Number Guess")
    async def numberguess_start(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.active_games:
            await interaction.response.send_message("A game of Number Guess is already in progress in this channel.", ephemeral=True)
            return

        number = random.randint(1, 10)

        self.active_games[interaction.channel.id] = NumberGuessView(interaction, number)

        await interaction.response.send_message("A new game of Number Guess has started! Guess a number between 1 and 10.")
        await interaction.followup.send(view=self.active_games[interaction.channel.id])

    @main.subcommand(name="guess", description="Guess the number in the current Number Guess game")
    async def numberguess_guess(self, interaction: nextcord.Interaction, guessed_number: int):
        if interaction.channel.id not in self.active_games:
            await interaction.response.send_message("No active Number Guess game in this channel. Start a game with /numberguess start.", ephemeral=True)
            return

        game = self.active_games[interaction.channel.id]

        if guessed_number == game.number:
            await interaction.response.send_message("Congratulations! You've guessed the number!")
            del self.active_games[interaction.channel.id]
        else:
            await interaction.response.send_message("Incorrect guess!")

def setup(bot):
    bot.add_cog(NumberGuess(bot))

