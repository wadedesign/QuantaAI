import asyncio
import os
import random
import re
import string

import nextcord
from nextcord.ext import commands

from utils.WF0.functions import read_file

# ** Remove this file, add to sub commands! **

class MadLibs(commands.Cog):
    """The classic [madlibs game](https://en.wikipedia.org/wiki/Mad_Libs)"""

    def __init__(self, bot):
        self.bot = bot

        # Setup our regex
        self.regex = re.compile(r"\[\[[^\[\]]+\]\]")

    @nextcord.slash_command()
    async def madlibs(self, interaction: nextcord.Interaction):
        """Let's play MadLibs!"""

        # Check if our folder exists
        if not os.path.isdir("Custom/madlibs/"):
            return await interaction.channel.send("I'm not configured for MadLibs yet...")

        # Folder exists - let's see if it has any files
        choices = []
        for file in os.listdir("assets/madlibs/"):
            if file.endswith(".txt"):
                choices.append(file)

        if not choices:
            # No madlibs files
            return await interaction.channel.send("No madlibs files found, ask the owner to add one")

        # We have the file, lets notify the user
        await interaction.send("Okay a madlibs game started, reply with `!stop` to stop")

        # Get a random madlib from those available
        random_madlib = random.choice(choices)

        # Let's load our madlibs file
        data = read_file(f"Custom/madlibs/{random_madlib}")

        # Set up an empty array of words
        words = []

        # Find all the words that need to be added
        matches = re.finditer(self.regex, data)

        # Get all the words from the matched and add them to a list
        for match in matches:
            words.append(match.group(0))

        # Create empty substitution array
        subs = []

        # Iterate words and ask for input
        for i, word in enumerate(words):
            # We define the vowels
            vowels = "aeiou"
            # The [2:-2] is there to remove the first [[ and the last ]] used by our syntax
            word = word[2:-2]

            # If the word starts with a vowel then we use an instead of a
            is_vowel = word[0].lower() in vowels
            await interaction.channel.send(f"I need a{'n' if is_vowel else ''} **{word}** (word *{i + 1}/{len(words)}*).")

            # Setup the check
            def check(msg):
                return msg.author == interaction.user and msg.channel == interaction.channel

            # We wait for a response
            try:
                talk = await self.bot.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                return await interaction.send("You did not respond")

            # Check if the message is to leave
            if talk.content.lower().startswith(("stop madlibs", "!stop", "!cancel")):
                if talk.author is interaction.user:
                    return await interaction.channel.send(f"Alright, *{interaction.user.name}*.  We'll play another time.")

            # We got a relevant message
            word = talk.content

            # Check for capitalization
            if not word.istitle():
                # Make it properly capitalized
                word = string.capwords(word)

            # Add to our list
            subs.append(word)

        # We replace the placeholders with the words picked by our user
        for asub in subs:
            # Only replace the first occurrence
            data = re.sub(self.regex, f"**{asub}**", data, 1)

        # Send the result
        await interaction.channel.send(data)


def setup(bot):
    """Adds the cog to the bot"""
    bot.add_cog(MadLibs(bot))
