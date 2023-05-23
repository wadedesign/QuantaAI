import random
import asyncio
import nextcord
from nextcord.ext import commands
from collections import defaultdict

# Dummy data for store items and stocks
store_items = {
    'apple': 10,
    'banana': 15,
    'carrot': 5,
    'chicken': 25,
    'beef': 35,
    'pork': 30,
    'bread': 12,
    'eggs': 8,
    'milk': 5,
    'water': 2
}

stock_market = {
    'TSLA': 500,
    'AAPL': 150,
    'AMZN': 3000,
    'GOOG': 2000,
    'FB': 300,
    'NFLX': 500,
    'NVDA': 800,
    'PYPL': 250,
    'SQ': 150,
    'SHOP': 1000
}


# Dummy data for job listings
job_listings = {
    'teacher': 100,
    'developer': 200,
    'police': 150,
    'nurse': 120,
    'salesperson': 80,
    'accountant': 180,
    'designer': 150,
    'writer': 90,
    'chef': 110,
    'mechanic': 100
}

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = defaultdict(lambda: {'balance': 0, 'job': None, 'stocks': {}})
        self.market_open = False
    
    @nextcord.slash_command(name="weco")
    async def main(self, interaction: nextcord.Interaction):
        pass
    @main.subcommand(description="check your balance")
    async def balance2(self, interaction: nextcord.Interaction):
        balance = self.users[interaction.user.id]['balance']
        await interaction.send(f'{interaction.user.name}, your balance is: ${balance}')

    @main.subcommand(description="job listings")
    async def job2(self, interaction: nextcord.Interaction, job_name: str = None):
        if job_name is None:
            job_list = '\n'.join([f"{job} - ${salary}" for job, salary in job_listings.items()])
            await interaction.send(f'Available jobs:\n{job_list}')
        else:
            if job_name in job_listings:
                self.users[interaction.user.id]['job'] = job_name
                await interaction.send(f'{interaction.user.name}, you have been hired as a {job_name}.')
            else:
                await interaction.send(f'{interaction.user.name}, the job {job_name} does not exist.')

    @main.subcommand(description="work for your job")
    async def work2(self, interaction: nextcord.Interaction):
        user = self.users[interaction.user.id]
        if user['job'] is not None:
            salary = job_listings[user['job']]
            user['balance'] += salary
            await interaction.send(f'{interaction.user.name}, you have earned ${salary} working as a {user["job"]}. Your new balance is ${user["balance"]}.')
        else:
            await interaction.send(f'{interaction.user.name}, you need to get a job first.')

    @main.subcommand(description="store items")
    async def store2(self, interaction: nextcord.Interaction):
        items = '\n'.join([f'{item} - ${price}' for item, price in store_items.items()])
        await interaction.send(f'Items available in the store:\n{items}')

    @main.subcommand(description="buy an item from the store")
    async def buy2(self, interaction: nextcord.Interaction, item_name: str, quantity: int):
        if item_name in store_items:
            cost = store_items[item_name] * quantity
            user = self.users[interaction.user.id]
            if user['balance'] >= cost:
                user['balance'] -= cost
                await interaction.send(f'{interaction.user.name}, you have purchased {quantity} {item_name}(s) for ${cost}. Your new balance is ${user["balance"]}.')
            else:
                await interaction.send(f'{interaction.user.name}, you do not have enough money to buy {quantity} {item_name}(s).')
        else:
            await interaction.send(f'{interaction.user.name}, the item {item_name} does not exist.')

    @main.subcommand(description="stock markets")
    async def stock2(self, interaction: nextcord.Interaction, stock_name: str = None):
        if stock_name is None:
            stocks = '\n'.join([f'{stock} - ${price}' for stock, price in stock_market.items()])
            await interaction.send(f'Stocks available in the market:\n{stocks}')
        elif stock_name in stock_market:
            price = stock_market[stock_name]
            await interaction.send(f'{interaction.user.name}, the current price of {stock_name} is ${price}.')
        else:
            await interaction.send(f'{interaction.user.name}, the stock {stock_name} does not exist.')

    @main.subcommand(description="buy a stock from the market")
    async def buy_stock2(self, interaction: nextcord.Interaction, stock_name: str, quantity: int):
        if stock_name in stock_market:
            price = stock_market[stock_name]
            cost = price * quantity
            user = self.users[interaction.user.id]
            if user['balance'] >= cost:
                user['balance'] -= cost
                if stock_name in user['stocks']:
                    user['stocks'][stock_name] += quantity
                else:
                    user['stocks'][stock_name] = quantity
                await interaction.send(f'{interaction.user.name}, you have purchased {quantity} share(s) of {stock_name} for ${cost}. Your new balance is ${user["balance"]}.')
            else:
                await interaction.send(f'{interaction.user.name}, you do not have enough money to buy {quantity} share(s) of {stock_name}.')
        else:
            await interaction.send(f'{interaction.user.name}, the stock {stock_name} does not exist.')

    @main.subcommand(description="sell a stock from the market")
    async def sell_stock2(self, interaction: nextcord.Interaction, stock_name: str, quantity: int):
        if stock_name in stock_market:
            price = stock_market[stock_name]
            user = self.users[interaction.user.id]
            if stock_name in user['stocks'] and user['stocks'][stock_name] >= quantity:
                user['stocks'][stock_name] -= quantity
                user['balance'] += price * quantity
                await interaction.send(f'{interaction.user.name}, you have sold {quantity} share(s) of {stock_name} for ${price * quantity}. Your new balance is ${user["balance"]}.')
            else:
                await interaction.send(f'{interaction.user.name}, you do not have enough shares of {stock_name} to sell {quantity}.')
        else:
            await interaction.send(f'{interaction.user.name}, the stock {stock_name} does not exist.')

    @main.subcommand(description="open the market")
    async def open_market(self, interaction: nextcord.Interaction):
        if self.market_open:
            await interaction.send(f'{interaction.user.name}, the market is already open.')
        else:
            self.market_open = True
            await interaction.send(f'{interaction.user.name}, the market is now open.')

            # Start a background task to update stock prices every minute
            async def update_stocks():
                while self.market_open:
                    for stock in stock_market:
                        change = random.uniform(-0.05, 0.05)
                        price = int(stock_market[stock] * (1 + change))
                        if price <= 0:
                            price = 1
                        stock_market[stock] = price
                    await asyncio.sleep(60)

            self.bot.loop.create_task(update_stocks())

    @main.subcommand(description="close the market")
    async def close_market(self, interaction: nextcord.Interaction):
        if not self.market_open:
            await interaction.send(f'{interaction.user.name}, the market is already closed.')
        else:
            self.market_open = False
            await interaction.send(f'{interaction.user.name}, the market is now closed.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return # Ignore messages from bots
        
        
        
    @main.subcommand(description="leaderboards")
    async def leaderboard23(self, interaction: nextcord.Interaction):
        sorted_users = sorted(self.users.items(), key=lambda x: x[1]['balance'], reverse=True)
        leaderboard = '\n'.join([f'{idx+1}. {self.bot.get_user(user[0]).name}: ${user[1]["balance"]}' for idx, user in enumerate(sorted_users)])
        await interaction.send(f'Leaderboard:\n{leaderboard}')


def setup(bot):
    bot.add_cog(EconomyCog(bot))