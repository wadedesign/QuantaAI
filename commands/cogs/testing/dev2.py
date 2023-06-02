import nextcord
from nextcord.ext import commands
import requests


class Developer2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
        
    @nextcord.slash_command(name='dev4')
    async def dev4(self, interaction: nextcord.Interaction):
       pass
   
   
    @dev4.subcommand(name="taxzewr",description="Get the sales tax rate for a specific location")
    async def taxzxer(self, interaction: nextcord.Interaction, city: str, state: str, street: str, zip_code: str):
        url = "https://sales-tax-calculator.p.rapidapi.com/rates"
        payload = {
            "city": city,
            "state": state,
            "street": street,
            "zip": zip_code
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "sales-tax-calculator.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        tax_rate = response.json().get("rate", 0)

        await interaction.response.send_message(f"The sales tax rate for {city}, {state}, {zip_code} is {tax_rate}%.", ephemeral=True)
        
        
        
        
        
        
        
        
        
        
        
        
        
def setup(bot):
    bot.add_cog(Developer2(bot))