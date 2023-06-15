import asyncio
import nextcord
from nextcord.ext import commands, tasks
import aiohttp
from nextcord.ui import Button, View
import json
import os
import random
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
players_collection = db["players"]
stocks_collection = db["stocks"]
bank_collection = db["bank"]

class StockMarketGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.load_players()
        self.stocks = {}
        self.load_stocks()
        self.update_interests.start()
        self.bank = {"balance": 1000000, "loan_interest": 0.05, "savings_interest": 0.02}
        self.load_bank()
        self.update_stock_prices.start()

    async def get_top_stocks(self, limit=50):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1000000000&limit={limit}&apikey=demo") as response:
                data = await response.json()
        return [stock["symbol"] for stock in data]
    
    async def get_random_stock(self):
        stock_symbols = list(self.stocks.keys())
        return random.choice(stock_symbols)
    
    def cog_unload(self):
        self.update_stock_prices.cancel()
    
    def save_players(self):
        players_collection.update_many({}, {"$set": self.players})
    
    def load_players(self):
        players = players_collection.find({})
        self.players = {str(player["_id"]): player["data"] for player in players}
    
    def save_stocks(self):
        stocks_collection.update_many({}, {"$set": self.stocks})
    
    def load_stocks(self):
        stocks = stocks_collection.find({})
        self.stocks = {stock["_id"]: stock["data"] for stock in stocks}
    
    def save_bank(self):
        bank_collection.update_one({"_id": "bank"}, {"$set": self.bank}, upsert=True)
    
    def load_bank(self):
        bank = bank_collection.find_one({"_id": "bank"})
        if bank:
            self.bank = bank["data"]
    
    @tasks.loop(minutes=1)
    async def update_stock_prices(self):
        top_stocks = await self.get_top_stocks()
        async with aiohttp.ClientSession() as session:
            for stock in top_stocks:
                async with session.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey=demo") as response:
                    data = (await response.json())[0]
                self.stocks[stock] = {"price": data["price"], "name": data["name"], "changePercent": data["changesPercentage"]}
        self.save_stocks()
    
    @tasks.loop(minutes=30)  # You can change the interval to your preference
    async def update_interests(self):
        for player_id, player_data in self.players.items():
            player_data["savings"] *= (1 + self.bank["savings_interest"])
            player_data["loan"] *= (1 + self.bank["loan_interest"])
        self.save_players()
    
    def is_admin():
        async def predicate(ctx):
            return ctx.author.guild_permissions.administrator
        return commands.check(predicate)
    
    def calculate_net_worth(self, player_data):
        net_worth = player_data["balance"] + player_data["savings"] - player_data["loan"]
        for stock, quantity in player_data["portfolio"].items():
            net_worth += self.stocks[stock]["price"] * quantity
        return net_worth
    
    @nextcord.slash_command(name="mk", description="Start a new game of Number Guess")
    async def main(self, interaction: nextcord.Interaction):
        pass
    
    @main.subcommand()
    async def stocks(self, interaction: nextcord.Interaction):
        stocks_list = [f"{stock}: {self.stocks[stock]['name']} (${self.stocks[stock]['price']:.2f})" for stock in self.stocks]
        await interaction.send("Available stocks:\n" + "\n".join(stocks_list))

    @main.subcommand()
    async def mk_stock_info(self, interaction: nextcord.Interaction, symbol: str):
        if symbol not in self.stocks:
            await interaction.send("That stock symbol is not available for trading.")
        else:
            stock_info = self.stocks[symbol]
            await interaction.send(f"{symbol}: {stock_info['name']} (${stock_info['price']:.2f})")

    @main.subcommand()
    async def mk_join_game(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id in self.players:
            await interaction.send("You have already joined the game.")
        else:
            self.players[player_id] = {"balance": 100000, "portfolio": {}, "savings": 0, "loan": 0}
            await interaction.send(f"Welcome to the game, {interaction.user.mention}! You have been given $100,000 to start trading.")
            self.save_players()
    @main.subcommand()
    async def mk_save_money(self, interaction: nextcord.Interaction, amount: float):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        elif amount <= 0:
            await interaction.send("Amount must be positive.")
        elif amount > self.players[player_id]["balance"]:
            await interaction.send("You do not have enough funds to save this amount.")
        else:
            self.players[player_id]["balance"] -= amount
            self.players[player_id]["savings"] += amount
            await interaction.send(f"You have successfully saved ${amount:.2f}.")
            self.save_players()
    @main.subcommand()
    async def mk_take_loan(self, interaction: nextcord.Interaction, amount: float):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        elif amount <= 0:
            await interaction.send("Amount must be positive.")
        elif amount > self.bank["balance"]:
            await interaction.send("The bank does not have enough funds to give you this loan.")
        else:
            self.bank["balance"] -= amount
            self.players[player_id]["balance"] += amount
            self.players[player_id]["loan"] += amount * (1 + self.bank["loan_interest"])
            await interaction.send(f"You have successfully taken a loan of ${amount:.2f}. You need to pay back ${amount * (1 + self.bank['loan_interest']):.2f}.")
            self.save_players()
    @main.subcommand()
    async def mk_pay_loan(self, interaction: nextcord.Interaction, amount: float):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        elif amount <= 0:
            await interaction.send("Amount must be positive.")
        elif amount > self.players[player_id]["balance"]:
            await interaction.send("You do not have enough funds to pay back this amount.")
        elif amount > self.players[player_id]["loan"]:
            await interaction.send("You are trying to pay back more than you owe.")
        else:
            self.players[player_id]["balance"] -= amount
            self.players[player_id]["loan"] -= amount
            await interaction.send(f"You have successfully paid back ${amount:.2f} of your loan.")
            self.save_players()
    @main.subcommand()
    @is_admin()
    async def mk_bank_balance(self, interaction: nextcord.Interaction):
        balance = self.bank["balance"]
        await interaction.send(f"Bank balance: ${balance:.2f}")
    
    
    @main.subcommand()
    @is_admin()
    async def mk_set_bank_balance(self, interaction: nextcord.Interaction, amount: float):
        if amount < 0:
            await interaction.send("Bank balance cannot be negative.")
        else:
            self.bank["balance"] = amount
            await interaction.send(f"Bank balance has been set to ${amount:.2f}.")

    @main.subcommand()
    @is_admin()
    async def mk_set_interest_rates(self, interaction: nextcord.Interaction, loan_interest: float, savings_interest: float):
        if loan_interest < 0 or savings_interest < 0:
            await interaction.send("Interest rates cannot be negative.")
        else:
            self.bank["loan_interest"] = loan_interest
            self.bank["savings_interest"] = savings_interest
            await interaction.send(f"Loan interest rate has been set to {loan_interest * 100:.2f}% and savings interest rate has been set to {savings_interest * 100:.2f}%.")

    @main.subcommand()
    async def mk_buy_stock(self, interaction: nextcord.Interaction, symbol: str, quantity: int):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        elif symbol not in self.stocks:
            await interaction.send("That stock symbol is not available for trading.")
        else:
            price = self.stocks[symbol]["price"]
            cost = price * quantity
            if cost > self.players[player_id]["balance"]:
                await interaction.send("You do not have enough funds to buy this many shares.")
            else:
                self.players[player_id]["balance"] -= cost
                if symbol in self.players[player_id]["portfolio"]:
                    self.players[player_id]["portfolio"][symbol] += quantity
                else:
                    self.players[player_id]["portfolio"][symbol] = quantity
                await interaction.send(f"You have successfully bought {quantity} shares of {symbol} for ${cost:.2f}.")
                self.save_players()
    @main.subcommand()
    async def mk_sell_stock(self, interaction: nextcord.Interaction, symbol: str, quantity: int):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        elif symbol not in self.stocks:
            await interaction.send("That stock symbol is not available for trading.")
        elif symbol not in self.players[player_id]["portfolio"]:
            await interaction.send("You do not have any shares of this stock to sell.")
        elif quantity > self.players[player_id]["portfolio"][symbol]:
            await interaction.send("You do not have this many shares to sell.")
        else:
            price = self.stocks[symbol]["price"]
            proceeds = price * quantity
            self.players[player_id]["balance"] += proceeds
            self.players[player_id]["portfolio"][symbol] -= quantity
            if self.players[player_id]["portfolio"][symbol] == 0:
                del self.players[player_id]["portfolio"][symbol]
            await interaction.send(f"You have successfully sold {quantity} shares of {symbol} for ${proceeds:.2f}.")
            self.save_players()
    @main.subcommand()
    async def mk_portfolio(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        else:
            portfolio = self.players[player_id]["portfolio"]
            portfolio_list = [f"{symbol}: {quantity} shares (${self.stocks[symbol]['price'] * quantity:.2f})" for symbol, quantity in portfolio.items()]
            loan_amount = self.players[player_id]["loan"]

            if not portfolio_list:
                await interaction.send("Your portfolio is empty.")
            else:
                await interaction.send("Your portfolio:\n" + "\n".join(portfolio_list) + f"\nLoan amount: ${loan_amount:.2f}")
                self.save_players()
    @main.subcommand()
    async def mk_pbal(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        else:
            balance_embed = nextcord.Embed(title="Your Balance", description=f"${self.players[player_id]['balance']:.2f}", color=0x00ff00)
            await interaction.send(embed=balance_embed)
            self.save_players()
    @main.subcommand()
    async def mk_leaderboard(self, interaction: nextcord.Interaction):
        sorted_players = sorted(self.players.items(), key=lambda x: self.calculate_net_worth(x[1]), reverse=True)
        leaderboard = []
        for player_id, player_data in sorted_players:
            user = self.bot.get_user(int(player_id))
            net_worth = self.calculate_net_worth(player_data)
            leaderboard.append(f"{user.display_name}: ${net_worth:.2f}")

        embed = nextcord.Embed(title="Stock Market Game Leaderboard", description="\n".join(leaderboard), color=0x00ff00)
        await interaction.send(embed=embed)
    
    @main.subcommand()
    async def mk_leave_game(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        else:
            del self.players[player_id]
            await interaction.send(f"You have left the game, {interaction.user.mention}. All your progress has been lost.")
            self.save_players()
            
            
    @main.subcommand()
    async def mk_loan_status(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        else:
            loan_amount = self.players[player_id]["loan"]
            await interaction.send(f"Your current loan amount: ${loan_amount:.2f}")
            
            
    @main.subcommand()
    async def mk_savings_status(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        else:
            savings_amount = self.players[player_id]["savings"]
            await interaction.send(f"Your current savings balance: ${savings_amount:.2f}")  
            
            
            
    @main.subcommand()
    async def mk_withdraw_savings(self, interaction: nextcord.Interaction, amount: float):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        elif amount <= 0:
            await interaction.send("Amount must be positive.")
        elif amount > self.players[player_id]["savings"]:
            await interaction.send("You do not have enough funds in your savings to withdraw this amount.")
        else:
            self.players[player_id]["savings"] -= amount
            self.players[player_id]["balance"] += amount
            await interaction.send(f"You have successfully withdrawn ${amount:.2f} from your savings.")
            self.save_players()              




    @main.subcommand()
    async def mk_top_movers(self, interaction: nextcord.Interaction):
        top_gainers = sorted(self.stocks.items(), key=lambda x: x[1]["changePercent"], reverse=True)[:5]
        top_losers = sorted(self.stocks.items(), key=lambda x: x[1]["changePercent"])[:5]

        gainers_list = [f"{stock[0]}: {stock[1]['name']} (${stock[1]['price']:.2f}, {stock[1]['changePercent']:.2f}%)" for stock in top_gainers]
        losers_list = [f"{stock[0]}: {stock[1]['name']} (${stock[1]['price']:.2f}, {stock[1]['changePercent']:.2f}%)" for stock in top_losers]

        await interaction.send("Top Gainers:\n" + "\n".join(gainers_list))
        await interaction.send("Top Losers:\n" + "\n".join(losers_list))





    @main.subcommand()
    async def mk_stock_history(self, interaction: nextcord.Interaction, symbol: str, days: int = 7):
        if symbol not in self.stocks:
            await interaction.send("Invalid stock symbol.")
        else:
            history = await self.get_stock_history(symbol, days)
            history_list = [f"{date}: ${price:.2f}" for date, price in history.items()]
            await interaction.send(f"{self.stocks[symbol]['name']} ({symbol}) price history:\n" + "\n".join(history_list))

    @main.subcommand()
    async def mk_liquidate_and_reset(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
        else:
            player_data = self.players[player_id]
            total_value = player_data["balance"]

            for stock_symbol, quantity in player_data["portfolio"].items():
                total_value += self.stocks[stock_symbol]["price"] * quantity

            self.players[player_id] = {"balance": total_value, "portfolio": {}, "savings": 0, "loan": 0}
            await interaction.send(f"{interaction.user.name}, you have liquidated all your stocks and reset your game progress. Your new balance is ${total_value:.2f}.")
            self.save_players()




    @main.subcommand()
    async def mk_stock_challenge(self, interaction: nextcord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            await interaction.send("You have not joined the game yet.")
            return

        stock1 = await self.get_random_stock()
        stock2 = await self.get_random_stock()
        while stock1 == stock2:
            stock2 = await self.get_random_stock()

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel and message.content.lower() in (stock1.lower(), stock2.lower())

        await interaction.send(f"Which stock will perform better in the next minute? Type your answer:\n1. {stock1}: {self.stocks[stock1]['name']}\n2. {stock2}: {self.stocks[stock2]['name']}")

        try:
            user_guess = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await interaction.send("You didn't respond in time!")
            return

        guessed_stock = user_guess.content.upper()
        initial_price1 = self.stocks[stock1]["price"]
        initial_price2 = self.stocks[stock2]["price"]

        await asyncio.sleep(60)

        final_price1 = self.stocks[stock1]["price"]
        final_price2 = self.stocks[stock2]["price"]

        performance1 = (final_price1 - initial_price1) / initial_price1
        performance2 = (final_price2 - initial_price2) / initial_price2

        if (guessed_stock == stock1 and performance1 > performance2) or (guessed_stock == stock2 and performance2 > performance1):
            reward = 100
            self.players[player_id]["balance"] += reward
            await interaction.send(f"Congratulations! You guessed correctly and earned ${reward:.2f}.")
        else:
            await interaction.send(f"Sorry, your guess was incorrect. Better luck next time!")



def setup(bot):
    bot.add_cog(StockMarketGame(bot))