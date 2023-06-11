import asyncio
import openai
import nextcord
from nextcord.ext import commands
from langdetect import detect
import os
import json

# ** ready for production add embeds

class TranslationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.chat_model = None
        self.config_file = "data/translation_settings.json" # Change this to your own file path

    def load_settings(self):
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_settings(self, settings):
        with open(self.config_file, "w") as file:
            json.dump(settings, file, indent=4)

    def is_english(self, text):
        try:
            language = detect(text)
        except Exception:
            return False

        if language == "en":
            return True
        else:
            return False

    async def translate_message(self, message):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Translate the following text to English: {message}",
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
            )
        except Exception as e:
            print(f"Error: {e}")
            return "Translation error"

        translated_message = response.choices[0].text.strip()
        return translated_message

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            if message.content.startswith("Translation is now"):
                return
            else:
                return

        settings = self.load_settings()
        guild_id = str(message.guild.id)
        if guild_id not in settings or not settings[guild_id]["enabled"]:
            return

        # Check if the translation channel is set and if the message is in the correct channel
        translation_channel_id = settings[guild_id].get("translation_channel")
        if translation_channel_id and message.channel.id != translation_channel_id:
            return

        if message.content and not self.is_english(message.content):
            translated_message = await self.translate_message(message.content)
            if translated_message.lower() != message.content.lower():
                await message.channel.send(f"{message.author.mention} said (translated): {translated_message}")


    @nextcord.slash_command(name="servertranslation", description="Enable or disable server translation")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="toggler", description="Enable or disable server translation")
    @commands.has_permissions(administrator=True)
    async def toggle_translation(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        settings = self.load_settings()
        guild_id = str(interaction.guild.id)

        if guild_id not in settings:
            settings[guild_id] = {"enabled": False}

        settings[guild_id]["enabled"] = not settings[guild_id]["enabled"]
        self.save_settings(settings)

        await interaction.send(f"Translation is now {'enabled' if settings[guild_id]['enabled'] else 'disabled'}")

        if not settings[guild_id]["enabled"]:
            await asyncio.sleep(1)
            settings[guild_id]["enabled"] = False
            self.save_settings(settings)


    
    @main.subcommand(name="setchannel", description="Set the channel for server translation")
    @commands.has_permissions(administrator=True)
    async def set_translation_channel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        settings = self.load_settings()
        guild_id = str(interaction.guild.id)

        if guild_id not in settings:
            settings[guild_id] = {"enabled": False, "translation_channel": None}

        settings[guild_id]["translation_channel"] = channel.id
        self.save_settings(settings)

        await interaction.send(f"Translation channel has been set to {channel.mention}")
    
    @main.subcommand(name="setmodel", description="Set the model for server translation")
    @commands.has_permissions(administrator=True)
    async def set_chat_model(self, interaction: nextcord.Interaction, model_key):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_model = openai.Completion.create(engine=model_key)

    @main.subcommand(name="disabler", description="Disable server translation")
    @commands.has_permissions(administrator=True)
    async def disable(self, interaction: nextcord.Interaction):
        self.enabled = False

    @main.subcommand(name="enabler", description="Enable server translation")
    @commands.has_permissions(administrator=True)
    async def enable(self, interaction: nextcord.Interaction):
        self.enabled = True
        
def setup(bot):
    bot.add_cog(TranslationCog(bot))