import nextcord
import json
from nextcord.ext import commands
import os

# Set the path for the folder where the user_notes.json file will be saved
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# Set the file name for storing user notes
USER_NOTES_FILE = os.path.join(data_folder, 'user_notes.json')

class UserNotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_notes = self.load_notes()

    def load_notes(self):
        try:
            with open(USER_NOTES_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_notes(self):
        with open(USER_NOTES_FILE, 'w') as f:
            json.dump(self.user_notes, f, indent=4)

    async def is_admin(self, user: nextcord.User):
        return user.guild_permissions.administrator

    @nextcord.slash_command()
    async def user_notes(self, interaction: nextcord.Interaction, action: str, user: nextcord.User, note: str = None):
        """Store and display notes about a specified user"""

        if not await self.is_admin(interaction.user):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        user_id = str(user.id)

        if action == "add":
            if note:
                self.user_notes.setdefault(user_id, []).append(note)
                self.save_notes()
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
            notes = self.user_notes.get(user_id, [])
            if notes:
                notes_list = "\n".join(f"- {n}" for n in notes)
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
                notes = self.user_notes.get(user_id, [])
                if note in notes:
                    notes.remove(note)
                    self.save_notes()
                    await interaction.response.send_message(
                        content=f":wastebasket: Note deleted for {user.name}: {note}",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message("Note not found.", ephemeral=True)
            else:
                await interaction.response.send_message(
                    content="Please provide a note to delete.",
                    ephemeral=True
                )

def setup(bot):
    bot.add_cog(UserNotes(bot))