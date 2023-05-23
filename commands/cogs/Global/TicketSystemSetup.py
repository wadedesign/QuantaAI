
# this is good, but lets give an option to make a transcript of the ticket and close it with a button instead of a command

# would use wadder modmail as a base for this

import nextcord
from nextcord.ext import commands

class TicketSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_ticket_category(self, guild):
        category_name = "Support Tickets"
        existing_categories = [c.name for c in guild.categories]
        if category_name not in existing_categories:
            return await guild.create_category(category_name)
        else:
            return nextcord.utils.get(guild.categories, name=category_name)

    async def create_support_channel(self, guild):
        support_channel_name = "support-channel"
        existing_channels = [c.name for c in guild.channels]
        if support_channel_name not in existing_channels:
            category = await self.create_ticket_category(guild)
            return await category.create_text_channel(support_channel_name)
        else:
            return nextcord.utils.get(guild.channels, name=support_channel_name)

    async def create_ticket(self, interaction):
        user = interaction.user
        guild = interaction.guild
        category = await self.create_ticket_category(guild)
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ticket_channel = await category.create_text_channel(f"ticket-{user.display_name.lower()}", overwrites=overwrites)
        admin_role = nextcord.utils.get(guild.roles, name="Admin")
        if admin_role:
            await ticket_channel.set_permissions(admin_role, read_messages=True, send_messages=True)

        await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)
        await ticket_channel.send(f"{user.mention}, your ticket has been created. An admin will be with you shortly.\n\n{admin_role.mention} a new ticket has been created by {user.mention}.")

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)
    async def setupticketsystem(self, interaction: nextcord.Interaction):
        support_channel = await self.create_support_channel(interaction.guild)
        embed = nextcord.Embed(title="Support Ticket", description="Click the button below to open a support ticket.")
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Open Ticket", custom_id="open_ticket")
        view = nextcord.ui.View()
        view.add_item(button)
        await support_channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        if interaction.type == nextcord.InteractionType.component:
            if interaction.data["custom_id"] == "open_ticket":
                await self.create_ticket(interaction)

def setup(bot):
    bot.add_cog(TicketSystemCog(bot))