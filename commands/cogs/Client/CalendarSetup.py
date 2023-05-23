import json
from datetime import datetime
import nextcord
import calendar
from nextcord.ext import commands
import os 


class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.calendar_data = 'data/calendar_data.json'
        
        if not os.path.exists(self.calendar_data):
            with open(self.calendar_data, 'w') as f:
                json.dump({}, f)

    @nextcord.slash_command(name="calendar", description="Manage calendar events")
    @commands.has_permissions(administrator=True)
    async def _calendar(self, interaction: nextcord.Interaction):
        pass

    @_calendar.subcommand(name="create", description="Create a new event")
    async def _create_event(self, interaction: nextcord.Interaction, date: str, time: str, event_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        event_datetime = f"{date} {time}"
        
        with open(self.calendar_data, 'r') as f:
            data = json.load(f)

        server_id = str(interaction.guild.id)
        if server_id not in data:
            data[server_id] = []

        data[server_id].append({
            'event_name': event_name,
            'datetime': event_datetime
        })

        with open(self.calendar_data, 'w') as f:
            json.dump(data, f)

        await interaction.response.send_message(f"Event '{event_name}' created on {date} at {time}.")

    @_calendar.subcommand(name="view", description="View the calendar with all events")
    async def _view_calendar(self, interaction: nextcord.Interaction, month: int = None, year: int = None):
        if not month or not year:
            today = datetime.today()
            month = today.month
            year = today.year

        with open(self.calendar_data, 'r') as f:
            data = json.load(f)

        server_id = str(interaction.guild.id)
        if server_id not in data:
            await interaction.response.send_message("No events found for this server.")
            return

        events = data[server_id]
        if not events:
            await interaction.response.send_message("No events found for this server.")
            return

        events.sort(key=lambda x: x['datetime'])
        event_list = [f"**{event['event_name']}** on {event['datetime']}" for event in events]

        cal = calendar.TextCalendar()
        cal_str = cal.formatmonth(year, month)

        await interaction.response.send_message(f"Calendar for {calendar.month_name[month]} {year}:\n```\n{cal_str}\n```\nUpcoming events:\n" + "\n".join(event_list))

def setup(bot):
    bot.add_cog(CalendarCog(bot))

