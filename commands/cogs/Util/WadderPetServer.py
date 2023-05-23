import json
import os
import random
import threading
import nextcord
from nextcord.ext import commands, tasks
import asyncio

class PetCog(commands.Cog): # good, change to where it shows the user and use embeds
    def __init__(self, bot):
        self.bot = bot
        self.health = 100
        self.happiness = 100
        self.hunger = 100
        self.currstatus = "awake"
        self.tick.start()

    def cog_unload(self):
        self.tick.cancel()

    @tasks.loop(minutes=1)
    async def tick(self):
        self.hunger -= 5
        self.happiness -= 2
        print("tick activated")
        if self.hunger <= 0:
            self.hunger = 0
            self.health -= 5
            print("starving!")
        if self.happiness <= 0:
            self.happiness = 0
            self.health -= 10
        if self.health <= 0:
            self.health = 0
        self.printdetails()

    def printdetails(self):
        print("Health: " + str(self.health) + "\n" + "Hunger: " + str(self.hunger) + "\n" + "Happiness: " + str(self.happiness))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setup complete!")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print(f'Ping: {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def feed(self, ctx):
        self.hunger += 10
        self.happiness += 2
        if self.hunger >= 100:
            self.hunger = 100
        if self.happiness >= 100:
            self.happiness = 100
        await ctx.send(f'Nom nom')
        print("Fed. Current hunger: " + self.hunger)

    @commands.command()
    async def snuggle(self, ctx):
        self.happiness += 10
        if self.happiness >= 100:
            self.happiness = 100
        await ctx.send(f'Zzzz')
        print("Snuggled. Current happiness: " + self.happiness)

    @commands.command()
    async def pet(self, ctx):
        self.happiness += 10
        if self.happiness >= 100:
            self.happiness = 100
        await ctx.send(f'mew')
        print("Petted. Current happiness: " + self.happiness)

    @commands.command()
    async def sleep(self, ctx):
        print(self.currstatus)
        if self.currstatus == "awake":
            self.happiness += 5
            self.health += 10
            if self.happiness >= 100:
                self.happiness = 100
            if self.health >= 100:
                self.health = 100
            self.currstatus = "sleeping"
            print("now sleeping")
        else:
            print("already sleeping")
            await ctx.send("meow??")

    @commands.command()
    async def wakeup(self, ctx):
        if self.currstatus == "sleeping":
            self.health += 5
            if self.health >= 100:
                self.health = 100
            self.currstatus = "awake"
        else:
            await ctx.send("meow??")


    @commands.command()
    async def rename(self, ctx, name):
        print("Renamed to " + str(name))
        await self.bot.user.edit(nick=name)

    @commands.command()
    async def status(self, ctx):
        await ctx.send(f'{self.bot.user.name}\nHealth : {self.health}\nHunger : {self.hunger}\nHappiness : {self.happiness}\nStatus : {self.currstatus} ')

def setup(bot):
    bot.add_cog(PetCog(bot))