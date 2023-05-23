import nextcord
from nextcord.ext import commands, tasks


mcOs = True #IF True = Minecraft Serve OR IF False = Source Server (like gmod,csgo...)

if mcOs:
    from mcstatus import JavaServer
else:
    from sourceserver.sourceserver import SourceServer

class ServerStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_ip = '208.52.147.254'
        self.server_port = '25565'
        self.mcOs = True

        self.status_loop.start()

    def cog_unload(self):
        self.status_loop.cancel()

    @tasks.loop(seconds=5)
    async def status_loop(self):
        try:
            if self.mcOs:
                server = JavaServer.lookup(str(self.server_ip + ':' + self.server_port))
                status = server.status()
                if status.players.online == 0:
                    await self.bot.change_presence(activity=nextcord.Game(name="{}/{} Joueurs".format(status.players.online, status.players.max)),
                                                   status=nextcord.Status.idle)
                else:
                    await self.bot.change_presence(activity=nextcord.Game(name="{}/{} Joueurs".format(status.players.online, status.players.max)),
                                                   status=nextcord.Status.online)
            else:
                srv = SourceServer(str(self.server_ip + ':' + self.server_port))
                if int(srv.info['players']) == 0:
                    await self.bot.change_presence(activity=nextcord.Game(name="{}/{} Joueurs".format(srv.info['players'], srv.info['max_players'])),
                                                   status=nextcord.Status.idle)
                else:
                    await self.bot.change_presence(activity=nextcord.Game(name="{}/{} Joueurs".format(srv.info['players'], srv.info['max_players'])),
                                                   status=nextcord.Status.online)
        except:
            await self.bot.change_presence(activity=nextcord.Game(name="Serveur Hors-Ligne"), status=nextcord.Status.dnd)

    @nextcord.slash_command(name="mineserver", description="Displays server information.")
    async def mineserver(self, interaction: nextcord.Interaction):
        try:
            if self.mcOs:
                server = JavaServer.lookup(str(self.server_ip + ':' + self.server_port))
                status = server.status()
                embed = nextcord.Embed(color=0xff8000)
                embed.add_field(name='Players', value=status.players.online, inline=True)
                embed.add_field(name='Slots', value=status.players.max, inline=True)
                embed.add_field(name='Latency', value=str(status.latency) + ' ms', inline=True)
                embed.add_field(name='Address', value=self.server_ip, inline=True)
                embed.add_field(name='Port', value=self.server_port, inline=True)
                embed.add_field(name='Version', value=status.version.name, inline=True)
                await interaction.response.send_message(embed=embed)
            else:
                srv = SourceServer(str(self.server_ip + ':' + self.server_port))
                embed = nextcord.Embed(title=srv.info['name'], color=0x0080ff)
                embed.add_field(name='Players', value=srv.info['players'], inline=True)
                embed.add_field(name='Slots', value=srv.info['max_players'], inline=True)
                embed.add_field(name='Latency', value=srv.ping(2), inline=True)
                embed.add_field(name='Gamemode', value=srv.info['game'], inline=True)
                embed.add_field(name='Map', value=srv.info['map'], inline=True)
                embed.add_field(name='Version', value=srv.info['version'], inline=True)
                await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("Server Offline")

def setup(bot):
    bot.add_cog(ServerStatusCog(bot))
