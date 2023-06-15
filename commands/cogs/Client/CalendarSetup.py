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

        event_datetime = f"{date} {time}"
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
        event_list = [f"**{event['event_name']}** on {event['datetime']}" for event in events]

        cal = calendar.TextCalendar()
        cal_str = cal.formatmonth(year, month)

        await interaction.response.send_message(f"Calendar for {calendar.month_name[month]} {year}:\n```\n{cal_str}\n```\nUpcoming events:\n" + "\n".join(event_list))


def setup(bot):
    bot.add_cog(CalendarCog(bot))