
# not showing up atm

import random
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

## Todo: Make sub commands of this


class WordScrambleView(View):
    def __init__(self, ctx, word, scrambled_word):
        super().__init__()
        self.ctx = ctx
        self.word = word
        self.scrambled_word = scrambled_word

    @button(label="End Game", style=nextcord.ButtonStyle.red)
    async def end_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"The game has been ended. The word was: {self.word}")
        self.stop()

class WordScramble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ["apple", "banana", "grape", "orange", "watermelon"]
        self.active_games = {}

    @nextcord.slash_command(name="wordscrabble")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="wordscramble", description="Start a new game of Word Scramble")
    async def wordscramble(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.active_games:
            await interaction.response.send_message("A game of Word Scramble is already in progress in this channel.", ephemeral=True)
            return

        word = random.choice(self.words)
        scrambled_word = ''.join(random.sample(word, len(word)))

        self.active_games[interaction.channel.id] = WordScrambleView(interaction, word, scrambled_word)

        await interaction.response.send_message("A new game of Word Scramble has started!")
        await interaction.followup.send(f"Unscramble this word: {scrambled_word}", view=self.active_games[interaction.channel.id])

    @main.subcommand(name="guessword", description="Guess the unscrambled word in the current Word Scramble game")
    async def guessword(self, interaction: nextcord.Interaction, guessed_word: str):
        if interaction.channel.id not in self.active_games:
            await interaction.response.send_message("No active Word Scramble game in this channel. Start a game with /wordscramble.", ephemeral=True)
            return

        game = self.active_games[interaction.channel.id]

        if guessed_word.lower() == game.word.lower():
            await interaction.response.send_message("Congratulations! You've guessed the word!")
            del self.active_games[interaction.channel.id]
        else:
            await interaction.response.send_message("Incorrect guess!")

def setup(bot):
    bot.add_cog(WordScramble(bot))
