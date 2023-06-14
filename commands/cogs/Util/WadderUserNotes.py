import nextcord
from nextcord.ext import commands
import urllib.parse
from pymongo import MongoClient

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
user_notes_collection = db["user_notes"]

class UserNotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_admin(self, user: nextcord.User):
        return user.guild_permissions.administrator

    @nextcord.slash_command(name="user_memoirs", description="Store and display notes about a specified user")
    async def user_notes(self, interaction: nextcord.Interaction, action: str, user: nextcord.User, note: str = None):
        if not await self.is_admin(interaction.user):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        user_id = str(user.id)

        if action == "add":
            if note:
                user_notes_collection.update_one({"user_id": user_id}, {"$push": {"notes": note}}, upsert=True)
                await interaction.response.send_message(
                    content=f":white_check_mark: Note added for {user.name}: {note}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    content="Please provide a note to add.",
                    ephemeral=True
                )
        elif action == "view":
            result = user_notes_collection.find_one({"user_id": user_id})
            if result and "notes" in result:
                notes_list = "\n".join(f"- {n}" for n in result["notes"])
                embed = nextcord.Embed(
                    title=f"Notes for {user.name}",
                    description=notes_list,
                    color=nextcord.Color.blue()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"No notes found for {user.name}.",
                    ephemeral=True
                )
        elif action == "delete":
            if note:
                result = user_notes_collection.find_one({"user_id": user_id})
                if result and "notes" in result:
                    if note in result["notes"]:
                        user_notes_collection.update_one({"user_id": user_id}, {"$pull": {"notes": note}})
                        await interaction.response.send_message(
                            content=f":wastebasket: Note deleted for {user.name}: {note}",
                            ephemeral=True
                        )
                    else:
                        await interaction.response.send_message("Note not found.", ephemeral=True)
                else:
                    await interaction.response.send_message("No notes found for the user.", ephemeral=True)
            else:
                await interaction.response.send_message(
                    content="Please provide a note to delete.",
                    ephemeral=True
                )

def setup(bot):
    bot.add_cog(UserNotes(bot))
