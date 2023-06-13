import datetime
import nextcord
from nextcord.ext import commands
import asyncio
from time import time


## Todo: Add a more sub commands (25 only)
#!!


class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduled_events = dict()

    async def execute_scheduled_event(self, event_key):
        event = self.scheduled_events[event_key]
        t, function, args, kwargs = event
        await asyncio.sleep(t - time())

        try:
            await function(*args, **kwargs)
        except Exception as e:
            import traceback
            print("[EXCEPTION IN SCHEDULED EVENT]")
            print(e)
            print(traceback.format_exc())

        del self.scheduled_events[event_key]

    @nextcord.slash_command(name="quanta4")
    async def main(self, interaction: nextcord.Interaction):
        pass
    @main.subcommand(name="schedulemessage", description="Schedules a message to be sent after the specified delay (in seconds).")
    @commands.has_permissions(administrator=True)
    async def schedulemessage(self, interaction: nextcord.Interaction, delay: int, message: str):
        await interaction.response.send_message(f"Scheduling your message in {delay} seconds.")
        event_key = object()
        t = time() + delay
        function = interaction.channel.send
        args = (message,)

        self.scheduled_events[event_key] = (t, function, args, {})
        asyncio.create_task(self.execute_scheduled_event(event_key))
        
    @main.subcommand(name="qwhisper", description="Whispers a message to a user.")
    @commands.is_owner()
    async def whisper(self, interaction: nextcord.Interaction, user_id: int, *, msg: str):
        user = await self.bot.fetch_user(user_id)
        try:
            # Show loading animation
            loading_message = await interaction.response.send_message("Sending message...")

            animation_frames = [
                "💌 Sending message",
                "💌 Sending message.",
                "💌 Sending message..",
                "💌 Sending message..."
            ]

            for frame in animation_frames:
                await loading_message.edit(content=frame)
                await asyncio.sleep(0.5)

            # Send the message
            embed = nextcord.Embed(colour=nextcord.Colour.red())
            embed.title = "You've received a message from a developer!"
            embed.add_field(name="Developer:", value=interaction.message.author, inline=False)
            embed.add_field(name="Time:", value=datetime.datetime.now().strftime("%A, %B %-d %Y at %-I:%M%p").replace("PM", "pm").replace("AM", "am"), inline=False)
            embed.add_field(name="Message:", value=msg, inline=False)
            embed.set_thumbnail(url=interaction.message.author.avatar_url)
            await user.send(embed=embed)

            await interaction.followup.send_message('Successfully sent message to {}'.format(user_id))
        except:
            await interaction.followup.send_message(':x: Failed to send message to user_id `{}`.'.format(user_id))

            



def setup(bot):
    bot.add_cog(ScheduleCog(bot))