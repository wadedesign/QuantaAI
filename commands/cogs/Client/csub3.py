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
        
    @nextcord.slash_command(name="q1")
    async def q1(self, interaction: nextcord.Interaction):
        pass
    @q1.subcommand()
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
            
    @q1.subcommand(name="onlinestatus", description="Print how many people are using each type of device.")
    async def onlinestatus(self, ctx: commands.Context):
        """Print how many people are using each type of device."""
        device = {
            (True, True, True): 0,
            (False, True, True): 1,
            (True, False, True): 2,
            (True, True, False): 3,
            (False, False, True): 4,
            (True, False, False): 5,
            (False, True, False): 6,
            (False, False, False): 7,
        }
        store = [0, 0, 0, 0, 0, 0, 0, 0]
        for m in ctx.guild.members:
            value = (
                m.desktop_status == nextcord.Status.offline,
                m.web_status == nextcord.Status.offline,
                m.mobile_status == nextcord.Status.offline,
            )
            store[device[value]] += 1
        msg = (
            f"offline all: {store[0]}"
            f"\ndesktop only: {store[1]}"
            f"\nweb only: {store[2]}"
            f"\nmobile only: {store[3]}"
            f"\ndesktop web: {store[4]}"
            f"\nweb mobile: {store[5]}"
            f"\ndesktop mobile: {store[6]}"
            f"\nonline all: {store[7]}"
        )
        await ctx.send(f"```py\n{msg}```")

def setup(bot):
    bot.add_cog(WeatherCog(bot))