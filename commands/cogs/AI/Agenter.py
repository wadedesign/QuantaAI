import re
import nextcord
from nextcord.ext import commands
import os

import openai
#* LangChain Imports
from langchain.agents import initialize_agent, load_tools

from langchain.llms import OpenAI
from langchain.llms.openai import OpenAI

# ** API KEYS
serper_api_key = os.getenv("SERPAPI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
scenex_api_key = os.getenv("SCENEX_API_KEY")

class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.llm = OpenAI(temperature=0, openai_api_key=openai.api_key)
        self.toolkit = load_tools(["serpapi"], llm=self.llm, serpapi_api_key=serpapi_api_key)
        self.agent = initialize_agent(self.toolkit, self.llm, agent="zero-shot-react-description", verbose=True, return_intermediate_steps=True)

    @commands.command(name='3search')
    async def search(self, ctx, *, query: str):
        response = self.agent({"input": query})
        response_text = response.get("intermediate_steps")[-1][-1]  # Get the last part of the response

        # Use regular expressions to find the final answer
        match = re.search(r'Final Answer: (.+)', response_text)
        if match:
            answer = match.group(1)
        else:
            answer = "Sorry, I couldn't find an answer."

        # Format the entire response as a single message
        formatted_response = '\n'.join([f"{step[1]}\n{step[0][2]}" for step in response["intermediate_steps"]])

        # Create an embed and add the fields
        embed = nextcord.Embed(title="Search Result", color=0x00bfff)
        embed.add_field(name="Query", value=query, inline=False)
        embed.add_field(name="Response", value=formatted_response, inline=False)
        embed.add_field(name="Final Answer", value=answer, inline=False)

        print(f"Answer: {answer}")  # Add this line to print the answer to the console
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SearchCog(bot))
