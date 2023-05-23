import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

class GameServerView(View):
    def __init__(self, bot, game_servers):
        super().__init__(timeout=None)
        self.bot = bot
        self.game_servers = game_servers

    async def send_server_info(self, server_name, interaction):
        server_info = self.game_servers.get(server_name)
        if server_info:
            await interaction.response.send_message(server_info, ephemeral=True)
        else:
            await interaction.response.send_message(f"No information found for server: {server_name}", ephemeral=True)

    @button(label="Server 1", style=nextcord.ButtonStyle.green)
    async def server_1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.send_server_info("Server 1", interaction)

    @button(label="Server 2", style=nextcord.ButtonStyle.green)
    async def server_2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.send_server_info("Server 2", interaction)

    # Add more buttons for additional servers if needed

class GameServerInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_servers = {}  # Format: {"Server 1": "Info", "Server 2": "Info"}
    
    
    @nextcord.slash_command(name="gameserverinfo")
    async def main(self, interaction: nextcord.Interaction):
        pass
    @main.subcommand(name="addserver", description="Add a game server to the list of servers.")
    @commands.has_permissions(administrator=True)
    async def add_server(self, interaction: nextcord.Interaction, server_name: str, *, server_info: str):
        self.game_servers[server_name] = server_info
        await interaction.send(f"Game server '{server_name}' added.")

    @main.subcommand(name="showservers", description="Show a list of all game servers.")
    async def show_servers(self, interaction: nextcord.Interaction):
        if not self.game_servers:
            await interaction.send("No game servers have been added yet.")
            return

        view = GameServerView(self.bot, self.game_servers)
        await interaction.send("Click a button to view information for a specific game server:", view=view)

def setup(bot):
    bot.add_cog(GameServerInfoCog(bot))
# bad ass (add a json file to keep buttonss sactive ) and also fix it
