import csv
import io
import json
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
        
    @dev4.subcommand(description="Get the tax information for a cryptocurrency transaction")
    async def crypto_tax(self, interaction: nextcord.Interaction, address: str, country: str, sell_amount: float):
        url = "https://cryptotax.p.rapidapi.com/"
        querystring = {
            "address": address,
            "country": country,
            "sell": str(sell_amount)
        }
        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "cryptotax.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        tax_info = response.json()

        await interaction.response.send_message(f"Tax information for address {address}:\n{tax_info}", ephemeral=True)
        
        
    @dev4.subcommand(description="Get the weather forecast summary for a specific location") # wip
    async def weather_summary(self, interaction: nextcord.Interaction, location: str):
        url = f"https://forecast9.p.rapidapi.com/rapidapi/forecast/{location}/summary/"
        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "forecast9.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        weather_summary = response.json().get("summary", "No information available")

        await interaction.response.send_message(f"The weather forecast summary for {location}:\n{weather_summary}", ephemeral=True)
        
        
        
    @dev4.subcommand(description="Get the weather history for a specific location")
    async def weather_history(self, interaction: nextcord.Interaction, start_date: str, end_date: str, location: str):
        url = "https://visual-crossing-weather.p.rapidapi.com/history"
        querystring = {
            "startDateTime": start_date,
            "aggregateHours": "24",
            "location": location,
            "endDateTime": end_date,
            "unitGroup": "us",
            "dayStartTime": "8:00:00",
            "contentType": "csv",
            "dayEndTime": "17:00:00",
            "shortColumnNames": "0"
        }
        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        try:
            weather_history_csv = response.content.decode("utf-8")
            reader = csv.DictReader(weather_history_csv.splitlines())
            
            formatted_weather_history = io.StringIO()  # Use StringIO to build the formatted output
            for row in reader:
                formatted_row = ""
                for key, value in row.items():
                    formatted_row += f"{key}: {value}\n"
                formatted_weather_history.write(formatted_row + "\n")
            
            # Create a file with the weather history data
            weather_history_file = nextcord.File(formatted_weather_history.getvalue(), filename="weather_history.txt")
            
            # Send the message with the file attachment
            await interaction.response.send_message(
                f"Weather history for {location} from {start_date} to {end_date}",
                ephemeral=True,
                files=[weather_history_file]
            )
            
            formatted_weather_history.close()  # Close the StringIO object
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while fetching the weather history. Error: {str(e)}", ephemeral=True)
            print(response.content)  # Print the response content for troubleshooting purposes
            
        
def setup(bot):
    bot.add_cog(Developer2(bot))