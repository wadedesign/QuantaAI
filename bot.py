import asyncio
import datetime
import importlib
import importlib.util
import os
import traceback
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from pretty_help import PrettyHelp
from typing import Tuple, List
from logger import setup_logger

# added by wade



ending_note = "For additional assistance, contact a moderator."
color = 0x00FF00

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = nextcord.Intents.all()
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all(), help_command=PrettyHelp(), activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="the community"))
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




def read_changelog(file_path: str) -> str:
    """
    Reads the changelog from the specified file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Changelog file not found at: {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred while reading the changelog file:\n{str(e)}")
        traceback.print_exc()
        return ""

def create_embed(changelog: str) -> nextcord.Embed:
    """
    Creates an embed with the given changelog string.
    """
    embed = nextcord.Embed(title="Changelog for Wadder", description=changelog, color=nextcord.Color.orange())
    embed.set_author(name=os.getenv('BOT_NAME', 'Wade'), icon_url=os.getenv('BOT_ICON_URL', "http://wadderprojects.bhweb.ws/assets/img/waddernew.png"))
    embed.set_footer(text=f"Bot developed by {os.getenv('BOT_DEVELOPER', 'Wade#1781')}")
    embed.set_thumbnail(url=os.getenv('BOT_THUMBNAIL_URL', 'http://wadderprojects.bhweb.ws/assets/img/waddernew.png')) 
    embed.timestamp = datetime.datetime.utcnow()  # Adding a timestamp
    return embed

def create_view(buttons: List[Tuple[nextcord.ButtonStyle, str, str, str]]) -> nextcord.ui.View:
    """
    Creates a view with buttons.
    """
    view = nextcord.ui.View()
    for style, label, emoji, url in buttons:
        view.add_item(nextcord.ui.Button(style=style, label=label, emoji=emoji, url=url))
    return view

@bot.event
async def on_ready():
    """
    Reads the changelog file and sends it as an embed to a specified channel.
    """
    try:
        changelog = read_changelog(os.getenv('CHANGELOG_PATH', 'QuantaProjects/Update/qchangelogsmd/changelog2.md'))

        channel_id = int(os.getenv('CHANNEL_ID', '1112958990171775089'))  # Replace with the ID of the channel you want to send the embed to

        # Send the embed
        channel = bot.get_channel(channel_id)
        if channel:
            embed = create_embed(changelog)
            buttons = [
                (nextcord.ButtonStyle.link, "Visit Website", "🌐", "https://example.com"),
                (nextcord.ButtonStyle.primary, "Support Server", "🤝", "https://example.com/support"),
                (nextcord.ButtonStyle.secondary, "GitHub Repo", "🔗", "https://github.com/your_username/your_repo"),
                (nextcord.ButtonStyle.success, "Documentation", "📚", "https://example.com/docs"),
                (nextcord.ButtonStyle.danger, "Bug Report", "🐛", "https://example.com/bug-report")
            ]
            view = create_view(buttons)
            await channel.send(embed=embed, view=view)
        else:
            print(f"Unable to find channel with ID: {channel_id}")

    except Exception as e:
        # Logging the exception with traceback
        print(f"An error occurred:\n{str(e)}")
        traceback.print_exc()







    



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




@bot.slash_command()
async def ss(ctx):
    servers = bot.guilds
    server_list = []
    for server in servers:
        invite = await server.text_channels[0].create_invite()
        server_list.append(f"[{server.name}]({invite.url}) (ID: {server.id})")
    server_list_text = "\n".join(server_list)
    embed = nextcord.Embed(title="Server List", description=server_list_text, color=nextcord.Color.blue())
    await ctx.send(embed=embed)

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

