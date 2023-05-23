import nextcord
from nextcord.ext import commands


# Come back to this later


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_messages = {}

    async def ask_for_input(self, ctx, prompt):
        await ctx.send(prompt)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        response = await self.bot.wait_for("message", check=check)
        return response.content

    @commands.group(name="reactionrole")
    async def reactionrole(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command. Use /reactionrole create to create a new reaction role message.")

    @reactionrole.command(name="create")
    async def create_reaction_role(self, ctx):
        channel_str = await self.ask_for_input(ctx, "Please provide the ID or mention of the channel where the reaction role message will be posted:")
        content = await self.ask_for_input(ctx, "Please provide the content for the reaction role message:")

        try:
            channel = await commands.TextChannelConverter().convert(ctx, channel_str)
        except commands.errors.ChannelNotFound:
            await ctx.send("Invalid channel. Please try again.")
            return

        reaction_roles = {}
        while True:
            emoji_str = await self.ask_for_input(ctx, "Please provide the emoji for the reaction role or type 'done':")
            if emoji_str.lower() == "done":
                break
            try:
                emoji = await commands.PartialEmojiConverter().convert(ctx, emoji_str)
            except commands.errors.PartialEmojiConversionFailure:
                await ctx.send("Invalid emoji. Please try again.")
                continue
                
            role_str = await self.ask_for_input(ctx, "Please provide the role for the reaction role:")
            try:
                role = await commands.RoleConverter().convert(ctx, role_str)
                reaction_roles[emoji] = role
            except commands.errors.RoleNotFound:
                await ctx.send("Invalid role. Please try again.")

        message = await channel.send(content)
        for emoji in reaction_roles:
            await message.add_reaction(emoji)

        self.role_messages[message.id] = reaction_roles

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id not in self.role_messages:
            return

        reaction_roles = self.role_messages[payload.message_id]
        for emoji, role in reaction_roles.items():
            if payload.emoji == emoji:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                await member.add_roles(role)
                break

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id not in self.role_messages:
            return

        reaction_roles = self.role_messages[payload.message_id]
        for emoji, role in reaction_roles.items():
            if payload.emoji == emoji:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                await member.remove_roles(role)
                break

def setup(bot):
    bot.add_cog(ReactionRoles(bot))