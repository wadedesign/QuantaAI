import asyncio
import json
import nextcord
from nextcord.ext import commands
import aiofiles

class MessageArchive(commands.Cog): #** RFP **#
    def __init__(self, bot):
        self.bot = bot

    async def archive_messages(self, channel):
        messages = []
        async for message in channel.history(limit=100):  # Adjust the message limit if needed
            messages.append({
                "content": message.content,
                "author": str(message.author),
                "timestamp": message.created_at.isoformat()
            })

        async with aiofiles.open(f"{channel.guild.id}_{channel.id}_archive.json", "w") as archive_file:
            await archive_file.write(json.dumps(messages, indent=2))
        
        return f"{channel.guild.id}_{channel.id}_archive.json"

    @nextcord.slash_command(name="archive", description="📚 Archive messages from a channel.")
    async def main(self, interaction: nextcord.Interaction):
        pass
    
    @main.subcommand(name="arcmes", description="📚 Archive messages from a channel.")
    @commands.has_permissions(administrator=True)
    async def arc(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        archive_filename = await self.archive_messages(channel)
        
        # Define the computer animation frames
        animation = [
            "```yaml\n[                    ]```",
            "```yaml\n[▉                   ]```",
            "```yaml\n[▉▉                  ]```",
            "```yaml\n[▉▉▉                 ]```",
            "```yaml\n[▉▉▉▉                ]```",
            "```yaml\n[▉▉▉▉▉               ]```",
            "```yaml\n[▉▉▉▉▉▉              ]```",
            "```yaml\n[▉▉▉▉▉▉▉             ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉            ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉           ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉          ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉         ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉        ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉       ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉      ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉     ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉    ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉   ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉  ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉]```",
            "```yaml\n[Archiving messages... ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        embed = nextcord.Embed(
            title="Message Archive",
            description=f"Archived messages from {channel.mention}",
            color=nextcord.Color.blue()
        )
        embed.set_footer(text="Created by MessageArchive")
        
        file = nextcord.File(archive_filename, filename=f"{channel.name}_archive.json")
        
        await loading_message.edit(content="Archived Messages", embed=embed, file=file)


    @main.subcommand(name="arcserver", description="📚 Archive Server")
    @commands.has_permissions(administrator=True)
    async def archive_server(self, interaction: nextcord.Interaction):
        # Define the computer animation frames
        animation = [
            "```yaml\n[                     ]```",
            "```yaml\n[▉                    ]```",
            "```yaml\n[▉▉                   ]```",
            "```yaml\n[▉▉▉                  ]```",
            "```yaml\n[▉▉▉▉                 ]```",
            "```yaml\n[▉▉▉▉▉                ]```",
            "```yaml\n[▉▉▉▉▉▉               ]```",
            "```yaml\n[▉▉▉▉▉▉▉              ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉             ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉            ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉           ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉          ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉         ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉        ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉       ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉      ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉     ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉    ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉   ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉  ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉]```",
            "```yaml\n[Archiving server...  ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        for channel in interaction.guild.text_channels:
            try:
                archive_filename = await self.archive_messages(channel)
                
                embed = nextcord.Embed(
                    title="Message Archive",
                    description=f"Archived messages from {channel.mention}",
                    color=nextcord.Color.blue()
                )
                embed.set_footer(text="Created by MessageArchive")
                
                file = nextcord.File(archive_filename, filename=f"{channel.name}_archive.json")
                
                await loading_message.edit(content="Archiving Server", embed=embed, file=file)
                
            except Exception as e:
                print(f"Error archiving channel {channel}: {e}")


def setup(bot):
    bot.add_cog(MessageArchive(bot))
