import asyncio
import datetime
import difflib
import io
import json
import os
import sqlite3
import nextcord
from nextcord.ext import commands
from newspaper import Article
import requests
from utils.WF0.functions import convert_sec_to_min, get_flag, get_p, get_status
from io import BytesIO
from utils.WF0.converters import TimeConverter

import humanize
# !Add more sub commands (Change whole file)


timezones_file = 'data/timezones.json'
def load_afk_data():
            if not os.path.exists("data/afker_data.json"):
                with open("data/afker_data.json", "w") as f:
                    json.dump({}, f)

            with open("data/afker_data.json", "r") as f:
                return json.load(f)


def save_afk_data(data):
        with open("data/afker_data.json", "w") as f:
            json.dump(data, f)



async def fetch_game_deals():
    url = "https://store.steampowered.com/api/featuredcategories"
    params = {
        "cc": "US",
        "l": "en",
        "v": 1,
        "tag": "specials",
        "count": 20
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["specials"]["items"]


async def send_new_deals(channel, old_deals, new_deals):
    for game in new_deals:
        if game not in old_deals:
            embed = nextcord.Embed(title=game['name'], color=0x00ff00)
            if game["discount_percent"] > 0:
                discount_price = game.get("discount_final_price_formatted")
                embed.add_field(name=f"{game['discount_percent']}% off", value=f"{discount_price}", inline=False)
            else:
                embed.add_field(name="Free to play!", value="\u200b", inline=False)

            image_url = game["header_image"]
            image_data = requests.get(image_url).content
            image_file = nextcord.File(io.BytesIO(image_data), filename="image.png")
            embed.set_image(url="attachment://image.png")

            await channel.send(embed=embed, file=image_file)

# Helper function to load existing timezones from the JSON file
def load_timezones():
    if os.path.exists(timezones_file):
        with open(timezones_file, 'r') as file:
            return json.load(file)
    else:
        return {}

# Helper function to save timezones to the JSON file
def save_timezones(timezones):
    with open(timezones_file, 'w') as file:
        json.dump(timezones, file, indent=4)

class LinkSharing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @nextcord.slash_command(name="sub3")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @commands.guild_only()
    @main.subcommand(name="share_link", description="Share a link and get a preview and summary")
    async def share_link(self, interaction: nextcord.Interaction, url: str):
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            title = article.title
            summary = article.summary
            image_url = article.top_image

            embed = nextcord.Embed(title=title, description=summary, url=url, color=0x00bfff)
            if image_url:
                embed.set_image(url=image_url)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}")
            
            
            
    @main.subcommand()
    async def notawayfromkeyboard(self, interaction: nextcord.Interaction):
        """Removes your afk status"""
        afk_data = load_afk_data()

        if str(interaction.user.id) not in afk_data:
            return await interaction.send("You are not afk")

        del afk_data[str(interaction.user.id)]
        save_afk_data(afk_data)

        await interaction.send("Removed your afk status")

    
    
    @main.subcommand()
    async def awayfromkeyboard(self, interaction: nextcord.Interaction, *, reason:  str = None):
        """Sets your afk status"""
        afk_data = load_afk_data()

        afk_data[str(interaction.user.id)] = {
            "last_seen": datetime.datetime.utcnow().isoformat(),
            "reason": reason
        }

        save_afk_data(afk_data)

        await interaction.send(f"You are now afk{' for '+ reason if reason else ''} :)")

    @main.subcommand()
    async def wremind(self, interaction: nextcord.Interaction, time: str, *, text: str):
        """Remind you to do something after the specified time."""
        converted_time = await TimeConverter().convert(interaction, time)
        natural_time = humanize.naturaldelta(datetime.timedelta(seconds=int(converted_time)))
        await interaction.send(f"Gonna remind you `{text}` in {natural_time}")
        await asyncio.sleep(converted_time)
        await interaction.user.send(text)

    @main.subcommand() #! need to add the code for the look at someones timezone
    async def timeset(self, interaction: nextcord.Interaction, *, timezone: str):
        location = timezone

        # Validate that the person did not just send a continent
        continents = ["asia", "europe", "oceania", "australia", "africa"]
        if location.lower() in continents:
            return await interaction.send("I need an area, not a continent 🤦‍♂️")

        async with self.bot.session.get(f"http://worldtimeapi.org/api/timezone/{location}") as resp:
            fj = json.loads(await resp.text())

        # The error key exists only when there is an error
        if fj.get("error"):
            if fj["error"] == "unknown location":
                async with self.bot.session.get("http://worldtimeapi.org/api/timezone") as resp:
                    locations = await resp.json()

                suggestions = difflib.get_close_matches(location, locations, n=5, cutoff=0.3)
                suggestions = "\n".join(suggestions)

                embed = nextcord.Embed(
                    title="Unknown Location",
                    description="The location couldn't be found",
                    color=14885931,
                )
                embed.add_field(name="Did you mean?", value=suggestions)

                await interaction.send(embed=embed)
            else:
                await interaction.send(fj["error"])

        timezones = load_timezones()
        previous_timezone = timezones.get(str(interaction.user.id))
        timezones[str(interaction.user.id)] = timezone
        save_timezones(timezones)

        if previous_timezone:
            if previous_timezone == timezone:
                embed = nextcord.Embed(
                    title="Failure",
                    description=f"Time zone not changed, it was already set to {timezone}",
                    color=nextcord.Colour.red(),
                )
            else:
                embed = nextcord.Embed(
                    title="Success",
                    description=f"Time zone changed from `{previous_timezone}` to `{timezone}`",
                    color=nextcord.Colour.yellow(),
                )
        else:
            embed = nextcord.Embed(
                title="Success",
                description=f"Time zone set to `{timezone}`",
                color=nextcord.Colour.green(),
            )

        await interaction.send(embed=embed)
    
    
    @main.subcommand()
    async def send_game_deals(self,interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        """
        Sends a notification to the specified channel with details about any free or discounted games on Steam.
        """

        # Check if the user executing the command has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.send("You must be an administrator to use this command.", ephemeral=True)
            return

        await interaction.send("Fetching game deals. This may take some time, please wait...", ephemeral=True)

        db_path = os.path.join("data", "game_deals.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the deals table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                discount_percent INTEGER NOT NULL,
                discount_final_price_formatted TEXT,
                header_image TEXT NOT NULL
            )
        """)
        conn.commit()

        old_deals = []

        # Get the previous deals from the database
        cursor.execute("SELECT * FROM deals")
        rows = cursor.fetchall()
        for row in rows:
            old_deals.append({
                "name": row[1],
                "discount_percent": row[2],
                "discount_final_price_formatted": row[3],
                "header_image": row[4]
            })

        while True:
            new_deals = await fetch_game_deals()
            await send_new_deals(channel, old_deals, new_deals)

            # Store the new deals in the database
            cursor.execute("DELETE FROM deals")
            for game in new_deals:
                cursor.execute("""
                    INSERT INTO deals (name, discount_percent, discount_final_price_formatted, header_image)
                    VALUES (?, ?, ?, ?)
                """, (game['name'], game['discount_percent'], game.get('discount_final_price_formatted', ''), game['header_image']))
            conn.commit()

            old_deals = new_deals

            await interaction.followup.send(f"Game deals notification sent to {channel.mention}!")
            # Wait for 1 hour before checking for updates again
            await asyncio.sleep(60 * 60)

            conn.close()
    
def setup(bot):
    bot.add_cog(LinkSharing(bot))
