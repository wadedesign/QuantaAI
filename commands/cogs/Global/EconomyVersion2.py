
# want to make this better!

import json
import os
from typing import Dict

import nextcord
from nextcord.ext import commands

# ! almost ready fpr production

class Economy(commands.Cog):
    """A cog for managing an economy within a Discord server"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.currency_data = {}
        self.data_file = "data/currency_data.json"
        self.load_currency_data()

    def load_currency_data(self):
        """Load currency data from the JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.currency_data = json.load(f)

    def save_currency_data(self):
        """Save currency data to the JSON file"""
        with open(self.data_file, "w") as f:
            json.dump(self.currency_data, f)

    def get_currency(self, user_id: int) -> int:
        """Get the current balance of a user"""
        return self.currency_data.get(str(user_id), 0)

    def add_currency(self, user_id: int, amount: int) -> int:
        """Add currency to a user's balance"""
        current_currency = self.get_currency(user_id)
        new_currency = current_currency + amount
        self.currency_data[str(user_id)] = new_currency
        self.save_currency_data()
        return new_currency

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        """Award currency to users when they send a message"""
        if not message.author.bot:
            currency_per_message = 1  # Adjust this value to change how much currency is awarded per message sent
            self.add_currency(message.author.id, currency_per_message)


    @nextcord.slash_command(name="eco")
    async def main(self, interaction: nextcord.Interaction):
        pass
    
    
    @main.subcommand()
    async def cbal(self, interaction: nextcord.Interaction):
        """Get the current balance of the user who sent the command"""
        balance = self.get_currency(interaction.user.id)
        embed = nextcord.Embed(title=f"{interaction.user.display_name}'s Balance", color=0x00ff00)
        embed.add_field(name="Balance", value=f"{balance} currency")
        await interaction.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @main.subcommand()
    async def award2(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        """Add currency to a user's balance"""
        if amount < 1:
            await interaction.send("Amount must be at least 1.")
            return

        new_balance = self.add_currency(user.id, amount)
        embed = nextcord.Embed(title=f"Awarded {amount} currency to {user.display_name}", color=0x00ff00)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")
        await interaction.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @main.subcommand()
    async def take2(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        """Remove currency from a user's balance"""
        if amount < 1:
            await interaction.send("Amount must be at least 1.")
            return

        current_balance = self.get_currency(user.id)
        if current_balance < amount:
            await interaction.send(f"{user.display_name} doesn't have enough currency.")
            return

        new_balance = self.add_currency(user.id, -amount)
        embed = nextcord.Embed(title=f"Took {amount} currency from {user.display_name}", color=0xff0000)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")
        await interaction.send(embed=embed)

    @main.subcommand()
    async def transfer2(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        """Transfer currency from the user who sent the command to another user"""
        if amount < 1:
            await interaction.send("Amount must be at least 1.")
            return

        current_balance = self.get_currency(interaction.user.id)
        if current_balance < amount:
            await interaction.send(f"You don't have enough currency.")
            return

        new_balance_sender = self.add_currency(interaction.user.id, -amount)
        new_balance_receiver = self.add_currency(user.id, amount)

        embed = nextcord.Embed(title=f"Transferred {amount} currency to {user.display_name}", color=0xffff00)
        embed.add_field(name=f"{interaction.user.display_name}'s New Balance", value=f"{new_balance_sender} currency")
        embed.add_field(name=f"{user.display_name}'s New Balance", value=f"{new_balance_receiver} currency")
        await interaction.send(embed=embed)

    @main.subcommand()
    async def curlead(self, interaction: nextcord.Interaction):
        """Show the leaderboard of users with the most currency"""
        sorted_data = sorted(self.currency_data.items(), key=lambda x: x[1], reverse=True)
        top_10 = sorted_data[:10]

        embed = nextcord.Embed(title="Leaderboard", color=0x00ff00)
        for i, (user_id, balance) in enumerate(top_10):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{i+1}. {user.display_name}", value=f"{balance} currency", inline=False)

        await interaction.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, interaction: nextcord.Interaction, error: commands.CommandError):
        """Handle errors related to missing arguments or incorrect input"""
        if isinstance(error, commands.MissingRequiredArgument):
            await interaction.send("Missing required argument.")
        elif isinstance(error, commands.BadArgument):
            await interaction.send("Invalid argument.")
            
def setup(bot):
    bot.add_cog(Economy(bot))