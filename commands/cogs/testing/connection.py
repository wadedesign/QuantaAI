import nextcord
from nextcord.ext import commands

class ConnectionInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.footer = "This is the footer for all embeds that are sent by this bot."

    def get_footer(self):
        return self.footer
    @nextcord.slash_command(name='sub12')
    async def main (self, interaction: nextcord.Interaction):
        pass

    @main.subcommand()
    async def connectioninfo(self, interaction: nextcord.Interaction, *, user: nextcord.User = None):
        await interaction.response.defer()
        user = user or interaction.user
        member = interaction.guild.get_member(user.id)

        if not member:
            return await interaction.send(":x: **This User is not a Member of this Guild!**")

        if not member.voice or not member.voice.channel:
            return await interaction.send(":x: **This User is not Connected to a Voice Channel!**")

        voice_channel = member.voice.channel
        embed = nextcord.Embed(title=f"Connection Info of: `{user}`")
        embed.add_field(name="<:arrow:832598861813776394> **Channel**", value=f"> **{voice_channel.name}** {voice_channel}", inline=True)
        embed.add_field(name="<:arrow:832598861813776394> **Channel-ID**", value=f"> `{voice_channel.id}`", inline=True)
        embed.add_field(name="<:arrow:832598861813776394> **Members in there**", value=f"> `{len(voice_channel.members)} total Members`", inline=True)

        user_limit = voice_channel.user_limit
        full_status = "✅" if len(voice_channel.members) >= user_limit else "❌"
        embed.add_field(name="<:arrow:832598861813776394> **Full Channel?**", value=f"> {full_status}", inline=True)

        embed.add_field(name="<:arrow:832598861813776394> **Bitrate**", value=f"> {voice_channel.bitrate}", inline=True)
        embed.add_field(name="<:arrow:832598861813776394> **User join limit**", value=f"> `{user_limit if user_limit != 0 else 'No limit!'}`", inline=True)

        await interaction.send(embed=embed)

    @main.subcommand()
    async def server_banner(self, interaction: nextcord.Interaction):
        await interaction.send("loading...")

        try:
            guild = interaction.guild

            if guild.banner:
                embed = nextcord.Embed(
                    title="**Server Banner**",
                    color=0x00FF00,
                )
                embed.set_description(
                    f"[Download Link]({guild.banner_url_as(size=1024)}){f' | [Link of Discovery Splash Image]({guild.discovery_splash_url_as(size=4096)})' if guild.discovery_splash else ''}\n> This is the Image which is shown on the Top left Corner of this Server, where you see the Channels!"
                )
                embed.set_image(url=guild.banner_url_as(size=4096))
                await interaction.send(embed=embed)
            else:
                embed = nextcord.Embed(
                    title="**This Server has no Banner!**",
                    color=0xFF0000,
                )
                await interaction.send(embed=embed)

        except Exception as e:
            print(e)
            await interaction.send(embed=nextcord.Embed(
                title="An Error Occurred",
                description="An error occurred while executing the command.",
                color=0xFF0000,
            ))

    @main.subcommand() # add way more ui to this
    async def support(self, interaction: nextcord.Interaction):
        try:
            embed = nextcord.Embed(
                title="Support Server",
                description="Click [here](https://discord.com/gg/milrato) to join our support server.",
                color=nextcord.Color.blue()
            )
            await interaction.send(embed=embed)
        except Exception as e:
            print(e)
            error_message = "An error occurred. Please try again later."
            await interaction.send(error_message)
    


def setup(bot):
    bot.add_cog(ConnectionInfo(bot))

