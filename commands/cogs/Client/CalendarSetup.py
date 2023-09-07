import json
from datetime import datetime
import nextcord
import calendar
from nextcord.ext import commands
import os
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
calendar_collection = db["calendar_events"]

class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def save_event(self, server_id, event_name, event_datetime):
        event_data = {
            "server_id": server_id,
            "event_name": event_name,
            "datetime": event_datetime
        }
        calendar_collection.insert_one(event_data)

    @nextcord.slash_command(name="calendar")
    @commands.has_permissions(administrator=True)
    async def _calendar(self, interaction: nextcord.Interaction):
        pass

    @_calendar.subcommand(name="create", description="Create a new event")
    async def _create_event(self, interaction: nextcord.Interaction, date: str, time: str, event_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        server_id = str(interaction.guild.id)

        await self.save_event(server_id, event_name, event_datetime)

        await interaction.response.send_message(f"Event '{event_name}' created on {date} at {time}.")

    @_calendar.subcommand(name="view", description="View the calendar with all events")
    async def _view_calendar(self, interaction: nextcord.Interaction, month: int = None, year: int = None):
        if not month or not year:
            today = datetime.today()
            month = today.month
            year = today.year

        server_id = str(interaction.guild.id)
        events = calendar_collection.find({"server_id": server_id})

        if not events:
            await interaction.response.send_message("No events found for this server.")
            return

        events = list(events)
        events.sort(key=lambda x: x['datetime'])

        cal = calendar.monthcalendar(year, month)
        cal_str = f"Calendar for {calendar.month_name[month]} {year}:\n"
        for week in cal:
            for day in week:
                if day == 0:
                    cal_str += "   "  # Blank spaces for days outside the current month
                else:
                    day_str = str(day).zfill(2)
                    events_on_day = [event for event in events if event['datetime'].day == day]
                    if events_on_day:
                        cal_str += f" {day_str}* "  # Add asterisk to indicate events on this day
                    else:
                        cal_str += f" {day_str}  "
            cal_str += "\n"

        event_list = [f"**{event['event_name']}** on {event['datetime'].strftime('%Y-%m-%d %H:%M')}" for event in events]

        await interaction.response.send_message(cal_str + "\nUpcoming events:\n" + "\n".join(event_list))

def setup(bot):
    bot.add_cog(CalendarCog(bot))
