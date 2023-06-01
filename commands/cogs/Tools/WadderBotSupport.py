import psutil
import nextcord
from utils.WF1 import Var, Link
from nextcord.ext import commands



class InfoCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    def usercount(self):
        count = 0
        for i in self.bot.guilds:
            count += i.member_count
        return count

    async def description(self):
        info = await self.bot.application_info()
        return (info.description).splitlines()[0]

    
    @nextcord.slash_command(name="waddersupport")
    async def main(self, interaction: nextcord.Interaction):
        pass
    
    
    
    @main.subcommand(name="info", description="To get brief information about bot.")
    async def info(self, interaction: nextcord.Interaction):
        dev = await self.bot.fetch_user(1097375209666908180)

        embed = nextcord.Embed(
            title="✅ About!", colour=nextcord.Color.blue()
        )
        embed.add_field(
            name="💻 Developer",
            value=dev,
            inline=False,
        )

        embed.add_field(
            name="👋 Server",
            value=f"[Join Here.]({Link.server.value})",
        )
        embed.add_field(
            name="🗳️ Vote",
            value=f"[Vote Here.]({Link.topgg.value})",
        )
        embed.add_field(name="** **", value=f"** **")

        embed.add_field(
            name="🏷️ Features",
            value=await self.description(),
            inline=False,
        )

        embed.add_field(
            name="⚙️ System Stats:",
            value=f"**Bot Latency: {round(self.bot.latency * 1000)}ms**\n"
                f"**RAM Usage: {round((psutil.virtual_memory().used / psutil.virtual_memory().total) * 100)}%**\n"
                f"**CPU Usage: {round(psutil.cpu_percent(interval=1, percpu=False))}%**\n"
        )

        embed.add_field(
            name="💬 Bot Stats:",
            value=f"**Total Commands: {len(self.bot.commands)}**\n"
                f"**Total Users: {InfoCmd.usercount(self)}**\n"
                f"**Total Servers: {len(self.bot.guilds)}**\n"
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.set_image(url=Link.banner.value)

        # Button
        info = await self.bot.application_info()
        button = nextcord.ui.View()

        button.add_item(item=nextcord.ui.Button(label="Terms Of Service", url=info.terms_of_service_url), )
        button.add_item(item=nextcord.ui.Button(label="Privacy Policy", url=info.privacy_policy_url))
        button.add_item(item=nextcord.ui.Button(label="Invite Link", url=Link.bot.value))

        # Slash Commands
        slash_commands = await self.bot.get_global_commands()

        if slash_commands:
            slash_commands_str = '\n'.join(f'/{command.name}' for command in slash_commands)
            embed.add_field(
                name="⚡ Slash Commands:",
                value=slash_commands_str,
                inline=False
            )

        await interaction.send(embed=embed, view=button)




    @main.subcommand(name = "waddervote", description = "To get information about voting the bot.")
    @commands.is_owner()
    async def votereminder(self, interaction: nextcord.Interaction):
        channel = self.bot.get_channel(Var.vote_logger.value)

        embed = nextcord.Embed(
            title="<:Tick:884027409123397682> Vote Reminder",
            colour=nextcord.Color.blurple(),
            description="Your votes **matter a lot** in my growth, please consider voting ❤️\n"
                        "Voting me gives you **Access to Development Channel** where you can test my **Experimental version** *when \n"
                        "<@404687039905136661> is working on any new update!*\nYou also **Unlock Vote Locked Commands!**\n"
                        "\nVoting on **top.gg** gives access for **12h**\n",
        )

        embed.set_image(url=Link.banner.value)
        button = nextcord.ui.View()
        button.add_item(item=nextcord.ui.Button(label="Vote Me", url=Link.topgg.value))

        await channel.send(content=f"<@&{Var.vote_role.value}>", embed=embed, view=button)
        await interaction.send(channel.mention)
        
    @main.subcommand(name = "voteunlock", description = "Voting unlocks some commands.")
    async def vote(self, interaction: nextcord.Interaction):

        dev = await self.bot.fetch_user(1097375209666908180) #! change this later to 1072418891680202824

        embed = nextcord.Embed(
            title="🗳️ Vote!", colour=nextcord.Color.blue()
        )
        embed.add_field(name="💻 Developer", value=dev)
        embed.add_field(
            name="👋 Server",
            value=f"[Join Here.]({Link.server.value})",
        )
        embed.add_field(
            name="By Voting You Unlock Following Commands:",
            value = "• All NSFW commands.\n"
                    "• Tic-Tac-Toe, poll, ship, wallpaper, say, embed, MAL, etc.",
            inline = False
        
        )

        embed.set_image(url=Link.banner.value)
        embed.set_thumbnail(url=self.bot.user.display_avatar)

        view = nextcord.ui.View()
        view.add_item(item=nextcord.ui.Button(label="Vote Me", url=Link.topgg.value))

        await interaction.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(InfoCmd(bot))