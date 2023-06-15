import json
import nextcord
from nextcord.ext import commands
from serpapi import GoogleSearch
from pymongo import MongoClient
import urllib.parse

# * Ready for Production * #

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
spam_collection = db["serpapi"]


class LocalSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="qserpapi")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="local_search", description="Local searches")
    async def local_search(self, interaction: nextcord.Interaction, query: str, *, location: str):
        await interaction.response.defer()
        params = {
            "engine": "google_maps",
            "q": query,
            "location": location,
            "type": "search",
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc"  # Replace with your actual API key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        local_results = results.get("local_results", [])

        if local_results:
            embed = nextcord.Embed(title="Local Search Results", color=0x00ff00)

            for index, result in enumerate(local_results, start=1):
                title = result["title"]
                data_id = result["data_id"]
                value = f"Data ID: {data_id}"

                embed.add_field(name=f"{index}. {title}", value=value, inline=False)

            await interaction.send(embed=embed)
        else:
            await interaction.send("No local results found.")

    @main.subcommand(name="photo_meta", description="Fetches photo metadata for a local search result")
    async def photo_meta(self, interaction: nextcord.Interaction, query: str, location: str, index: int):
        # Get the search results first
        search_params = {
            "engine": "google_maps",
            "q": query,
            "location": location,
            "type": "search",
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc"  # Replace with your actual API key
        }

        search = GoogleSearch(search_params)
        results = search.get_dict()
        local_results = results.get("local_results", [])

        if index < 1 or index > len(local_results):
            await interaction.send("Invalid index. Please provide a valid index from the local search results.")
            return

        data_id = local_results[index - 1]["data_id"]

        # Fetch photo metadata
        params = {
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc",  # Replace with your actual API key
            "engine": "google_maps_photo_meta",
            "q": query,
            "data_id": data_id,
            "no_cache": "true"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        response = f"Photo meta data for '{query}':\n```{json.dumps(results, indent=2, sort_keys=True)}```"
        await interaction.send(response)

    # ** Google Lens **# Very good, look a picutre of someone or something and it will find more things about it
    @main.subcommand(name="googlelens", description="Searches for visual matches of url.png")
    async def googlelens(self, interaction: nextcord.Interaction, url: str):
        await interaction.response.defer()
        params = {
            "engine": "google_lens",
            "url": url,
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        visual_matches = results["visual_matches"]

        if visual_matches:
            await interaction.send("Visual matches found:")
            for match in visual_matches:
                response = f"{match['title']} - {match['link']}"
                await interaction.send(response)
        else:
            await interaction.send("No visual matches found.")

    # ** Uses a word to find videos from google **#
    @main.subcommand(name="googlevideos", description="Searches for videos based on a query")
    async def googlevideos(self, interaction: nextcord.Interaction, query: str):
        await interaction.response.defer()
        params = {
            "q": query,
            "engine": "google_videos",
            "hl": "en",
            "gl": "us",
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        video_results = results["video_results"]

        if video_results:
            await interaction.send("Video results found:")
            for video in video_results[:5]:  # Limit to 5 results to avoid exceeding message limit
                response = f"{video['title']} - {video['link']}"
                await interaction.send(response)
        else:
            await interaction.send("No video results found.")

    @main.subcommand(name="ytvideos", description="Searches for videos based on a query")
    async def youtubesearch(self, interaction: nextcord.Interaction, query: str):
        await interaction.response.defer()
        params = {
            "engine": "youtube",
            "search_query": query,
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        video_results = results.get("video_results")

        if video_results:
            await interaction.send("Video results found:")
            for video in video_results[:5]:  # Limit to 5 results to avoid exceeding message limit
                response = f"{video['title']} - {video['link']}"
                await interaction.send(response)
        else:
            await interaction.send("No video results found.")

    @main.subcommand(name="bing", description="Searches for things on Bing")
    async def bingsearch(self, interaction: nextcord.Interaction, query: str):
        await interaction.response.defer()
        params = {
            "engine": "bing",
            "q": query,
            "cc": "US",
            "api_key": "699dffabdbe268638db02f4f4663dc7bfa7ded8da92b2ae47b41ddb40cdbffcc"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        if organic_results:
            embed = nextcord.Embed(title="Bing Search Results", color=0x00ff00)

            for result in organic_results[:5]:
                title = result["title"]
                link = result["link"]

                embed.add_field(name=title, value=link, inline=False)

            await interaction.send(embed=embed)
        else:
            await interaction.send("No Bing search results found.")


def setup(bot):
    bot.add_cog(LocalSearchCog(bot))



