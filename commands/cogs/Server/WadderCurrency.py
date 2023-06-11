import json
import os

import nextcord
from nextcord.ext import commands

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currency_data = {}
        self.data_file = "data/currency_data.json"
        self.load_currency_data()

    def load_currency_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.currency_data = json.load(f)

    def save_currency_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.currency_data, f)

    def get_currency(self, user_id):
        return self.currency_data.get(str(user_id), 0)

    def add_currency(self, user_id, amount):
        current_currency = self.get_currency(user_id)
        new_currency = current_currency + amount
        self.currency_data[str(user_id)] = new_currency
        self.save_currency_data()
        return new_currency

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            currency_per_message = 1
            self.add_currency(message.author.id, currency_per_message)

    @nextcord.slash_command(name="quantaeco", description="Economy System")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(description="Check your balance")
    async def balance(self, interaction: nextcord.Interaction):
        balance = self.get_currency(interaction.user.id)
        embed = nextcord.Embed(title=f"{interaction.user.display_name}'s Balance", color=0x00ff00)
        embed.add_field(name="Balance", value=f"{balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @commands.has_permissions(administrator=True)
    @main.subcommand(description="Award currency to a user")
    async def award(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        if amount < 1:
            await interaction.send("Amount must be at least 1.", ephemeral=True)
            return

        new_balance = self.add_currency(user.id, amount)
        embed = nextcord.Embed(title=f"Awarded {amount} currency to {user.display_name}", color=0x00ff00)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @commands.has_permissions(administrator=True)
    @main.subcommand(description="Take currency from a user")
    async def take(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        if amount < 1:
            await interaction.send("Amount must be at least 1.", ephemeral=True)
            return

        current_balance = self.get_currency(user.id)
        if current_balance < amount:
            await interaction.send(f"{user.display_name} doesn't have enough currency.", ephemeral=True)
            return

        new_balance = self.add_currency(user.id, -amount)
        embed = nextcord.Embed(title=f"Took {amount} currency from {user.display_name}", color=0xff0000)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @main.subcommand(description="Transfer currency to a user")
    async def transfer(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        if amount < 1:
            await interaction.send("Amount must be at least 1.", ephemeral=True)
            return

        current_balance = self.get_currency(interaction.user.id)
        if current_balance < amount:
            await interaction.send("You don't have enough currency.", ephemeral=True)
            return

        new_balance_sender = self.add_currency(interaction.user.id, -amount)
        new_balance_receiver = self.add_currency(user.id, amount)

        embed = nextcord.Embed(title=f"Transferred {amount} currency to {user.display_name}", color=0xffff00)
        embed.add_field(name=f"{interaction.user.display_name}'s New Balance", value=f"{new_balance_sender} currency")
        embed.add_field(name=f"{user.display_name}'s New Balance", value=f"{new_balance_receiver} currency")

        await interaction.send(embed=embed, ephemeral=True)
        
    @main.subcommand(name="buyrole",description="Buy a role")
    async def buyquanta(self, interaction: nextcord.Interaction, role: nextcord.Role):
        role_price = self.currency_data.get("role_prices", {}).get(str(role.id))
        if role_price is None:
            await interaction.send("This role is not available for purchase.", ephemeral=True)
            return

        user_balance = self.get_currency(interaction.user.id)
        if user_balance < role_price:
            await interaction.send("You don't have enough currency to buy this role.", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        if role in member.roles:
            await interaction.send("You already have this role.", ephemeral=True)
            return

        try:
            await member.add_roles(role)
        except nextcord.HTTPException:
            await interaction.send("Failed to add the role. Please check the bot's role hierarchy.", ephemeral=True)
            return

        new_balance = self.add_currency(interaction.user.id, -role_price)
        embed = nextcord.Embed(title=f"Bought {role.name}", color=0x00ff00)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")

        await interaction.send(embed=embed, ephemeral=True)
        
    @commands.has_permissions(administrator=True)
    @main.subcommand(description="Set the price for a role")
    async def set_price(self, interaction: nextcord.Interaction, role: nextcord.Role, price: int):
        if price < 1:
            await interaction.send("Price must be at least 1.", ephemeral=True)
            return

        self.currency_data.setdefault("role_prices", {})
        self.currency_data["role_prices"][str(role.id)] = price
        self.save_currency_data()

        await interaction.send(f"Price for {role.name} set to {price} currency.", ephemeral=True)


def setup(bot):
    bot.add_cog(Currency(bot))
