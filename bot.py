import asyncio
import importlib
import importlib.util
import os
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from pretty_help import PrettyHelp

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




@bot.event
async def on_ready():
    try:
        with open(r'TODO/Update/changelog2.md', 'r', encoding='utf-8') as f:
            changelog = f.read()
        channel_id = 1112958990171775089  # Replace with the ID of the channel you want to send the embed to

        channel = bot.get_channel(channel_id)
        if channel:
            embed = nextcord.Embed(title="Changelog for Wadder", description=changelog, color=nextcord.Color.orange())
            embed.set_author(name="Wade", icon_url="http://wadderprojects.bhweb.ws/assets/img/waddernew.png")
            embed.set_footer(text="Bot developed by Wade#1781")

            # Add buttons
            view = nextcord.ui.View()

            view.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.link, label="Visit Website", emoji="🌐", url="https://example.com"))
            view.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Support Server", emoji="🤝", url="https://example.com/support"))
            view.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.secondary, label="GitHub Repo", emoji="🔗", url="https://github.com/your_username/your_repo"))
            view.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="Documentation", emoji="📚", url="https://example.com/docs"))
            view.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Bug Report", emoji="🐛", url="https://example.com/bug-report"))
            
            await channel.send(embed=embed, view=view)
        else:
            print(f"Unable to find channel with ID: {channel_id}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")







    



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




#@bot.slash_command()
#async def ss(ctx):
    #servers = bot.guilds
    #server_list = []
    #for server in servers:
        #invite = await server.text_channels[0].create_invite()
        #server_list.append(f"[{server.name}]({invite.url}) (ID: {server.id})")
    #server_list_text = "\n".join(server_list)
    #embed = nextcord.Embed(title="Server List", description=server_list_text, color=nextcord.Color.blue())
   # await ctx.send(embed=embed)

#@bot.event
#async def on_application_command_error(interaction: nextcord.Interaction, error: Exception):
    #if isinstance(error, nextcord.errors.InteractionResponded):
        #print(f"Interaction already responded to: {interaction.command}")
    #else:
        #print(f"Unhandled application command error: {error}")
        #await interaction.send(content="An error occurred while processing the command.")


#@bot.event
#async def on_bot_close():
    #await bot.session.close()
    

bot.run(TOKEN)
