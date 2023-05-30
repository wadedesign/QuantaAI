import json
import nextcord
from nextcord.ext import commands
import os
from nextcord.ui import Button
import requests

class Developer1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @nextcord.slash_command(name="dev2")
    async def dev2(self, interaction: nextcord.Interaction):
       pass

   

    @dev2.subcommand(name="trivia2", description="Get a random trivia question")
    async def trivia2(self, interaction: nextcord.Interaction):
        try:
            url = "http://jservice.io/api/random"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data:
                question = data[0]["question"]
                category = data[0]["category"]["title"]
                answer = data[0]["answer"]

                embed = nextcord.Embed(title="Trivia Question", color=nextcord.Color.green())
                embed.add_field(name="Category", value=category, inline=False)
                embed.add_field(name="Question", value=question, inline=False)
                embed.add_field(name="Answer", value=answer, inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = nextcord.Embed(title="Trivia Question", color=nextcord.Color.red())
                embed.description = "No trivia question found."

                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the trivia question.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


    @dev2.subcommand(name="fbiwanted", description="Get the FBI's most wanted list")
    async def fbiwanted(self, interaction: nextcord.Interaction):
        try:
            url = "https://api.fbi.gov/wanted/v1/list"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data and "items" in data:
                wanted_list = data["items"]
                embed = nextcord.Embed(title="FBI's Most Wanted", color=nextcord.Color.red())

                for wanted in wanted_list:
                    title = wanted["title"]
                    description = wanted["description"]
                    image_url = wanted["images"][0]["large"]

                    embed.add_field(name=title, value=description, inline=False)
                    embed.set_image(url=image_url)

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = nextcord.Embed(title="FBI's Most Wanted", color=nextcord.Color.red())
                embed.description = "No wanted list found."
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the FBI's most wanted list.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev2.subcommand(name="federalregister", description="Get information about the latest document from the Federal Register")
    async def federalregister(self, interaction: nextcord.Interaction):
        try:
            url = "https://www.federalregister.gov/api/v1/documents?per_page=1&order=newest"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data and "results" in data:
                latest_document = data["results"][0]
                title = latest_document["title"]
                document_number = latest_document["document_number"]
                publication_date = latest_document["publication_date"]
                html_url = latest_document["html_url"]

                embed = nextcord.Embed(title=title, color=nextcord.Color.blue())
                embed.add_field(name="Document Number", value=document_number, inline=True)
                embed.add_field(name="Publication Date", value=publication_date, inline=True)
                embed.add_field(name="More Information", value=f"[Read More]({html_url})", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = nextcord.Embed(title="Federal Register Document", color=nextcord.Color.blue())
                embed.description = "No document found."
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching information from the Federal Register.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev2.subcommand(name="healthcare", description="Get information from the Healthcare.gov API")
    async def healthcare(self, interaction: nextcord.Interaction):
        try:
            url = "https://www.healthcare.gov/api/index.json"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data and "topics" in data:
                topics = data["topics"]
                topic_list = "\n".join(topics)

                embed = nextcord.Embed(title="Healthcare Topics", color=nextcord.Color.blue())
                embed.description = topic_list

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = nextcord.Embed(title="Healthcare Topics", color=nextcord.Color.blue())
                embed.description = "No topics found."
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching information from the Healthcare.gov API.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
def setup(bot):
    bot.add_cog(Developer1(bot))