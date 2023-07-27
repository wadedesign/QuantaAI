from datetime import time
import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import asyncio
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009") 
password = urllib.parse.quote_plus("Celina@12")
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