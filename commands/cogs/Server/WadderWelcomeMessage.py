import nextcord
from nextcord.ext import commands
import json

class WelcomeMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_file = "data/welcome_settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        welcome_channel_id = self.settings.get(str(guild.id), {}).get("welcome_channel_id")
        welcome_message = self.settings.get(str(guild.id), {}).get("welcome_message")

        if welcome_channel_id:
            channel = guild.get_channel(welcome_channel_id)
            if channel:
                embed = nextcord.Embed(
                    title=f"Welcome to {guild.name}!",
                    description=f"{member.mention} has joined the server.",
                    color=0x00ff00
                )
                user = await self.bot.fetch_user(member.id)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_footer(text=f"User ID: {member.id}")
                await channel.send(embed=embed)

        if welcome_message:
            try:
                await member.send(welcome_message)
            except nextcord.errors.Forbidden:
                pass

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        guild_id = str(interaction.guild.id)
        self.settings.setdefault(guild_id, {})
        self.settings[guild_id]["welcome_channel_id"] = channel.id
        self.save_settings()
        await interaction.send(f"Welcome channel set to {channel.mention}.")

    @setwelcomechannel.error
    async def setwelcomechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid text channel.")
        else:
            await ctx.send("An error occurred while processing this command.")

    

def setup(bot):
    bot.add_cog(WelcomeMessage(bot))