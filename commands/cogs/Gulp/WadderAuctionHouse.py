import nextcord
from nextcord.ext import commands
from collections import defaultdict


# add admin controls, and better embeds. 
# will move under other cogs later

class AuctionSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auctions = {}
        self.inventory = defaultdict(dict)
        self.currency = defaultdict(int)


    @nextcord.slash_command(name="auction")
    async def main(self, interaction: nextcord.Interaction):
        pass



    @main.subcommand()
    async def create_item(self, interaction: nextcord.Interaction, item_name: str, starting_price: int):
        if item_name in self.auctions:
            await interaction.send("An auction with this item name already exists.")
            return

        self.auctions[item_name] = {
            "starting_price": starting_price,
            "current_bid": starting_price,
            "highest_bidder": None
        }
        await interaction.send(f"Auction created for '{item_name}' with starting price {starting_price}.")

    @main.subcommand()
    async def bid(self, interaction: nextcord.Interaction, item_name: str, bid_amount: int):
        if item_name not in self.auctions:
            await interaction.send("This auction does not exist.")
            return

        auction = self.auctions[item_name]
        if bid_amount <= auction["current_bid"]:
            await interaction.send("Your bid must be higher than the current bid.")
            return

        user_id = str(interaction.user.id)
        if bid_amount > self.currency[user_id]:
            await interaction.send("You do not have enough virtual currency to place this bid.")
            return

        auction["current_bid"] = bid_amount
        auction["highest_bidder"] = interaction.user
        await interaction.send(f"{interaction.user.mention} is now the highest bidder with {bid_amount}.")
        
    @main.subcommand()
    async def end_auction(self, interaction: nextcord.Interaction, item_name: str):
        if item_name not in self.auctions:
            await interaction.send("This auction does not exist.")
            return

        auction = self.auctions[item_name]
        winner = auction["highest_bidder"]
        if winner is None:
            await interaction.send(f"No bids were placed for '{item_name}'. The auction has been closed.")
            del self.auctions[item_name]
            return

        winner_id = str(winner.id)
        item_cost = auction["current_bid"]
        self.currency[winner_id] -= item_cost
        if item_name in self.inventory[winner_id]:
            self.inventory[winner_id][item_name] += 1
        else:
            self.inventory[winner_id][item_name] = 1

        await interaction.send(f"{winner.mention} has won the auction for '{item_name}' at {item_cost}. The item has been added to their inventory.")
        del self.auctions[item_name]

    @main.subcommand()
    async def add_currency(self, interaction: nextcord.Interaction, amount: int):
        user_id = str(interaction.user.id)
        self.currency[user_id] += amount
        await interaction.send(f"Added {amount} virtual currency to {interaction.user.mention}'s balance. New balance: {self.currency[user_id]}")

    @main.subcommand()
    async def show_inventory(self, interaction: nextcord.Interaction):
        user_id = str(interaction.user.id)
        inventory = self.inventory[user_id]

        if not inventory:
            await interaction.send("Your inventory is empty.")
            return

        inventory_display = "\n".join([f"{item}: {count}" for item, count in inventory.items()])
        await interaction.send(f"{interaction.user.mention}'s inventory:\n{inventory_display}")
    @main.subcommand()
    async def show_currency(self, interaction: nextcord.Interaction):
        user_id = str(interaction.user.id)
        balance = self.currency[user_id]
        await interaction.send(f"{interaction.user.mention}'s virtual currency balance: {balance}")
def setup(bot):
    bot.add_cog(AuctionSystem(bot))
    
    
    
    
    #This cog provides an auction system where users can bid on items using virtual currency. It allows users to create items for auctions, place bids, end auctions, add currency to their balance, and display their inventory and currency balance.

#Note that this is a basic implementation and can be improved or extended as needed.