from typing import List
from nextcord.ui import View, button
import nextcord

class Paginator(View):
    """Class for the Paginator"""

    def __init__(self, embeds: List[nextcord.Embed], page_name="Page"):
        """Initializes the paginator

        Parameters
        ----------
        embeds : List[nextcord.Embed]
            A list of embeds to paginate from
        page_name : str, optional
            The text to display on the footer of the embed, by default "Page"
        """
        super().__init__()
        self.embeds = embeds
        self.current_page = 0
        self.channel = None
        self.page_name = page_name

    async def send_initial_message(self, ctx, channel):
        """Send the initial message"""
        if not self.embeds:
            raise ValueError("Empty Embeds List")
        if len(self.embeds) == 1:
            await channel.send(embed=self.embeds[0])
            del self
            return
        try:
            self.channel = channel
        except UnboundLocalError:
            pass
        emb = self.embeds[self.current_page].set_footer(
            text=f"{self.page_name} {self.current_page+1}/{len(self.embeds)}"
        )
        self.message = await channel.send(embed=emb, view=self)
        return self.message

    def check_skip(self):
        """Check if it should be skipped"""
        return len(self.embeds) < 2

    @button(label="First")
    async def on_first_page(self, button: nextcord.Button, interaction: nextcord.Interaction):
        """Go to the first page"""
        if self.current_page == 0:
            return
        self.current_page = 0
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page].set_footer(
                text=f"{self.page_name} {self.current_page+1}/{len(self.embeds)}"
            ),
            view=self
        )

    @button(label="Previous")
    async def on_previous_page(self, button: nextcord.Button, interaction: nextcord.Interaction):
        """Go to the previous page"""
        if self.current_page == 0:
            return
        self.current_page -= 1
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page].set_footer(
                text=f"{self.page_name} {self.current_page+1}/{len(self.embeds)}"
            ),
            view=self
        )

    @button(label="Pause")
    async def on_pause(self, button: nextcord.Button, interaction: nextcord.Interaction):
        """Pause the paginator"""
        self.stop()
        await interaction.response.edit_message(view=None)

    @button(label="Next")
    async def on_next_page(self, button: nextcord.Button, interaction: nextcord.Interaction):
        """Go to the next page"""
        if self.current_page == len(self.embeds):
            return
        self.current_page += 1
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page].set_footer(
                text=f"{self.page_name} {self.current_page+1}/{len(self.embeds)}"
            ),
            view=self
        )

    @button(label="Last")
    async def on_last_page(self, button: nextcord.Button, interaction: nextcord.Interaction):
        """Go to the last page"""
        if self.current_page == len(self.embeds) - 1:
            return
        self.current_page = len(self.embeds) - 1
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page].set_footer(
                text=f"{self.page_name} {self.current_page+1}/{len(self.embeds)}"
            ),
            view=self
        )

    @button(label="Custom")
    async def numbered_page(self, button: nextcord.Button, interaction: nextcord.Interaction):
        """Go to a custom page"""
        channel = interaction.channel
        to_delete = []
        to_delete.append(await channel.send(f"{interaction.author.mention}, What {self.page_name} do you want to go to?"))

