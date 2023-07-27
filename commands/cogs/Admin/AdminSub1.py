import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import asyncio
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("uname") 
password = urllib.parse.quote_plus("pass")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@cluster.mongodb.net/db?retryWrites=true")

db = cluster["commands_db"]
commands_collection = db["commands"]

class CustomCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Custom commands cog loaded')
        await self.populate_commands()
        
    async def populate_commands(self):
        cursor = commands_collection.find({})
        async for document in cursor:
            self.commands[document['_id']] = document['response']
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, name: str, *, response: str):
        if name in self.commands:
            return await ctx.send('That command already exists')
        
        commands_collection.insert_one({'_id': name, 'response': response})
        self.commands[name] = response
        await ctx.send(f'Added `{name}` command')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, name: str, *, response: str):
        if name not in self.commands:
            return await ctx.send('That command does not exist')
        
        self.commands[name] = response
        commands_collection.update_one({'_id': name}, {'$set': {'response': response}}) 
        await ctx.send(f'Edited `{name}` command')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, name: str):
        if name not in self.commands:
            return await ctx.send('That command does not exist')
        
        del self.commands[name]
        commands_collection.delete_one({'_id': name})
        await ctx.send(f'Removed `{name}` command')

    @commands.command()
    async def commands(self, ctx):
        """Lists all custom commands"""
        if not self.commands:
            return await ctx.send('No custom commands set')
            
        embed = nextcord.Embed(title='Custom Commands', color=nextcord.Color.green())
        for name in self.commands:
            embed.add_field(name=name, value=self.commands[name], inline=False)
        await ctx.send(embed=embed)
            
    @commands.Cog.listener() 
    async def on_message(self, message):
        if message.author.bot:
            return
    
        prefix = '!' # change to your bot's prefix
        if not message.content.startswith(prefix):
            return
            
        cmd = message.content[len(prefix):].lower().split(' ')[0] 
        if cmd in self.commands:
            
            if message.author.id in self.cooldowns:
                if time.time() - self.cooldowns[message.author.id] < 5: 
                    # 5 second cooldown
                    return
            
            self.cooldowns[message.author.id] = time.time()
            
            response = self.commands[cmd]
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