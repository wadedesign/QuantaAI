import nextcord
from nextcord.ext import commands
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# ! Def add more sub commands (Change whole file)

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_weather_data(self, location, api_key):
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    @nextcord.slash_command()
    async def weather(self, interaction: nextcord.Interaction, location: str):
        """Get the current weather for a given location."""
        api_key = os.getenv("WEATHER_API_KEY")
        weather_data = self.get_weather_data(location, api_key)

        if weather_data:
            location_name = weather_data['location']['name']
            country = weather_data['location']['country']
            temp_c = weather_data['current']['temp_c']
            temp_f = weather_data['current']['temp_f']
            condition = weather_data['current']['condition']['text']
            humidity = weather_data['current']['humidity']
            wind_kph = weather_data['current']['wind_kph']
            uv_index = weather_data['current']['uv']

            embed = nextcord.Embed(
                title=f"Weather for {location_name}, {country}",
                description=f"{condition}",
                color=nextcord.Color.blue()
            )
            embed.add_field(name="Temperature", value=f"{temp_c}°C | {temp_f}°F", inline=True)
            embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
            embed.add_field(name="Wind Speed", value=f"{wind_kph} km/h", inline=True)
            embed.add_field(name="UV Index", value=f"{uv_index}", inline=True)
            embed.set_thumbnail(url="https://www.example.com/weather_icon.png")  # Replace with the URL of the desired thumbnail

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Failed to fetch weather data. Please try again later.")

def setup(bot):
    bot.add_cog(WeatherCog(bot))