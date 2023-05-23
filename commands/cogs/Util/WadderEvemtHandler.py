import json
import nextcord
from nextcord.ext import commands
from utils.WF1 import Link, Var

data = {"guild": []}

with open("data/ban.json", "w") as f:
    json.dump(data, f)


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() #! Doesnt Work
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        bot_mention = f"<@!{self.bot.user.id}>"
        if bot_mention in message.content:
            button = nextcord.ui.View()
            button.add_item(item=nextcord.ui.Button(label="Invite Link", url=Link.bot.value))
            button.add_item(item=nextcord.ui.Button(label="My Server", url=Link.server.value))

            embed = nextcord.Embed(
                title=f"Hey {message.author.name}!",
                description=f"**Slash Commands:** `/`\n**For Help:** `/help`",
                color=nextcord.Color.blurple(),
            )
            embed.set_thumbnail(url=self.bot.user.display_avatar)

            if message.channel is not None:
                try:
                    await message.channel.send(embed=embed, view=button)
                except AttributeError:
                    pass
            else:
                print("Message channel is None")


    @commands.Cog.listener() # ** works  - change the actual guild logger channels
    async def on_guild_join(self, guild):

        if guild.id in data["guild"]:
            await guild.leave()

        else:
            try:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:

                        embed = nextcord.Embed(
                            title="Thanks For Adding Me!",
                            colour=nextcord.Color.blurple(),
                            description=f"**Slash Commands Only** `/`"
                        )

                        embed.set_thumbnail(url=self.bot.user.display_avatar)
                        embed.set_footer(
                            text=f"Join My Server!",
                            icon_url=self.bot.user.display_avatar,
                        )

                        view = nextcord.ui.View()

                        view.add_item(item=nextcord.ui.Button(label="My Server", url=Link.server.value))

                        await channel.send(embed=embed, view=view)
                        break
            finally:
                Log = self.bot.get_channel(Var.guild_logger.value)

                embed = nextcord.Embed(
                    title=f"<a:Added:884853928683008001> Added To {guild.name}",
                    description=f"\n:id: **Server ID:** `{guild.id}`\n:earth_americas: **Server Region:** {str(guild.region).title()}",
                    colour=nextcord.Colour.green(),
                )
                # embed.add_field(name=f"<:ServerOwner:864765886916067359> Server Owner", value=f"**{guild.owner}**\n`{guild.owner.id}`")
                embed.add_field(
                    name=f"<:ServerOwner:864765886916067359> Server Owner",
                    value=f"**{guild.owner}**",
                )
                embed.add_field(
                    name=f"📝 Total Channels",
                    value=f"**Text Channels:** {len(guild.text_channels)}\n**Voice Channels:** {len(guild.voice_channels)}",
                )
                embed.add_field(
                    name=f"<:boost:864737209722470420> Boost",
                    value=f"**Server Boosts:** {guild.premium_subscription_count}\n**Boost Level:** {guild.premium_tier}",
                )
                embed.add_field(
                    name=f"👥 Total Members", 
                    value=f"{guild.member_count}"
                )
                embed.add_field(
                    name=f"✅ Verification Level",
                    value=f"{guild.verification_level}",
                    inline=True,
                )
                date = guild.created_at.strftime("%d-%m-%Y")
                embed.add_field(name=f"📆 Created On", value=f"{date}", inline=True)

                if guild.icon:
                    embed.set_thumbnail(url=guild.icon)

                if guild.banner:
                    embed.set_image(url=guild.banner)

                await Log.send(embed=embed)

    @commands.Cog.listener() # ** works
    async def on_guild_remove(self, guild):
        Log = self.bot.get_channel(Var.guild_logger.value)

        embed = nextcord.Embed(
            title=f"<a:Removed:884853970810593341> Removed From {guild.name}",
            description=f"\n:id: **Server ID:** `{guild.id}`\n:earth_americas: **Server Region:** {str(guild.region).title()}",
            colour=nextcord.Colour.red(),
        )
        # embed.add_field(name=f"<:ServerOwner:864765886916067359> Server Owner", value=f"**{guild.owner}**\n`{guild.owner.id}`")
        embed.add_field(
            name=f"<:ServerOwner:864765886916067359> Server Owner",
            value=f"**{guild.owner}**",
        )
        embed.add_field(
            name=f"📝 Total Channels",
            value=f"**Text Channels:** {len(guild.text_channels)}\n**Voice Channels:** {len(guild.voice_channels)}",
        )
        embed.add_field(
            name=f"<:boost:864737209722470420> Boost",
            value=f"**Server Boosts:** {guild.premium_subscription_count}\n**Boost Level:** {guild.premium_tier}",
        )
        embed.add_field(name=f"👥 Total Members", value=f"{guild.member_count}")
        embed.add_field(
            name=f"✅ Verification Level",
            value=f"{guild.verification_level}",
            inline=True,
        )
        date = guild.created_at.strftime("%d-%m-%Y")
        embed.add_field(name=f"📆 Created On", value=f"{date}", inline=True)

        thumbnail = guild.icon
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        image = guild.banner
        if image:
            embed.set_image(url=image)

        await Log.send(embed=embed)

   

    

    async def log_command(self, ctx):
        channel = self.bot.get_channel(Var.command_logger.value)

        embed = nextcord.Embed(
            title=f"<:mecool:885766779496972298> Command Executed!",
            colour=nextcord.Color.blurple(),
            description=f"**Command:** {ctx.command.name}"
            f"```{ctx.message.content}```\n"
            f"in {ctx.channel.mention} of \n"
            f"**{ctx.guild.name}** : {ctx.guild.id}",
        )

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon)

        embed.set_author(
            name=f"{ctx.author} | {ctx.author.id}", icon_url=ctx.author.display_avatar
        )
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(EventHandler(bot))