import asyncio
import os
import json
import nextcord
from nextcord.ext import commands
import openai

## !Fix not being able to disable the ban hammer

openai.api_key = os.getenv("OPENAI_API_KEY")

class BanHammer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_file = "data/ban_hammer_settings.json"
        if not os.path.isfile(self.settings_file):
            with open(self.settings_file, "w") as f:
                json.dump({}, f)
        self.warns = {}

    def _load_settings(self):
        with open(self.settings_file, "r") as f:
            return json.load(f)

    def _save_settings(self, settings):
        with open(self.settings_file, "w") as f:
            json.dump(settings, f)

    async def is_ban_hammer_enabled(self, guild_id):
        settings = self._load_settings()
        return settings.get(str(guild_id), {}).get("enabled", False)
    
    async def warn_user(self, user, guild):
        user_id = str(user.id)
        if user_id not in self.warns:
            self.warns[user_id] = 0
        self.warns[user_id] += 1

        if self.warns[user_id] >= 5:
            # Temporarily ban the user for 3 days
            await user.ban(reason="Inappropriate messages detected by Ban Hammer", delete_message_days=0)
            await asyncio.sleep(3 * 24 * 60 * 60)  # Wait for 3 days
            await guild.unban(user)
            self.warns[user_id] = 0
            return True
        return False



    @nextcord.slash_command(name="banhammer", description="Enable or disable the Ban Hammer")
    @commands.has_permissions(administrator=True)
    async def banhammer(self, interaction: nextcord.Interaction):
        settings = self._load_settings()
        guild_id = str(interaction.guild.id)
        enabled = settings.get(guild_id, {}).get("enabled", False)

        if enabled:
            settings[guild_id]["enabled"] = False
            message = "Ban Hammer has been disabled."
        else:
            if guild_id not in settings:
                settings[guild_id] = {}
            settings[guild_id]["enabled"] = True
            message = "Ban Hammer has been enabled."

        self._save_settings(settings)
        await interaction.send(message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not await self.is_ban_hammer_enabled(message.guild.id):
            return

        try:
            response = openai.Moderation.create(input=message.content)
            flagged = response['results'][0]['flagged']
        except Exception as e:
            print(f"Error while calling OpenAI API: {e}")
            return

        if flagged:
            banned = await self.warn_user(message.author, message.guild)
            if banned:
                await message.channel.send(f"{message.author.name} has been temporarily banned for 3 days due to inappropriate messages.")
            else:
                warning_message = f"{message.author.name}, this is a warning. You have sent an inappropriate message. "\
                                  f"You have {self.warns[str(message.author.id)]} out of 5 warnings. "\
                                  f"Reaching 5 warnings will result in a temporary ban for 3 days."
                await message.channel.send(warning_message)
                try:
                    await message.author.send(warning_message)
                except nextcord.errors.Forbidden:
                    pass


def setup(bot):
    bot.add_cog(BanHammer(bot))
    print("BanHammer Ready!")