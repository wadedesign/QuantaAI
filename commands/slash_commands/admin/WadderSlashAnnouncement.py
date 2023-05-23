import nextcord
import os

def setup(bot):
    @bot.slash_command(description="Send a customized announcement with an optional image.")
    async def announce(
        interaction: nextcord.Interaction,
        title: str,
        message: str,
        channel: nextcord.TextChannel,
        mention: bool = False,
        image_name: str = None
    ):
        """
        Send a customized announcement in the specified channel.

        Args:
        - title (str): The title of the announcement.
        - message (str): The message to be included in the announcement.
        - channel (nextcord.TextChannel): The channel to send the announcement in.
        - mention (bool): Whether or not to mention the @everyone role in the announcement. Defaults to False.
        - image_name (str): The name of the image file in the 'images' folder to be included in the announcement. Defaults to None.
        """
        # Create the announcement embed
        embed = nextcord.Embed(
            title=title,
            description=message,
            color=0x1abc9c
        )

        # Add image if provided
        if image_name:
            image_path = os.path.join("images", image_name)
            if os.path.isfile(image_path):
                with open(image_path, "rb") as image_file:
                    image = nextcord.File(image_file, filename="test.png")
                    embed.set_image(url="attachment://test.png")
            else:
                image = None
        else:
            image = None
        
        # Add footer with command issuer's name and profile picture
        embed.set_footer(text=f"Announcement by {interaction.user}", icon_url=interaction.user.avatar.url)

        # Mention @everyone if requested
        content = "@everyone" if mention else None
        
        # Send the announcement message
        await channel.send(content=content, files=[image] if image else None, embed=embed)
        
        # Send a response to the user
        await interaction.response.send_message(f"Announcement sent in {channel.mention}!")
