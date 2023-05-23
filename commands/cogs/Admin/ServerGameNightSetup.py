import asyncio
from datetime import datetime, timedelta
import uuid
import nextcord
from nextcord.ext import commands, tasks

# def needs some work! (add a channel for it. ) * 


#ex: /gamenight create Arma3 2023-04-15 20:30


class GameNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_nights = {}
        self.reminder_minutes = 15
        self.reminder_task.start()

    def cog_unload(self):
        self.reminder_task.cancel()

    @tasks.loop(minutes=1)
    async def reminder_task(self):
        now = datetime.utcnow()
        for event_id, event in list(self.game_nights.items()):
            if event["datetime"] - timedelta(minutes=self.reminder_minutes) <= now:
                await self.send_reminder(event)
                del self.game_nights[event_id]

    async def send_reminder(self, event):
        embed = nextcord.Embed(title="Game Night Reminder", description=f"Game night **{event['name']}** is starting in {self.reminder_minutes} minutes!", color=0x3cff00)
        for user_id in event["rsvp"]:
            user = self.bot.get_user(user_id)
            if user:
                await user.send(embed=embed)

    async def get_or_create_game_night_channel(self, guild):
        channel = nextcord.utils.get(guild.text_channels, name="game-nights")
        if not channel:
            overwrites = {
                guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
            }
            channel = await guild.create_text_channel("game-nights", overwrites=overwrites)
        return channel

    async def update_game_night_embed(self, ctx, event_id):
        channel = await self.get_or_create_game_night_channel(ctx.guild)
        event = self.game_nights[event_id]
        embed = nextcord.Embed(
            title=f"Game Night: {event['name']}",
            description=f"Date & Time: {event['datetime'].strftime('%Y-%m-%d %H:%M')} UTC",
            color=0x3cff00
        )
        rsvp_users = [self.bot.get_user(user_id) for user_id in event["rsvp"]]
        rsvp_names = [user.display_name for user in rsvp_users if user]
        embed.add_field(name="RSVP List", value="\n".join(rsvp_names) if rsvp_names else "No RSVPs yet")

        if "message" in event:
            try:
                message = await channel.fetch_message(event["message"])
                await message.edit(embed=embed)
            except (nextcord.NotFound, nextcord.HTTPException):
                pass
        else:
            message = await channel.send(embed=embed)
            event["message"] = message.id
            await message.add_reaction("👍")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and reaction.message.author == self.bot.user:
            event_id = None
            for event in self.game_nights.values():
                if event["message"] == reaction.message.id:
                    event_id = event["id"]
                    break

            if event_id is not None and str(reaction.emoji) == "👍":
                self.game_nights[event_id]["rsvp"].add(user.id)
                await self.update_game_night_embed(reaction.message.channel, event_id)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if not user.bot and reaction.message.author == self.bot.user:
            event_id = None
            for event in self.game_nights.values():
                if event["message"] == reaction.message.id:
                    event_id = event["id"]
                    break

            if event_id is not None and str(reaction.emoji) == "👍":
                self.game_nights[event_id]["rsvp"].remove(user.id)
                await self.update_game_night_embed(reaction.message.channel, event_id)
    @nextcord.slash_command(name="gamenight", description="Start a new game of Number Guess")
    async def main(self, interaction: nextcord.Interaction):
        pass
    
    
    @main.subcommand(name="creategamenight")
    async def create_game_night(self, interaction: nextcord.Interaction, name: str, date: str, time: str):
        event_id = str(uuid.uuid4())
        event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        self.game_nights[event_id] = {
            "id": event_id,
            "name": name,
            "datetime": event_datetime,
            "rsvp": set()
        }
        await self.update_game_night_embed(interaction, event_id)

    @main.subcommand(name="listgamenights")
    async def list_game_nights(self, interaction: nextcord.Interaction):
        if not self.game_nights:
            await interaction.send("There are no game nights scheduled.")
            return

        embed = nextcord.Embed(title="Game Nights", color=0x3cff00)
        for event in self.game_nights.values():
            rsvp_users = [self.bot.get_user(user_id) for user_id in event["rsvp"]]
            rsvp_names = [user.display_name for user in rsvp_users if user]
            embed.add_field(
                name=f"{event['name']} - {event['datetime'].strftime('%Y-%m-%d %H:%M')}",
                value="\n".join(rsvp_names) if rsvp_names else "No RSVPs yet",
                inline=False
            )

        await interaction.send(embed=embed)

    @main.subcommand(name="cancelgamenight")
    async def cancel_game_night(self, interaction: nextcord.Interaction, event_id: str):
        if event_id not in self.game_nights:
            await interaction.send("Invalid event ID.")
            return

        del self.game_nights[event_id]
        await interaction.send("Game night cancelled.")
        
def setup(bot):
    bot.add_cog(GameNight(bot))        