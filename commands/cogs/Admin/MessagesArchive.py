import asyncio
import json
import nextcord
from nextcord.ext import commands
import aiofiles
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"] 
archive_collection = db["message_archives"]

class MessageArchive(commands.Cog):
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

        archive_data = {
            "guild_id": str(channel.guild.id),
            "channel_id": str(channel.id),
            "messages": messages
        }

        await archive_collection.insert_one(archive_data)
        return str(channel.guild.id), str(channel.id)

    @nextcord.slash_command(name="archive", description="📚 Archive messages from a channel.")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="arcmes", description="📚 Archive messages from a channel.")
    @commands.has_permissions(administrator=True)
    async def arc(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        guild_id, channel_id = await self.archive_messages(channel)

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
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉       ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉      ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉     ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉    ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉   ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉  ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ ]```",
            "```yaml\n[▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉]```",
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

        await loading_message.edit(content="Archived Messages", embed=embed)

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
                guild_id, channel_id = await self.archive_messages(channel)

                embed = nextcord.Embed(
                    title="Message Archive",
                    description=f"Archived messages from {channel.mention}",
                    color=nextcord.Color.blue()
                )
                embed.set_footer(text="Created by MessageArchive")

                await loading_message.edit(content="Archiving Server", embed=embed)
            except Exception as e:
                print(f"Error archiving channel {channel}: {e}")


def setup(bot):
    bot.add_cog(MessageArchive(bot))
