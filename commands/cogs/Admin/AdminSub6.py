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
        
    



def setup(bot):
    bot.add_cog(ScheduleCog(bot))