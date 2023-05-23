import asyncio
import nextcord
from nextcord.ext import commands, tasks
from pycoingecko import CoinGeckoAPI

class CryptoPrice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cg = CoinGeckoAPI()
        self.crypto_channel = None
        self.ticker_message = None
        self.ticker_task.start()

    async def create_crypto_channel(self, guild):
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        }
        channel_name = "💰crypto-prices"
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        return channel

    async def fetch_crypto_prices(self):
        coins_list = ["bitcoin", "ethereum", "binancecoin", "cardano", "ripple"]
        coins_data = self.cg.get_price(ids=coins_list, vs_currencies="usd")
        return coins_data

    async def format_prices_embed(self, coins_data):
        embed = nextcord.Embed(title="Crypto Prices", color=0x2ecc71)
        for coin, data in coins_data.items():
            price = round(data["usd"], 2)
            embed.add_field(name=coin.capitalize(), value=f"${price}", inline=True)
        return embed

    @tasks.loop(seconds=25)
    async def ticker_task(self):
        if self.crypto_channel is None or self.ticker_message is None:
            return

        try:
            coins_data = await self.fetch_crypto_prices()
            formatted_prices_embed = await self.format_prices_embed(coins_data)
            await self.ticker_message.edit(embed=formatted_prices_embed)
        except Exception as e:
            print(f"Error fetching crypto prices: {e}")

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)
    async def create_crypto_ticker(self, interaction: nextcord.Interaction):
        if self.crypto_channel is not None:
            await interaction.send("A crypto ticker channel already exists.")
            return

        self.crypto_channel = await self.create_crypto_channel(interaction.guild)
        coins_data = await self.fetch_crypto_prices()
        formatted_prices_embed = await self.format_prices_embed(coins_data)
        self.ticker_message = await self.crypto_channel.send(embed=formatted_prices_embed)
        await interaction.send(f"Crypto ticker channel created: {self.crypto_channel.mention}")

def setup(bot):
    bot.add_cog(CryptoPrice(bot))