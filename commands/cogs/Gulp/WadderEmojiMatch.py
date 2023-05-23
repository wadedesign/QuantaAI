
# emoji match not there sub commands



import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View, Select

class EmojiMatchView(View):
    def __init__(self, ctx, emoji_set, shuffled_emojis):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.emoji_set = emoji_set
        self.shuffled_emojis = shuffled_emojis
        self.correct_selections = 0

    async def on_timeout(self):
        await self.ctx.send("Time's up!")

    @button(label="Submit", style=nextcord.ButtonStyle.green)
    async def submit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.correct_selections == len(self.emoji_set):
            await interaction.response.send_message("Congratulations! You've matched all the emojis!")
        else:
            await interaction.response.send_message(f"Time's up! You matched {self.correct_selections} out of {len(self.emoji_set)} emojis.")
        self.stop()

class EmojiMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_list = ["🍎", "🍌", "🍇", "🍉", "🍊", "🍋", "🍍", "🥥", "🥦", "🥕"]
        self.active_games = {}

    @nextcord.slash_command(name="emojimatch", description="Start a new game of Emoji Match")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="start", description="Start a new game of Emoji Match")
    async def emojimatch_start(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.active_games:
            await interaction.response.send_message("An Emoji Match game is already in progress in this channel.", ephemeral=True)
            return

        emoji_set = random.sample(self.emoji_list, 4)
        shuffled_emojis = random.sample(emoji_set, len(emoji_set))

        self.active_games[interaction.channel.id] = EmojiMatchView(interaction, emoji_set, shuffled_emojis)

        await interaction.response.send_message("A new game of Emoji Match has started! Memorize the following emojis:")
        await interaction.followup.send(" ".join(emoji_set))
        await asyncio.sleep(10)
        await interaction.followup.send("Now, select the emojis in the correct order:", view=self.active_games[interaction.channel.id])

    @main.subcommand(name="select", description="Select an emoji in the current Emoji Match game")
    async def emojimatch_select(self, interaction: nextcord.Interaction, emoji: str):
        if interaction.channel.id not in self.active_games:
            await interaction.response.send_message("No active Emoji Match game in this channel. Start a game with /emojimatch start.", ephemeral=True)
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

def setup(bot):
    bot.add_cog(EmojiMatch(bot))

