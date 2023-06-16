import csv
import datetime
import io
import json
import os
import time
from bs4 import BeautifulSoup
import nextcord
from nextcord.ext import commands
import requests
import time
from datetime import datetime, timedelta

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
        image_title = data.get("title", "Untitled")
        image_url = data.get("url")
        image_explanation = data.get("explanation", "No explanation available.")

        # Build the response message
        message = "Astronomy Picture of the Day:\n\n"
        message += f"Title: {image_title}\n"
        message += f"Explanation: {image_explanation}"

        # Send the message with the image URL as an embed
        embed = nextcord.Embed(title=image_title, description=image_explanation)
        embed.set_image(url=image_url)

        await interaction.response.send_message(content=message, embed=embed, ephemeral=True)
            
    @dev4.subcommand(description="Fetch SEO data for a sitemap URL")
    async def fetch_seo_data(self, interaction: nextcord.Interaction, url: str):
        api_url = "https://seo-automations.p.rapidapi.com/v1/seo/fetchsitemap/"

        querystring = {
            "url": url,
            "breadcrumbs": "true",
            "categories": "true",
            "meta": "true"
        }

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "seo-automations.p.rapidapi.com"
        }

        response = requests.get(api_url, headers=headers, params=querystring)
        data = response.json()

        # Extract the relevant information from the response
        breadcrumbs = data.get("breadcrumbs", [])
        categories = data.get("categories", [])
        meta_data = data.get("meta", {})

        # Build the response message
        message = "SEO Data for Sitemap URL:\n\n"
        message += "Breadcrumbs:\n"
        for breadcrumb in breadcrumbs:
            message += f"- {breadcrumb}\n"
        message += "\nCategories:\n"
        for category in categories:
            message += f"- {category}\n"
        message += f"\nMeta Data:\nTitle: {meta_data.get('title')}\nDescription: {meta_data.get('description')}"

        # Send the message
        await interaction.response.send_message(message, ephemeral=True)
        
        
        
    @dev4.subcommand(description="Get information about a D&D spell")
    async def dnd_spell_info(self, interaction: nextcord.Interaction, spell_name: str):
        base_url = "https://dungeons-and-dragon-5e.p.rapidapi.com/spell/"
        url = base_url + spell_name.lower().replace(" ", "-")

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "dungeons-and-dragon-5e.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)

            # Check if the spell exists in the response
            if "name" not in data:
                await interaction.response.send_message("The spell was not found.", ephemeral=True)
                return

            # Extract the relevant information from the response
            spell_name = data.get("name")
            spell_description = data.get("desc")
            spell_range = data.get("range")
            spell_components = data.get("components")
            spell_duration = data.get("duration")
            spell_casting_time = data.get("casting_time")

            # Build the response message
            message = "D&D Spell Information:\n\n"
            message += f"Spell Name: {spell_name}\n"
            message += f"Description: {spell_description}\n"
            message += f"Range: {spell_range}\n"
            message += f"Components: {spell_components}\n"
            message += f"Duration: {spell_duration}\n"
            message += f"Casting Time: {spell_casting_time}"

            # Send the message
            await interaction.response.send_message(message, ephemeral=True)
        except requests.exceptions.RequestException:
            await interaction.response.send_message("An error occurred while making the API request.", ephemeral=True)
        except json.JSONDecodeError:
            await interaction.response.send_message("An error occurred while parsing the API response.", ephemeral=True)
    
    # Command to save email addresses
    @dev4.subcommand(description="Save an email address")
    async def save_email(self, interaction: nextcord.Interaction, email: str):
        # Read the existing email addresses from the JSON file
        with open('email_addresses.json', 'r') as file:
            data = json.load(file)
        
        # Ensure that data is a list
        if not isinstance(data, list):
            data = []
        
        # Append the new email address to the list
        data.append(email)
        
        # Write the updated email addresses back to the JSON file
        with open('email_addresses.json', 'w') as file:
            json.dump(data, file)
        
        await interaction.response.send_message("Email address saved successfully!", ephemeral=True)


    # Command to send emails
    @dev4.subcommand(description="Send news email to all subscribers")
    async def send_news_email(self, interaction: nextcord.Interaction):
        # Read the email addresses from the JSON file
        with open('email_addresses.json', 'r') as file:
            email_addresses = json.load(file)

        url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

        payload = {
            "personalizations": [
                {
                    "to": [{"email": email} for email in email_addresses],
                    "subject": "Hello, World!"
                }
            ],
            "from": {"email": "wadderproject@gmail.com"},
            "content": [
                {
                    "type": "text/plain",
                    "value": "Hello, World!"
                }
            ]
        }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 202:
            await interaction.response.send_message("News email sent successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred while sending the news email.", ephemeral=True)
    @dev4.subcommand(description="Convert text to a formatted HTML response")
    async def convert_text(self, interaction: nextcord.Interaction, *, text: str):
        url = "https://bionic-reading1.p.rapidapi.com/convert"

        payload = {
            "content": text,
            "response_type": "html",
            "request_type": "html",
            "fixation": "1",
            "saccade": "10"
        }

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com"
        }

        response = requests.post(url, data=payload, headers=headers)

        try:
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            formatted_text = soup.select_one(".bionic-reader-container").get_text()
            await interaction.response.send_message(formatted_text, ephemeral=True)
        except requests.HTTPError as e:
            await interaction.response.send_message(f"An HTTP error occurred: {str(e)}", ephemeral=True)
        except Exception:
            await interaction.response.send_message("An error occurred while processing the API response.", ephemeral=True)



    @dev4.subcommand(description="Get information about a place")
    async def get_place_info(self, interaction: nextcord.Interaction, *, place_name: str):
        url = "https://opentripmap-places-v1.p.rapidapi.com/en/places/geoname"

        querystring = {"name": place_name}

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "opentripmap-places-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            place_info = response.json()
            await interaction.response.send_message(place_info, ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred while retrieving place information.", ephemeral=True)

    @dev4.subcommand(description="Get recent video game news")
    async def get_video_game_news(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        url = "https://videogames-news2.p.rapidapi.com/videogames_news/recent"

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "videogames-news2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            video_game_news = response.json()

            for news in video_game_news:
                title = news.get("title")
                description = news.get("description")
                link = news.get("link")

                news_message = f"Title: {title}\nDescription: {description}\nLink: {link}"

                # Split the news message into chunks of 2000 characters or less
                chunks = [news_message[i:i+2000] for i in range(0, len(news_message), 2000)]

                for chunk in chunks:
                    await interaction.response.send_message(chunk)
        else:
            await interaction.response.send_message("An error occurred while retrieving video game news.")
     
     
    @dev4.subcommand(description="Get TikTok user info")
    async def get_tiktok_user_info(self, interaction: nextcord.Interaction, user_id: str):
        url = "https://tiktok-web-api.p.rapidapi.com/"

        querystring = {
            "type": "rapidapi-userinfo",
            "username": user_id
        }

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "tiktok-web-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print("URL:", url)
        print("Querystring:", querystring)
        print("Headers:", headers)
        print("Response status code:", response.status_code)
        print("Response content:", response.content)

        if response.status_code == 200:
            tiktok_user_info = response.json()

            print("TikTok user info:", tiktok_user_info)

            extra = tiktok_user_info.get("extra")
            log_pb = tiktok_user_info.get("log_pb")
            share_meta = tiktok_user_info.get("shareMeta")
            status_code = tiktok_user_info.get("statusCode")
            user_info = tiktok_user_info.get("userInfo")

            desc = share_meta.get("desc")
            title = share_meta.get("title")

            stats = user_info.get("stats")
            follower_count = stats.get("followerCount")
            following_count = stats.get("followingCount")
            heart_count = stats.get("heartCount")
            video_count = stats.get("videoCount")

            avatar_larger = user_info.get("avatarLarger")
            avatar_medium = user_info.get("avatarMedium")
            avatar_thumb = user_info.get("avatarThumb")

            signature = user_info.get("signature")

            formatted_user_info = f"Title: {title}\nDescription: {desc}\n\n"
            formatted_user_info += f"Followers: {follower_count}\nFollowing: {following_count}\nHearts: {heart_count}\nVideos: {video_count}\n\n"
            formatted_user_info += f"Avatar Larger: {avatar_larger}\nAvatar Medium: {avatar_medium}\nAvatar Thumb: {avatar_thumb}\n\n"
            formatted_user_info += f"Signature: {signature}"

            print("Formatted user info:", formatted_user_info)

            await interaction.response.send_message(formatted_user_info)
        else:
            await interaction.response.send_message("An error occurred while retrieving TikTok user info.")
            
    @dev4.subcommand(description="counters")
    @commands.has_permissions(administrator=True)
    async def setup_counters(self, interaction: nextcord.Interaction):
        # Check if the user has administrator privileges
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You must have administrator privileges to use this command.", ephemeral=True)
            return

        # Get the number of members in the server
        member_count = len(interaction.guild.members)

        # Create a voice channel with the member count
        member_count_channel_name = f"👥 Members: {member_count}"
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(connect=False)
        }

        # Create the member count voice channel
        try:
            member_count_channel = await interaction.guild.create_voice_channel(
                name=member_count_channel_name,
                overwrites=overwrites,
                category=None
            )
        except nextcord.HTTPException:
            await interaction.response.send_message("❌ Failed to create the member count channel.", ephemeral=True)
            return

        await interaction.response.send_message(f"✅ Member count channel created: {member_count_channel.mention}", ephemeral=True)

    @dev4.subcommand(name="ch", description="Check the health of a channel")
    
    async def channel_status(self, ctx, channel: nextcord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        server_id = self.bot.get_guild(self.bot.guilds[0].id)

        embed = nextcord.Embed(colour=nextcord.Colour.orange())
        embed.set_author(name="Channel Health:")

        loading_message = await ctx.send("Fetching channel information...")

        # Define the ASCII animation frames
        frames = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]", "[    ]"]

        for frame in frames:
            await loading_message.edit(content=f"Fetching channel information {frame}")
            time.sleep(0.5)

        async with ctx.channel.typing():
            count = 0
            async for message in channel.history(limit=500000, after=datetime.today() - timedelta(days=100)):
                count += 1

            if count >= 5000:
                average = "OVER 5000!"
                healthiness = "VERY HEALTHY \U0001F60D"  # Emoji: 😍
            else:
                try:
                    average = round(count / 100, 2)

                    if 0 > server_id.member_count / average:
                        healthiness = "VERY HEALTHY \U0001F60D"  # Emoji: 😍
                    elif server_id.member_count / average <= 5:
                        healthiness = "HEALTHY \U0001F642"  # Emoji: 🙂
                    elif server_id.member_count / average <= 10:
                        healthiness = "NORMAL \U0001F610"  # Emoji: 😐
                    elif server_id.member_count / average <= 20:
                        healthiness = "UNHEALTHY \U0001F615"  # Emoji: 😕
                    else:
                        healthiness = "VERY UNHEALTHY \U0001F625"  # Emoji: 😥

                except ZeroDivisionError:
                    average = 0
                    healthiness = "VERY UNHEALTHY \U0001F625"  # Emoji: 😥

            embed.add_field(name="­", value=f"Number of members: {server_id.member_count}", inline=False)
            embed.add_field(name="­", value=f'Number of messages per day on average in "{channel}" is: {average}', inline=False)
            embed.add_field(name="­", value=f"Channel health: {healthiness}", inline=False)

            # Additional information in the embed
            embed.add_field(name="Channel", value=channel.mention, inline=True)
            embed.add_field(name="Created at", value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
            embed.add_field(name="Channel ID", value=channel.id, inline=True)
            embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
            embed.add_field(name="Slowmode", value=channel.slowmode_delay if channel.slowmode_delay else "Not Enabled", inline=True)

            # Get the path to the GIF file in your project's directory
            gif_path = os.path.join(os.getcwd(), 'images', 'quanta.gif')

            # Attach the GIF file to the embed
            gif_file = nextcord.File(gif_path, filename='animated.gif')
            embed.set_image(url="attachment://animated.gif")

            # Update the loading message with the channel information embed
            await loading_message.edit(content="Channel Information", file=gif_file, embed=embed)
            
            
    @dev4.subcommand(description="Get ZIP Code Information")
    async def zip_code(self, interaction: nextcord.Interaction, zip_code: str):
        url = "https://us-zip-code-information.p.rapidapi.com/"

        querystring = {"zipcode": zip_code}

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "us-zip-code-information.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Extract the relevant information from the response
        city = data.get("city")
        state = data.get("state")
        country = data.get("country")

        # Build the response message
        message = f"ZIP Code Information for {zip_code}:\n\n"
        message += f"City: {city}\n"
        message += f"State: {state}\n"
        message += f"Country: {country}"

        await interaction.response.send_message(content=message, ephemeral=True)
            
def setup(bot):
    bot.add_cog(Developer2(bot))