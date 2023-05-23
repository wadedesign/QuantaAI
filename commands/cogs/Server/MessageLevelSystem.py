import nextcord
from nextcord.ext import commands
from collections import defaultdict

# ! Delete this


class Gamification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.points = defaultdict(int)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not message.content.startswith(self.bot.command_prefix):
            self.points[message.author.id] += 1


    @nextcord.slash_command(name="points", description="Check your points")
    async def check_points(self, interaction: nextcord.Interaction):
        user_points = self.points[interaction.user.id]
        await interaction.response.send_message(f"{interaction.user.name}, you have {user_points} points.")

    @nextcord.slash_command(name="leaderboard", description="Show the leaderboard")
    async def show_leaderboard(self, interaction: nextcord.Interaction):
        leaderboard = sorted(self.points.items(), key=lambda x: x[1], reverse=True)
        top_users = []

        for user_id, points in leaderboard[:10]:
            user = await self.bot.fetch_user(user_id)
            top_users.append(f"{user.name}: {points} points")

        leaderboard_text = "\n".join(top_users)
        await interaction.response.send_message(f"**Leaderboard**\n\n{leaderboard_text}")

def setup(bot):
    bot.add_cog(Gamification(bot))
