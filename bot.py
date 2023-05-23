import importlib
import importlib.util
import os
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from pretty_help import PrettyHelp
from Logs.logger import setup_logger

ending_note = "For additional assistance, contact a moderator."
color = 0x00FF00

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = nextcord.Intents.all()
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all(), help_command=PrettyHelp())
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID"))


@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, nextcord.ApplicationCheckFailure):
        await interaction.response.send_message(":warning: You are not authorized to use this command!")
    else:
        await interaction.response.send_message(f":x: An error occurred while processing this command. \n```py\n{error}\n```")


async def update_presence():
    num_guilds = len(bot.guilds)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{num_guilds} guilds | Check out: github.com/wadder12"))


with open(r'TODO/Update/changelog.TOML', 'r', encoding='utf-8') as f:
    changelog = f.read()
changelog_channel_id = 1099128349978275863


@bot.event
async def on_ready():
    await update_presence()
    print('Logged in as {0.user}'.format(bot))
    changelog_channel = bot.get_channel(changelog_channel_id)
    embed = nextcord.Embed(title="Changelog for Wadder", description=changelog, color=0xFF5733)
    embed.add_field(name="Developer", value="Wade#1781", inline=False)
    await changelog_channel.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    await update_presence()


@bot.event
async def on_guild_remove(guild):
    await update_presence()


slashcommands_dir = "commands/slash_commands"
cogs_dir = "commands/cogs"

for root, dirs, files in os.walk(slashcommands_dir):
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(root, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.setup(bot)

loaded_cogs = []
loaded_folders = []

for root, dirs, files in os.walk(cogs_dir):
    if root in loaded_folders:
        continue
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{root.replace('/', '.').replace(os.sep, '.')}.{filename[:-3]}"
            bot.load_extension(module_name)
    if "__init__.py" in files:
        loaded_folders.append(root)


@bot.slash_command(name="setuplogger", description="Sets up the logger (Admin only)")
@commands.has_permissions(administrator=True)
async def setuplogger(interaction: nextcord.Interaction):
    await setup_logger(interaction)


@setuplogger.error
async def setuplogger_error(interaction: nextcord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.send("You do not have the required permissions to use this command.", ephemeral=True)


@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error: Exception):
    if isinstance(error, nextcord.errors.InteractionResponded):
        print(f"Interaction already responded to: {interaction.command}")
    else:
        print(f"Unhandled application command error: {error}")
        await interaction.send(content="An error occurred while processing the command.")


@bot.event
async def on_bot_close():
    await bot.session.close()


bot.run(TOKEN)
