import json
import os
import nextcord
from nextcord.ext import commands

class ReactionRoles12(nextcord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Check if the reaction roles JSON file exists
        if not os.path.isfile("data/reaction_roles.json"):
            # If the file doesn't exist, create an empty JSON file
            with open("data/reaction_roles.json", "w") as f:
                json.dump({}, f)

        # Load the reaction roles from JSON
        with open("data/reaction_roles.json", "r") as f:
            self.reaction_roles = json.load(f)

    @nextcord.ext.commands.command()
    async def add_reaction_role2(self, ctx, emote, role):
        # Check if the user has permission to add reaction roles
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("You do not have permission to add reaction roles.")
            return

        # Check if the role exists
        role = ctx.guild.get_role(role)
        if role is None:
            await ctx.send("The role you specified does not exist.")
            return

        # Check if the emote exists
        emote = nextcord.utils.get(ctx.guild.emojis, name=emote)
        if emote is None:
            await ctx.send("The emote you specified does not exist.")
            return

        # Add the reaction role
        self.reaction_roles[emote.id] = role.id

        # Save the reaction roles to JSON
        with open("data/reaction_roles.json", "w") as f:
            json.dump(self.reaction_roles, f, indent=4)

        # Send a confirmation message
        await ctx.send(f"The reaction role for {emote.name} has been added.")

    @nextcord.ext.commands.command()
    async def list_reaction_roles2(self, ctx):
        # Check if the user has permission to list reaction roles
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("You do not have permission to list reaction roles.")
            return

        # Send a message with a list of all the reaction roles
        message = ""
        for emote, role_id in self.reaction_roles.items():
            role = ctx.guild.get_role(role_id)
            message += f"{emote.name}: {role.name}\n"
        await ctx.send(message)

    @nextcord.ext.commands.command()
    async def remove_reaction_role2(self, ctx, emote):
        # Check if the user has permission to remove reaction roles
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("You do not have permission to remove reaction roles.")
            return

        # Check if the emote exists
        emote = nextcord.utils.get(ctx.guild.emojis, name=emote)
        if emote is None:
            await ctx.send("The emote you specified does not exist.")
            return

        # Remove the reaction role
        del self.reaction_roles[emote.id]

        # Save the reaction roles to JSON
        with open("data/reaction_roles.json", "w") as f:
            json.dump(self.reaction_roles, f, indent=4)

        # Send a confirmation message
        await ctx.send(f"The reaction role for {emote.name} has been removed.")


def setup(bot):
    bot.add_cog(ReactionRoles12(bot))

