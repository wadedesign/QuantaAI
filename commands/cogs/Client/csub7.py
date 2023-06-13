import json
import nextcord
from nextcord.ext import commands
from typing import Optional, List
import os
import requests

# ! Add more sub commands (Change whole file)


class Profile1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nopings = nextcord.AllowedMentions(replied_user=False)
        self.nasa_api_key = os.getenv("NASA_API_KEY")  # Replace with your NASA API key

    def split_chunks(self, input: str, chunks: int = 1990) -> List[str]:
        return [input[n:n + chunks] for n in range(0, len(input), chunks)]
    
    
    async def get_latest_launch(self):
        response = requests.get("https://api.spacexdata.com/v5/launches/latest")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception("Could not get latest launch data")

    async def get_embed_for_launch(self, launch):
        embed = nextcord.Embed(
            title=launch["mission_name"],
            description=launch["details"],
            url=launch["links"]["webcast"],
            color=0x0000FF,
        )
        embed.add_field(name="Launch Date", value=launch["launch_date_utc"])
        embed.add_field(name="Rocket", value=launch["rocket_name"])
        embed.add_field(name="Payload", value=launch["payloads"][0]["name"])
        return embed
    
    
    @nextcord.slash_command(name="sub8")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="profile1", description="Displays the user's server profile picture.")
    async def profile1(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = None):
        """
        Correct usage: /profile <user>
        Displays the user's server profile picture
        """
        if not user:
            if not isinstance(interaction.author, nextcord.Member):
                raise Exception("Invalid caller")
            user = interaction.author
        emb: nextcord.Embed = nextcord.Embed(
            title=str(user),
            type="rich"
        )
        emb.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(
            embed=emb,
            allowed_mentions=self.nopings
        )
        
    @main.subcommand(name="nasapod", description="Displays NASA's Astronomy Picture of the Day.")
    async def get_apod(self, interaction: nextcord.Interaction):
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.nasa_api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            embed = nextcord.Embed(
                title="Astronomy Picture of the Day",
                description=data["explanation"],
                color=0x00ff00
            )
            embed.set_image(url=data["url"])
            embed.set_footer(text=f"Date: {data['date']}")

            await interaction.send(embed=embed)
        
        except requests.exceptions.RequestException as e:
            await interaction.send(f"An error occurred: {str(e)}")
            
    @main.subcommand(name="neo", description="Displays NASA's Near Earth Object Web Service.")
    async def get_neo(self, interaction: nextcord.Interaction):
        url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={self.nasa_api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            neo_list = data["near_earth_objects"]
            neos = "\n".join([neo["name"] for neo in neo_list])

            embed = nextcord.Embed(
                title="Near-Earth Objects",
                description=f"List of Near-Earth Objects:\n\n{neos}",
                color=0x00ff00
            )

            await interaction.send(embed=embed)
        
        except requests.exceptions.RequestException as e:
            await interaction.send(f"An error occurred: {str(e)}")
            
    @main.subcommand(name="cme", description="Displays NASA's Coronal Mass Ejection Web Service.")
    async def get_cme(self, interaction: nextcord.Interaction, start_date, end_date):
            await interaction.send("Fetching data...")
            url = f"https://api.nasa.gov/DONKI/CME?startDate={start_date}&endDate={end_date}&api_key={self.nasa_api_key}"
            await self._fetch_and_send_data(interaction, url)

    async def _fetch_and_send_data(self, ctx, url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                # Create a text file
                with open("data/cme.txt", "w") as f:
                    f.write(json.dumps(data, indent=4))

                # Send the text file to Discord
                await ctx.send(file=nextcord.File("cme.txt"))

            except requests.exceptions.RequestException as e:
                await ctx.send(f"An error occurred: {str(e)}")
        
    @main.subcommand(name="cmeanalysis", description="Displays NASA's Coronal Mass Ejection Analysis Web Service.")
    async def get_cme_analysis(self, ctx, start_date, end_date):
        url = f"https://api.nasa.gov/DONKI/CMEAnalysis?startDate={start_date}&endDate={end_date}&mostAccurateOnly=true&speed=500&halfAngle=30&catalog=ALL&api_key={self.nasa_api_key}"
        await self._fetch_and_send_data(ctx, url)

    async def _fetch_and_send_data(self, ctx, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Create a text file
            with open("data/cmeanalysis.txt", "w") as f:
                f.write(json.dumps(data, indent=4))

            # Send the text file to Discord
            await ctx.send(file=nextcord.File("cmeanalysis.txt"))

        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")
        
    @main.subcommand(name="gst", description="Displays NASA's Geomagnetic Storm Web Service.")
    async def get_gst(self, interaction: nextcord.Interaction, start_date, end_date):
        url = f"https://api.nasa.gov/DONKI/GST?startDate={start_date}&endDate={end_date}&api_key={self.nasa_api_key}"
        await self._fetch_and_send_data(interaction, url)

    async def _fetch_and_send_data(self, ctx, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Create a text file
            with open("data/gst.txt", "w") as f:
                f.write(json.dumps(data, indent=4))

            # Send the text file to Discord
            await ctx.send(file=nextcord.File("gst.txt"))

        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")
        
    @main.subcommand(name="ips", description="Displays NASA's Interplanetary Shock Web Service.")
    async def get_ips(self, interaction: nextcord.Interaction, start_date, end_date, location, catalog):
        await interaction.send("Reaching out to NASA...")
        await interaction.send("Fetching data...")
        url = f"https://api.nasa.gov/DONKI/IPS?startDate={start_date}&endDate={end_date}&location={location}&catalog={catalog}&api_key={self.nasa_api_key}"
        await self._fetch_and_send_data(interaction, url, "ips.txt")

    async def _fetch_and_send_data(self, ctx, url, filename):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Check if the response is empty or not
            if not response.text.strip():
                await ctx.send("No data available.")
                return

            # Parse the JSON response
            data = response.json()

            # Create a text file
            with open(f"data/{filename}", "w") as f:
                f.write(json.dumps(data, indent=4))

            # Send the text file to Discord
            await ctx.send(file=nextcord.File(f"data/{filename}"))

        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")

        except ValueError as e:
            await ctx.send("An error occurred while processing the response from the API. Please try again later.")
            print(f"Error parsing JSON response: {str(e)}")
        
    @main.subcommand(name="mars_photos", description="Displays photos taken by Mars rovers.")
    async def get_mars_photos(self, interaction: nextcord.Interaction, sol: int, camera: str):
        await interaction.send("Reaching out to NASA...")
        await interaction.send("Fetching data...")
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&camera={camera}&api_key={self.nasa_api_key}"
        await self._fetch_and_send_photos(interaction, url)

    async def _fetch_and_send_photos(self, ctx, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Check if the response is empty or not
            if not response.text.strip():
                await ctx.send("No data available.")
                return

            # Parse the JSON response
            data = response.json()

            if not data.get('photos'):
                await ctx.send("No photos available.")
                return

            # Send each photo to Discord
            for photo in data['photos']:
                await ctx.send(photo['img_src'])

        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")

        except ValueError as e:
            await ctx.send("An error occurred while processing the response from the API. Please try again later.")
            print(f"Error parsing JSON response: {str(e)}")

    

def setup(bot):
    bot.add_cog(Profile1(bot))