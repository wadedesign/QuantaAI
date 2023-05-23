# Autor: Wade
import json
import nextcord
from nextcord.ext import commands
from nextcord import File
from easy_pil import Editor, Font, load_image_async


## Todo: Make it where the user can upload a photo to use as the background

def get_config(guild_id):
    try:
        with open("data/configwelcome.json", "r") as f:
            configs = json.load(f)
            return configs[str(guild_id)]
    except KeyError:
        return None
def create_config_file_if_not_exists():
    try:
        with open("data/configwelcome.json", "r") as f:
            pass
    except FileNotFoundError:
        with open("data/configwelcome.json", "w") as f:
            f.write("{}")

create_config_file_if_not_exists()
class WelcomeCogSET(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = get_config(member.guild.id)
        if config and config["welcome"]:
            channel = member.guild.get_channel(int(config["welcome_channel"]))

            background = Editor("test12.png") # You can use any image you want here as background
            profile_image = await load_image_async(str(member.avatar.url))

            profile = Editor(profile_image).resize((150, 150)).circle_image()
            poppins = Font.poppins(size=50, variant="bold")

            poppins_small = Font.poppins(size=20, variant="light")

            background.paste(profile, (325, 90))
            background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)

            background.text((400, 260), f"Welcome to {member.guild.name}!", color="white", font=poppins, align="center")
            background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")

            file = File(fp=background.image_bytes, filename="test12.png")
            await channel.send(f"Hello {member.mention}! Welcome to **{member.guild.name}**! For more information, go to #rules.")
            await channel.send(file=file)


    @nextcord.slash_command(name="welcome_setup", description="Set up the welcome message.")
    @commands.has_permissions(administrator=True)
    async def welcome_setup(self, interaction: nextcord.Interaction, enable: bool, channel: nextcord.TextChannel):
        config = get_config(interaction.guild.id)

        if config is None:
            config = {}

        config.update({"welcome": enable, "welcome_channel": str(channel.id)})

        with open("data/configwelcome.json", "r") as f:
            configs = json.load(f)

        configs[str(interaction.guild.id)] = config

        with open("data/configwelcome.json", "w") as f:
            json.dump(configs, f, indent=4)

        await interaction.send(f"Welcome message has been {'enabled' if enable else 'disabled'} and set to channel {channel.mention}.")

def setup(bot):
    bot.add_cog(WelcomeCogSET(bot))