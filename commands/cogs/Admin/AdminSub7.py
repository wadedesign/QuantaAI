import nextcord
from nextcord import *
from nextcord.ext import commands
import random
from nextcord.ui import Button, View
from datetime import datetime
import json
import time
import os

class AwayFromKeyboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_file = 'data/afk.json'
        self.create_afk_file()
        
    def create_afk_file(self):
        os.makedirs(os.path.dirname(self.afk_file), exist_ok=True)
        if not os.path.exists(self.afk_file):
            with open(self.afk_file, 'w') as f:
                json.dump({}, f)
    
    async def update_data(self, afk, user):
        if not f'{user.id}' in afk:
            afk[f'{user.id}'] = {}
            afk[f'{user.id}']['AFK'] = 'False'
            afk[f'{user.id}']['reason'] = 'None'
    
    async def time_formatter(self, seconds: float):
        '''
        Convert UNIX time to human readable time.
        '''
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + "d, ") if days else "") + \
            ((str(hours) + "h, ") if hours else "") + \
            ((str(minutes) + "m, ") if minutes else "") + \
            ((str(seconds) + "s, ") if seconds else "")
        return tmp[:-2]
    
    @commands.Cog.listener()
    async def on_message(self, message):
        with open('data/afk.json', 'r') as f:
            afk = json.load(f)

        for user_mention in message.mentions:
            user_id = f'{user_mention.id}'
            if user_id in afk and afk[user_id]['AFK'] == 'True':
                if message.author.bot:
                    return

                reason = afk[user_id]['reason']
                meth = int(time.time()) - int(afk[user_id]['time'])
                been_afk_for = await self.time_formatter(meth)
                embed = nextcord.Embed(description=f'{user_mention.name} is currently AFK!\nReason: {reason}')
                await message.channel.send(content=message.author.mention, embed=embed)

                meeeth = int(afk[user_id]['mentions']) + 1
                afk[user_id]['mentions'] = meeeth
                with open('db/afk.json', 'w') as f:
                    json.dump(afk, f)
        
        if not message.author.bot:
            await self.update_data(afk, message.author)

            if afk[f'{message.author.id}']['AFK'] == 'True':
                meth = int(time.time()) - int(afk[f'{message.author.id}']['time'])
                been_afk_for = await self.time_formatter(meth)
                mentionz = afk[f'{message.author.id}']['mentions']

                embed = nextcord.Embed(description=f'Welcome back {message.author.name}!', color=0x00ff00)
                embed.add_field(name="You've been AFK for:", value=been_afk_for, inline=False)
                embed.add_field(name='Times you were mentioned while AFK:', value=mentionz, inline=False)

                await message.channel.send(content=message.author.mention, embed=embed)
                
                afk[f'{message.author.id}']['AFK'] = 'False'
                afk[f'{message.author.id}']['reason'] = 'None'
                afk[f'{message.author.id}']['time'] = '0'
                afk[f'{message.author.id}']['mentions'] = 0
                
                with open('data/afk.json', 'w') as f:
                    json.dump(afk, f)
                
                try:
                    await message.author.edit(nick=f'{message.author.display_name[5:]}')
                except:
                    print(f'I was not able to edit [{message.author}].')
        
        with open('data/afk.json', 'w') as f:
            json.dump(afk, f)

    @nextcord.slash_command(name='afk', description='Set your AFK to let others know when they ping you')
    async def afk(self, interac: Interaction, reason):
        with open('data/afk.json', 'r') as f:
            afk = json.load(f)

        if not reason:
            reason = 'None'
        
        await self.update_data(afk, interac.user)
        afk[f'{interac.user.id}']['AFK'] = 'True'
        afk[f'{interac.user.id}']['reason'] = f'{reason}'
        afk[f'{interac.user.id}']['time'] = int(time.time())
        afk[f'{interac.user.id}']['mentions'] = 0

        embed = nextcord.Embed(description=f"I've set your AFK, {interac.user.display_name}!\nReason: {reason}", color=0x00ff00)
        await interac.response.send_message(content=interac.user.mention, embed=embed)

        with open('data/afk.json', 'w') as f:
            json.dump(afk, f)
        
        try:
            await interac.user.edit(nick=f'[AFK]{interac.user.display_name}')
        except:
            print(f'I was not able to edit [{interac.user}].')
    
    @nextcord.slash_command(name='removeafk', description='Remove your AFK status')
    async def remove_afk(self, interac: Interaction):
        with open('data/afk.json', 'r') as f:
            afk = json.load(f)
        
        await self.update_data(afk, interac.user)
        if afk[f'{interac.user.id}']['AFK'] == 'True':
            afk[f'{interac.user.id}']['AFK'] = 'False'
            afk[f'{interac.user.id}']['reason'] = 'None'
            afk[f'{interac.user.id}']['time'] = '0'
            afk[f'{interac.user.id}']['mentions'] = 0
            
            with open('data/afk.json', 'w') as f:
                json.dump(afk, f)
            
            try:
                await interac.user.edit(nick=f'{interac.user.display_name[5:]}')
            except:
                print(f'I was not able to edit [{interac.user}].')
            
            await interac.response.send_message(content=f"{interac.user.mention} Your AFK status has been removed.")
        else:
            await interac.response.send_message(content=f"{interac.user.mention} You are not currently AFK.")

def setup(bot):
    bot.add_cog(AwayFromKeyboard(bot))
    print('AFK Cog is loaded')

