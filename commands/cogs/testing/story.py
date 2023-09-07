import nextcord
from nextcord.ext import commands
import random

class StoryCog(commands.Cog):

    stories = {}
    
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="story", description="Start a collaborative story")
    async def story(self, interaction: nextcord.Interaction):
        pass

    @story.subcommand(name="start", description="Start a new story")
    async def start_story(self, interaction: nextcord.Interaction, title):
        
        story_id = str(random.randint(100000, 999999))
        self.stories[story_id] = {
            "title": title,
            "authors": [],
            "lines": []
        }
        
        embed = nextcord.Embed(title=title)
        msg = await interaction.send(embed=embed)
        self.stories[story_id]["message_id"] = msg.id

        await interaction.respond(f"New story started with id {story_id}")

    @story.subcommand(name="add", description="Add a line to a story")
    async def add_line(self, interaction: nextcord.Interaction, story_id, *, line):
        
        if story_id not in self.stories:
            await interaction.respond("Story not found!")
            return

        story = self.stories[story_id]
        
        if interaction.user in story["authors"]:
            await interaction.respond("You have already added a line to this story!")
            return

        story["authors"].append(interaction.user)
        story["lines"].append(line)

        embed = nextcord.Embed(title=story["title"])
        
        for i, line in enumerate(story["lines"]):
            embed.add_field(name=f"Line {i+1}", value=line, inline=False)

        message = await interaction.channel.fetch_message(story["message_id"])
        await message.edit(embed=embed)

        await interaction.respond("Your line was added to the story!")

    @story.subcommand(name="end", description="End a story") 
    async def end_story(self, interaction: nextcord.Interaction, story_id):
        
        if story_id not in self.stories:
            await interaction.respond("Story not found!")
            return

        story = self.stories.pop(story_id)
        message = await interaction.channel.fetch_message(story["message_id"])
        await message.delete()

        await interaction.respond("The story has ended.")
        
def setup(bot):
    bot.add_cog(StoryCog(bot))