import nextcord
from nextcord.ext import commands


# * * this could have more sub commands, not utilizing the space well enough.


class OnlineStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def onlinestatus(self, ctx: commands.Context):
        """Print how many people are using each type of device."""
        device = {
            (True, True, True): 0,
            (False, True, True): 1,
            (True, False, True): 2,
            (True, True, False): 3,
            (False, False, True): 4,
            (True, False, False): 5,
            (False, True, False): 6,
            (False, False, False): 7,
        }
        store = [0, 0, 0, 0, 0, 0, 0, 0]
        for m in ctx.guild.members:
            value = (
                m.desktop_status == nextcord.Status.offline,
                m.web_status == nextcord.Status.offline,
                m.mobile_status == nextcord.Status.offline,
            )
            store[device[value]] += 1
        msg = (
            f"offline all: {store[0]}"
            f"\ndesktop only: {store[1]}"
            f"\nweb only: {store[2]}"
            f"\nmobile only: {store[3]}"
            f"\ndesktop web: {store[4]}"
            f"\nweb mobile: {store[5]}"
            f"\ndesktop mobile: {store[6]}"
            f"\nonline all: {store[7]}"
        )
        await ctx.send(f"```py\n{msg}```")

    @commands.guild_only()
    @commands.command()
    async def onlineinfo(
        self, ctx: commands.Context, member: nextcord.Member = None
    ):
        """Show what devices a member is using."""
        if member is None:
            member = ctx.author
        d = str(member.desktop_status)
        m = str(member.mobile_status)
        w = str(member.web_status)
        # because it isn't supported in nextcord, manually override if streaming
        if any(isinstance(a, nextcord.Streaming) for a in member.activities):
            d = d if d == "offline" else "streaming"
            m = m if m == "offline" else "streaming"
            w = w if w == "offline" else "streaming"
        status = {
            "online": "\U0001f7e2",
            "idle": "\U0001f7e0",
            "dnd": "\N{LARGE RED CIRCLE}",
            "offline": "\N{MEDIUM WHITE CIRCLE}",
            "streaming": "\U0001f7e3",
        }
        embed = nextcord.Embed(
            title=f"**{member.display_name}'s devices:**",
            description=(
                f"{status[d]} Desktop\n" f"{status[m]} Mobile\n" f"{status[w]} Web"
            ),
            color=await ctx.embed_color(),
        )
        embed.set_thumbnail(url=member.avatar.url)
        try:
            await ctx.send(embed=embed)
        except nextcord.errors.Forbidden:
            await ctx.send(
                f"{member.display_name}'s devices:\n"
                f"{status[d]} Desktop\n"
                f"{status[m]} Mobile\n"
                f'{status[w]} Web'
			)
            
    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found.")
        else:
            await super().cog_command_error(ctx, error)


def setup(bot: commands.Bot):
    bot.add_cog(OnlineStats(bot))        

