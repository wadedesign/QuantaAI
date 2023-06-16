import datetime
import nextcord
from nextcord.ext import commands, tasks
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.dates as mdates

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "YOUR_API_KEY"
        self.server_id = None
        self.original_message = None
        self.update_server_info.start()

    def cog_unload(self):
        self.update_server_info.cancel()

    async def fetch_player_count_history(self):
        now = datetime.datetime.utcnow()
        start = now - datetime.timedelta(hours=24)

        url = f"https://api.battlemetrics.com/servers/{self.server_id}/player-count-history"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "start": start.isoformat() + "Z",
            "stop": now.isoformat() + "Z",
            "resolution": "30"
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            timestamps = []
            player_counts = []

            for item in data["data"]:
                timestamps.append(item["attributes"]["timestamp"])
                player_counts.append(item["attributes"]["value"])

            return timestamps, player_counts
        else:
            print(f"Error fetching player count history: {response.status_code} - {data.get('errors', 'Unknown error')}")
            return None, None

    async def generate_player_count_history_graph(self):
        timestamps, player_counts = await self.fetch_player_count_history()

        if timestamps and player_counts:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(timestamps, player_counts, linestyle='-', marker='o', markersize=3, color='blue', linewidth=1)

            ax.set_xlabel("Time")
            ax.set_ylabel("Player Count")
            ax.set_title("Player Count History")
            ax.grid(True)

            # Format x-axis date and time labels
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
            fig.autofmt_xdate()

            buffer = BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0.2)
            buffer.seek(0)
            plt.close(fig)

            return buffer
        else:
            return None

    async def update_server_info_message(self):
        try:
            # Send a request to the BattleMetrics API
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"https://api.battlemetrics.com/servers/{self.server_id}"
            response = requests.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                # Extract server information
                server_name = data["data"]["attributes"]["name"]
                server_ip = data["data"]["attributes"]["ip"]
                server_port = data["data"]["attributes"]["port"]
                online_players = data["data"]["attributes"]["players"]
                max_players = data["data"]["attributes"]["maxPlayers"]

                # Generate and send player count history graph
                graph_buffer = await self.generate_player_count_history_graph()
                if graph_buffer:
                    graph_file = nextcord.File(graph_buffer, "player_count_history.png")

                    # Create embed message with server information and graph
                    embed = nextcord.Embed(title=f"Server info for {server_name}",
                                           description=f"IP: {server_ip}:{server_port}\n"
                                                       f"Online players: {online_players}/{max_players}",
                                           color=nextcord.Color.blue())

                    embed.set_image(url="attachment://player_count_history.png")
                    await self.original_message.edit(embed=embed, file=graph_file)
                else:
                    # Create embed message with server information only
                    embed = nextcord.Embed(title=f"Server info for {server_name}",
                                           description=f"IP: {server_ip}:{server_port}\n"
                                                       f"Online players: {online_players}/{max_players}",
                                           color=nextcord.Color.blue())

                    await self.original_message.edit(embed=embed)

            else:
                # Handle invalid server ID
                await self.original_message.edit(content="Invalid server ID")

        except Exception as e:
            print(e)
            await self.original_message.edit(content="An error occurred while fetching server information")

    @tasks.loop(seconds=15)
    async def update_server_info(self):
        if self.server_id and self.original_message:
            await self.update_server_info_message()

    @nextcord.slash_command(name="setserver", description="Set the server ID for server info updates")
    @commands.has_permissions(administrator=True)
    async def set_server_id(self, ctx, server_id: int):
        self.server_id = server_id
        await ctx.send(f"Server ID set to {server_id}")

    @nextcord.slash_command(name="setupdates", description="Set up server info updates in a channel")
    @commands.has_permissions(administrator=True)
    async def set_updates_channel(self, ctx, channel: nextcord.TextChannel):
        if self.server_id:
            self.original_message = await channel.send("Initializing server info...")
            await self.update_server_info_message()
            await ctx.send(f"Server info updates set up in {channel.mention}")
        else:
            await ctx.send("Please set the server ID first using the `setserver` command.")

    @nextcord.slash_command(name="refresh", description="Refresh the server info")
    @commands.has_permissions(administrator=True)
    async def refresh_server_info(self, ctx):
        if self.server_id and self.original_message:
            await self.update_server_info_message()
            await ctx.send("Server info refreshed.")
        else:
            await ctx.send("Please set the server ID and channel first using the `setserver` and `setupdates` commands.")

def setup(bot):
    bot.add_cog(ServerInfo(bot))
