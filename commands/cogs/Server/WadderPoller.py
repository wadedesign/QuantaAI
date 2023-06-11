import nextcord
from nextcord.ext import commands
from collections import defaultdict

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = {}
        self.vote_emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']

    async def update_poll(self, poll_id):
        poll = self.polls[poll_id]

        embed = nextcord.Embed(title=poll["question"], description="React with the corresponding emoji to vote.")
        for idx, choice in enumerate(poll["choices"]):
            embed.add_field(name=f"{self.vote_emojis[idx]} {choice}", value=f"{poll['votes'][idx]} votes", inline=False)

        await poll["message"].edit(embed=embed)

    @nextcord.slash_command(name="cpoll", description="Create a poll with up to 10 choices.")
    async def cpoll(self, interaction: nextcord.Interaction, question: str, choices: str):
        choices = choices.split(",")
        if len(choices) > len(self.vote_emojis):
            await interaction.send("You can have a maximum of 10 choices.")
            return

        embed = nextcord.Embed(title=question, description="React with the corresponding emoji to vote.")
        for idx, choice in enumerate(choices):
            embed.add_field(name=f"{self.vote_emojis[idx]} {choice}", value="0 votes", inline=False)

        poll_message = await interaction.send(embed=embed)

        for idx in range(len(choices)):
            await poll_message.add_reaction(self.vote_emojis[idx])

        self.polls[poll_message.id] = {
            "question": question,
            "choices": choices,
            "votes": defaultdict(int),
            "message": poll_message
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or reaction.message.id not in self.polls:
            return

        poll = self.polls[reaction.message.id]
        if reaction.emoji in self.vote_emojis:
            idx = self.vote_emojis.index(reaction.emoji)
            poll["votes"][idx] += 1
            await self.update_poll(reaction.message.id)
            await reaction.remove(user)

def setup(bot):
    bot.add_cog(Poll(bot))
