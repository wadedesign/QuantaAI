import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
commands_collection = db["custom_commands"]


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.load_custom_commands()

    def load_custom_commands(self):
        commands_data = commands_collection.find({})
        for command_data in commands_data:
            name = command_data["_id"]
            response = command_data["response"]
            self.commands[name] = response

    @commands.group(name='cc', invoke_without_command=True)
    async def custom_commands(self, ctx):
        """Manage custom commands."""
        await ctx.send('Invalid subcommand. Use `create`, `edit`, `delete`, or `list`.')

    @custom_commands.command(name='create')
    @commands.has_permissions(administrator=True)
    async def create_custom_command(self, ctx, name: str, *, response: str):
        """Create a new custom command."""
        if name in self.commands:
            await ctx.send(f'Error: `{name}` already exists.')
            return

        self.commands[name] = response
        commands_collection.insert_one({"_id": name, "response": response})
        await ctx.send(f'Successfully created custom command: `{name}`')

    @custom_commands.command(name='edit')
    @commands.has_permissions(administrator=True)
    async def edit_custom_command(self, ctx, name: str, *, response: str):
        """Edit an existing custom command."""
        if name not in self.commands:
            await ctx.send(f'Error: `{name}` does not exist.')
            return

        self.commands[name] = response
        commands_collection.update_one({"_id": name}, {"$set": {"response": response}})
        await ctx.send(f'Successfully edited custom command: `{name}`')

    @custom_commands.command(name='delete')
    @commands.has_permissions(administrator=True)
    async def delete_custom_command(self, ctx, name: str):
        """Delete an existing custom command."""
        if name not in self.commands:
            await ctx.send(f'Error: `{name}` does not exist.')
            return

        del self.commands[name]
        commands_collection.delete_one({"_id": name})
        await ctx.send(f'Successfully deleted custom command: `{name}`')

    @custom_commands.command(name='list')
    async def list_custom_commands(self, ctx):
        """List all custom commands."""
        if not self.commands:
            await ctx.send('There are no custom commands.')
            return

        embed = nextcord.Embed(title='Custom Commands', color=0x3cff00)
        for name, response in self.commands.items():
            embed.add_field(name=name, value=response, inline=False)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        command = message.content.strip().lower()

        if command in self.commands:
            response = self.commands[command]
            await message.channel.send(response)


def setup(bot):
    bot.add_cog(CustomCommands(bot))

    
    
    
    
    
    # CustomCommands cog allows server admins to create custom text commands that trigger specific responses from the bot.

# Use the cc create command to create a new custom command. For example, to create a custom command named !hello that responds with Hello, world!, an admin could run the following command:
# cc create hello Hello, world!

# Use the cc edit command to edit an existing custom command. For example, to change the response for the !hello command to Hi there!, an admin could run the following command:
# cc edit hello Hi there!

# Use the cc delete command to delete an existing custom command. For example, to delete the !hello command, an admin could run the following command:
# cc delete hello

# Use the cc list command to list all existing custom commands. An admin could run the following command to see a list of all custom commands:
# cc list

# Whenever a user sends a message that matches a custom command, the bot will respond with the associated response. For example, if a user sends a message that says !hello, the bot will respond with Hi there! if that was the last response set by an admin.