import nextcord
from nextcord.ext import commands
import requests



class NBAPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def nba_player(self, interaction: nextcord.Interaction, name: str):
        search_url = "https://free-nba.p.rapidapi.com/players"
        search_params = {
            "search": name,
            "per_page": 5
        }

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
        }

        search_response = requests.get(search_url, headers=headers, params=search_params)
        search_results = search_response.json()["data"]

        if not search_results:
            await interaction.send("No players found with that name.")
            return

        player_ids = [player["id"] for player in search_results]
        player_data = []

        for player_id in player_ids:
            player_url = f"https://free-nba.p.rapidapi.com/players/{player_id}"
            player_response = requests.get(player_url, headers=headers)
            player_data.append(player_response.json())

        for player in player_data:
            player_name = player['first_name'] + " " + player['last_name']
            player_team = player['team']['full_name']
            player_stats = (
                str(player['height_feet'])
                + " ft "
                + str(player['height_inches'])
                + " in, "
                + str(player['weight_pounds'])
                + " lbs"
            )
            
            image_search_url = "https://api.unsplash.com/search/photos"
            image_search_params = {
                "query": player_name,
                "per_page": 1,
                "client_id": "8_x4s8mZvLnV6ZzBsiEfWIdq8ZL_utvXX5MdtyDgm34"
            }
            
            image_response = requests.get(image_search_url, params=image_search_params)
            image_data = image_response.json()["results"]
            
            if image_data:
                player_image = image_data[0]["urls"]["small"]
            else:
                player_image = None
            
            embed = nextcord.Embed(title="NBA Player Information", description=f"Player: {player_name}", color=0x00ff00)
            embed.add_field(name="Team", value=player_team, inline=False)
            embed.add_field(name="Stats", value=player_stats, inline=False)
            
            if player_image:
                embed.set_thumbnail(url=player_image)
            
            await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(NBAPlayerCog(bot))



