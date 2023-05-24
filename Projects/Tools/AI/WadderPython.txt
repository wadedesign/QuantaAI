import os

import openai
from langchain.agents.agent_toolkits import create_python_agent
from langchain.llms import OpenAI
from langchain.llms.openai import OpenAI
from langchain.tools.python.tool import PythonREPLTool
from nextcord.ext import commands

serper_api_key = os.getenv("SERPAPI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
scenex_api_key = os.getenv("SCENEX_API_KEY")


class PythonAgent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.agent_executor = create_python_agent(
            llm=OpenAI(temperature=0, max_tokens=1000),
            tool=PythonREPLTool(),
            verbose=True
        )

    @commands.command()
    async def fib(self, ctx, number: int):
        result = self.agent_executor.run(f"What is the {number}th fibonacci number?")
        await ctx.send(result)


def setup(bot):
    bot.add_cog(PythonAgent(bot))
