import random
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View, Select


# !Add more sub commands (Change whole file) and add more words

class HangmanView(View):
    def __init__(self, ctx, word, display, guesses):
        super().__init__()
        self.ctx = ctx
        self.word = word
        self.display = display
        self.guesses = guesses

    @button(label="End Game", style=nextcord.ButtonStyle.red)
    async def end_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"The game has been ended. The word was: {self.word}")
        self.stop()

class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ["apple", "banana", "grape", "orange", "watermelon"]
        self.active_games = {}
    
    @nextcord.slash_command(name="hangerman")
    async def main(self, interaction: nextcord.Interaction):
        pass
    @main.subcommand(name="hangman", description="Start a new game of hangman")
    async def hangman(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.active_games:
            await interaction.response.send_message("A game of hangman is already in progress in this channel.", ephemeral=True)
            return

        word = random.choice(self.words)
        display = ["_" if letter.isalnum() else letter for letter in word]
        guesses = []

        self.active_games[interaction.channel.id] = HangmanView(interaction, word, display, guesses)

        await interaction.response.send_message("A new game of hangman has started!")
        await interaction.followup.send(" ".join(display), view=self.active_games[interaction.channel.id])

    @main.subcommand(name="guess", description="Guess a letter in the current hangman game")
    async def guess(self, interaction: nextcord.Interaction, letter: str):
        if interaction.channel.id not in self.active_games:
            await interaction.response.send_message("No active hangman game in this channel. Start a game with /hangman.", ephemeral=True)
            return

        game = self.active_games[interaction.channel.id]

        if letter.lower() in game.guesses:
            await interaction.response.send_message("This letter has already been guessed!", ephemeral=True)
            return

        game.guesses.append(letter.lower())

        if letter.lower() in game.word.lower():
            for idx, char in enumerate(game.word):
                if char.lower() == letter.lower():
                    game.display[idx] = char

            await interaction.response.send_message("Correct guess!")
        else:
            await interaction.response.send_message("Incorrect guess!")

        await interaction.followup.send(" ".join(game.display))

        if "_" not in game.display:
            await interaction.followup.send("Congratulations! You've guessed the word!")
            del self.active_games[interaction.channel.id]

def setup(bot):
    bot.add_cog(Hangman(bot))