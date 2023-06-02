import csv
import io
import json
import os
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

            formatted_weather_history = ""
            for row in reader:
                formatted_row = ""
                for key, value in row.items():
                    formatted_row += f"{key}: {value}\n"
                formatted_weather_history += f"\n{formatted_row}"

            # Save the weather history to a file
            filename = "weather_history.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(formatted_weather_history)

            # Send the file as an attachment
            with open(filename, "rb") as file:
                file_data = io.BytesIO(file.read())
                file_data.seek(0)

                await interaction.response.send_message(
                    content=f"Weather history for {location} from {start_date} to {end_date}",
                    ephemeral=True,
                    file=nextcord.File(file_data, filename=filename)
                )

            # Remove the file after sending
            os.remove(filename)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while fetching the weather history. Error: {str(e)}", ephemeral=True)
            print(response.content)  # Print the response content for troubleshooting purposes
            
        
    @dev4.subcommand(description="Get current astrological information")
    async def astro_info(self, interaction: nextcord.Interaction):
        url = "https://astrologer.p.rapidapi.com/api/v3/now"

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "astrologer.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        # Extract the relevant information from the response
        sun = data["data"]["sun"]
        moon = data["data"]["moon"]
        mercury = data["data"]["mercury"]
        venus = data["data"]["venus"]
        mars = data["data"]["mars"]
        jupiter = data["data"]["jupiter"]
        saturn = data["data"]["saturn"]
        uranus = data["data"]["uranus"]
        neptune = data["data"]["neptune"]
        pluto = data["data"]["pluto"]

        # Build the response message
        message = "Current astrological information:\n\n"
        message += f"Sun Sign: {sun['sign']}\n"
        message += f"Moon Sign: {moon['sign']}\n"
        message += f"Mercury Sign: {mercury['sign']}\n"
        message += f"Venus Sign: {venus['sign']}\n"
        message += f"Mars Sign: {mars['sign']}\n"
        message += f"Jupiter Sign: {jupiter['sign']}\n"
        message += f"Saturn Sign: {saturn['sign']}\n"
        message += f"Uranus Sign: {uranus['sign']}\n"
        message += f"Neptune Sign: {neptune['sign']}\n"
        message += f"Pluto Sign: {pluto['sign']}"

        # Send the message
        await interaction.response.send_message(message, ephemeral=True)
        
    @dev4.subcommand(description="Get Astronomy Picture of the Day")
    async def apod(self, interaction: nextcord.Interaction):
        url = "https://astronomy-picture-of-the-day.p.rapidapi.com/apod"

        querystring = {
            "api_key": "nWYhQQdmCKwd0cVvrfyge124OrW4fnVOEL7QDdJH"
        }

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "astronomy-picture-of-the-day.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Extract the relevant information from the response
        image_title = data.get("title")
        image_url = data.get("url")
        image_explanation = data.get("explanation", "No explanation available.")

        # Build the response message
        message = f"Astronomy Picture of the Day:\n\n"
        message += f"Title: {image_title}\n"
        message += f"Explanation: {image_explanation}"

        # Send the message with the image URL as an embed
        embed = nextcord.Embed(title=image_title, description=image_explanation)
        embed.set_image(url=image_url)

        await interaction.response.send_message(content=message, embed=embed, ephemeral=True)
            
        
def setup(bot):
    bot.add_cog(Developer2(bot))