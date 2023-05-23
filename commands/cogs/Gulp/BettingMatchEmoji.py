import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View, Select

class BettingMatchView(View):
    def __init__(self, ctx, emoji_set, shuffled_emojis, bet_amount):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.emoji_set = emoji_set
        self.shuffled_emojis = shuffled_emojis
        self.correct_selections = 0
        self.bet_amount = bet_amount

    async def on_timeout(self):
        await self.ctx.send("Time's up!")

    @button(label="Submit", style=nextcord.ButtonStyle.green)
    async def submit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.correct_selections == len(self.emoji_set):
            # Modify the user's balance here, adding the bet amount as a reward.
            await interaction.response.send_message(f"Congratulations! You've matched all the emojis! You've won {self.bet_amount}!")
        else:
            await interaction.response.send_message(f"Time's up! You matched {self.correct_selections} out of {len(self.emoji_set)} emojis.")
        self.stop()

class BettingMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_list = ["🍎", "🍌", "🍇", "🍉", "🍊", "🍋", "🍍", "🥥", "🥦", "🥕"]
        self.active_games = {}
        self.user_balances = {}  # Add a dictionary to store user balances

    @nextcord.slash_command(name="bettingmatch", description="Start a new betting game")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="start", description="Start a new betting game")
    async def bettingmatch_start(self, interaction: nextcord.Interaction, bet_amount: int):
        if interaction.channel.id in self.active_games:
            await interaction.response.send_message("A betting game is already in progress in this channel.", ephemeral=True)
            return

        if not self.check_user_balance(interaction.user, bet_amount):
            await interaction.response.send_message("You don't have enough balance to place this bet.", ephemeral=True)
            return

        self.update_user_balance(interaction.user, -bet_amount)  # Deduct bet amount from user's balance

        emoji_set = random.sample(self.emoji_list, 4)
        shuffled_emojis = random.sample(emoji_set, len(emoji_set))

        self.active_games[interaction.channel.id] = BettingMatchView(interaction, emoji_set, shuffled_emojis, bet_amount)

        await interaction.response.send_message("A new betting game has started! Memorize the following emojis:")
        await interaction.followup.send(" ".join(emoji_set))
        await asyncio.sleep(10)
        await interaction.followup.send("Now, select the emojis in the correct order:", view=self.active_games[interaction.channel.id])

    @main.subcommand(name="select", description="Select an emoji in the current betting game")
    async def bettingmatch_select(self, interaction: nextcord.Interaction, emoji: str):
        if interaction.channel.id not in self.active_games:
            await interaction.response.send_message("No active betting game in this channel. Start a game with /bettingmatch start.", ephemeral=True)
            return

        game = self.active_games[interaction.channel.id]
        if emoji in game.emoji_set:
            idx = game.emoji_set.index(emoji)

            if game.shuffled_emojis[idx] == emoji:
                await interaction.response.send_message("Correct emoji!")
                game.correct_selections += 1
            else:
                await interaction.response.send_message("Incorrect emoji!")
        else:
            await interaction.response.send_message("Invalid emoji! Select one of the emojis from the game.")

    def check_user_balance(self, user, bet_amount):
        if user not in self.user_balances:
            self.user_balances[user] = 1000  # Initialize balance if not already present
        return self.user_balances[user] >= bet_amount

    def update_user_balance(self, user, amount):
        if user not in self.user_balances:
            self.user_balances[user] = 1000  # Initialize balance if not already present
        self.user_balances[user] += amount

def setup(bot):
    bot.add_cog(BettingMatch(bot))
       
