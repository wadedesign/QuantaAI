import nextcord
from nextcord.ext import commands
import plotly.graph_objects as go
import os 
class MessageStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def message_stats(self, ctx):
        messages = await ctx.channel.history(limit=100).flatten()  # Fetches the latest 100 messages

        users = {}
        for message in messages:
            if message.author.bot:  # Skip messages sent by bots
                continue

            if message.author.id not in users:
                users[message.author.id] = 1
            else:
                users[message.author.id] += 1

        usernames = []
        message_counts = []
        for user_id, count in users.items():
            user = await self.bot.fetch_user(user_id)
            usernames.append(user.name)
            message_counts.append(count)

        # Create a bar chart using Plotly
        fig = go.Figure(data=go.Bar(x=usernames, y=message_counts))
        fig.update_layout(
            title="Message Statistics",
            xaxis_title="User",
            yaxis_title="Number of Messages",
        )

        # Save the chart as an image
        chart_filename = "message_stats.png"
        fig.write_image(chart_filename)

        # Send the chart as an image attachment
        with open(chart_filename, "rb") as file:
            chart_image = nextcord.File(file)
            await ctx.send(file=chart_image)

        # Remove the chart image file
        os.remove(chart_filename)

def setup(bot):
    bot.add_cog(MessageStats(bot))
