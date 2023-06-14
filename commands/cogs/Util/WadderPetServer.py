import json
import os
import random
import threading
import nextcord
from nextcord.ext import commands, tasks
import asyncio


# ** ready for production add embeds

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

    @nextcord.slash_command(name="pet")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(description="Nourish your pet")
    async def nourish(self, interaction: nextcord.Interaction):
        self.hunger += 10
        self.happiness += 2
        if self.hunger >= 100:
            self.hunger = 100
        if self.happiness >= 100:
            self.happiness = 100

        await interaction.response.send_message('Nom nom')
        print("Fed. Current hunger: " + str(self.hunger))

        # Define the animation frames using ASCII art
        animation_frames = [
            "🍗 Feeding your pet...",
            "🍖 Feeding your pet...",
            "🍕 Feeding your pet...",
            "🥩 Feeding your pet...",
            "🌮 Feeding your pet...",
            "🍔 Feeding your pet...",
            "🥪 Feeding your pet...",
            "🥗 Feeding your pet...",
            "🍟 Feeding your pet...",
            "🍝 Feeding your pet..."
        ]

        # Send the animation
        for frame in animation_frames:
            await asyncio.sleep(0.5)  # Adjust the delay between frames if needed
            await interaction.followup.send(frame)


    @main.subcommand(description="snuggle with your pet")
    async def snuggle(self, interaction: nextcord.Interaction):
        self.happiness += 10
        if self.happiness >= 100:
            self.happiness = 100
        await interaction.send(f'Zzzz')
        print("Snuggled. Current happiness: " + str(self.happiness))


    @main.subcommand(description="Snuggle with your pet")
    async def snuggle(self, interaction: nextcord.Interaction):
        self.happiness += 10
        if self.happiness >= 100:
            self.happiness = 100

        await interaction.response.send_message('Zzzz')
        print("Snuggled. Current happiness: " + str(self.happiness))

        # Define the animation frames using ASCII art
        animation_frames = [
            "😴 Snuggling with your pet...",
            "💤 Snuggling with your pet...",
            "😊 Snuggling with your pet...",
            "🥰 Snuggling with your pet...",
            "😻 Snuggling with your pet...",
            "🐾 Snuggling with your pet...",
            "🐱 Snuggling with your pet...",
            "🐶 Snuggling with your pet...",
            "🐰 Snuggling with your pet...",
            "🐦 Snuggling with your pet..."
        ]

        # Send the animation
        for frame in animation_frames:
            await asyncio.sleep(0.5)  # Adjust the delay between frames if needed
            await interaction.followup.send(frame)


    @main.subcommand(description="sleep your pet")
    async def sleep(self, interaction: nextcord.Interaction):
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
            await interaction.send("meow??")

    @main.subcommand(description="wake up your pet")
    async def wakeup(self, interaction: nextcord.Interaction):
        if self.currstatus == "sleeping":
            self.health += 5
            if self.health >= 100:
                self.health = 100
            self.currstatus = "awake"
        else:
            await interaction.send("meow??")


    @main.subcommand(description="rename your pet")
    async def rename(self, interaction: nextcord.Interaction, name):
        print("Renamed to " + str(name))
        await self.bot.user.edit(nick=name)

    @main.subcommand(description="check your pet's status")
    async def status(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Pet Status", color=nextcord.Color.blue())
        embed.add_field(name="Health", value=str(self.health))
        embed.add_field(name="Hunger", value=str(self.hunger))
        embed.add_field(name="Happiness", value=str(self.happiness))
        embed.add_field(name="Status", value=self.currstatus)
        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(PetCog(bot))