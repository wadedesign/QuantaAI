import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
currency_collection = db["currency"]

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_currency(self, user_id):
        user_data = currency_collection.find_one({"user_id": user_id})
        if user_data:
            return user_data.get("currency", 0)
        return 0

    def add_currency(self, user_id, amount):
        user_data = currency_collection.find_one({"user_id": user_id})
        if user_data:
            current_currency = user_data.get("currency", 0)
            new_currency = current_currency + amount
            currency_collection.update_one({"user_id": user_id}, {"$set": {"currency": new_currency}})
        else:
            currency_collection.insert_one({"user_id": user_id, "currency": amount})
            new_currency = amount
        return new_currency

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            currency_per_message = 1
            self.add_currency(str(message.author.id), currency_per_message)

            # Store message data in MongoDB
            message_data = {
                "user_id": str(message.author.id),
                "message_content": message.content,
                "server_id": str(message.guild.id),
                "timestamp": message.created_at.timestamp()
            }
            currency_collection.insert_one(message_data)

    @nextcord.slash_command(name="quantaeco", description="Economy System")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(description="Check your balance")
    async def balance(self, interaction: nextcord.Interaction):
        balance = self.get_currency(str(interaction.user.id))
        embed = nextcord.Embed(title=f"{interaction.user.display_name}'s Balance", color=0x00ff00)
        embed.add_field(name="Balance", value=f"{balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @commands.has_permissions(administrator=True)
    @main.subcommand(description="Award currency to a user")
    async def award(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        if amount < 1:
            await interaction.send("Amount must be at least 1.", ephemeral=True)
            return

        new_balance = self.add_currency(str(user.id), amount)
        embed = nextcord.Embed(title=f"Awarded {amount} currency to {user.display_name}", color=0x00ff00)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @commands.has_permissions(administrator=True)
    @main.subcommand(description="Take currency from a user")
    async def take(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        if amount < 1:
            await interaction.send("Amount must be at least 1.", ephemeral=True)
            return

        current_balance = self.get_currency(str(user.id))
        if current_balance < amount:
            await interaction.send(f"{user.display_name} doesn't have enough currency.", ephemeral=True)
            return

        new_balance = self.add_currency(str(user.id), -amount)
        embed = nextcord.Embed(title=f"Took {amount} currency from {user.display_name}", color=0xff0000)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @main.subcommand(description="Transfer currency to a user")
    async def transfer(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        if amount < 1:
            await interaction.send("Amount must be at least 1.", ephemeral=True)
            return

        current_balance = self.get_currency(str(interaction.user.id))
        if current_balance < amount:
            await interaction.send("You don't have enough currency.", ephemeral=True)
            return

        new_balance_sender = self.add_currency(str(interaction.user.id), -amount)
        new_balance_receiver = self.add_currency(str(user.id), amount)

        embed = nextcord.Embed(title=f"Transferred {amount} currency to {user.display_name}", color=0xffff00)
        embed.add_field(name=f"{interaction.user.display_name}'s New Balance", value=f"{new_balance_sender} currency")
        embed.add_field(name=f"{user.display_name}'s New Balance", value=f"{new_balance_receiver} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @main.subcommand(name="buyrole",description="Buy a role")
    async def buyquanta(self, interaction: nextcord.Interaction, role: nextcord.Role):
        role_price = currency_collection.find_one({"role_id": str(role.id)})
        if not role_price:
            await interaction.send("This role is not available for purchase.", ephemeral=True)
            return

        user_balance = self.get_currency(str(interaction.user.id))
        if user_balance < role_price["price"]:
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

        new_balance = self.add_currency(str(interaction.user.id), -role_price["price"])
        embed = nextcord.Embed(title=f"Bought {role.name}", color=0x00ff00)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")

        await interaction.send(embed=embed, ephemeral=True)

    @commands.has_permissions(administrator=True)
    @main.subcommand(description="Set the price for a role")
    async def set_price(self, interaction: nextcord.Interaction, role: nextcord.Role, price: int):
        if price < 1:
            await interaction.send("Price must be at least 1.", ephemeral=True)
            return

        currency_collection.update_one({"role_id": str(role.id)}, {"$set": {"price": price}}, upsert=True)

        await interaction.send(f"Price for {role.name} set to {price} currency.", ephemeral=True)


def setup(bot):
    bot.add_cog(Currency(bot))

