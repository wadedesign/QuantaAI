import random
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View, Select

class TradingView(View):
    def __init__(self, ctx, stock, price, balance):
        super().__init__()
        self.ctx = ctx
        self.stock = stock
        self.price = price
        self.balance = balance

    @button(label="Buy", style=nextcord.ButtonStyle.green)
    async def buy_stock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.balance < self.price:
            await interaction.response.send_message("You don't have enough balance to buy this stock!", ephemeral=True)
            return

        self.balance -= self.price
        await interaction.response.send_message(f"You have bought {self.stock} for {self.price}! Your balance is now {self.balance}.")
        

    @button(label="Sell", style=nextcord.ButtonStyle.red)
    async def sell_stock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.balance += self.price
        await interaction.response.send_message(f"You have sold {self.stock} for {self.price}! Your balance is now {self.balance}.")
        

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stocks = {"AAPL": 150, "GOOG": 200, "TSLA": 300, "AMZN": 400, "MSFT": 250}
        self.active_games = {}

    @nextcord.slash_command(name="trading", description="Start a new game of trading")
    async def trading(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.active_games:
            await interaction.response.send_message("A game of trading is already in progress in this channel.", ephemeral=True)
            return

        stock = random.choice(list(self.stocks.keys()))
        price = self.stocks[stock]
        balance = 1000

        self.active_games[interaction.channel.id] = TradingView(interaction, stock, price, balance)

        await interaction.response.send_message("A new game of trading has started!")
        await interaction.followup.send(f"The current stock is {stock} and the price is {price}. Your balance is {balance}.", view=self.active_games[interaction.channel.id])

def setup(bot):
    bot.add_cog(Trading(bot))