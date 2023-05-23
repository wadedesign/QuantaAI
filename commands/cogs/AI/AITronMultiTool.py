
from nextcord.ext import commands

from langchain.schema import AgentAction, AgentFinish


import openai
import os

serper_api_key = os.getenv("SERPAPI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
scenex_api_key = os.getenv("SCENEX_API_KEY")
# I assume your SerpAPIWrapper and OpenAI are asynchronous, thus use aiohttp or httpx for HTTP requests.
class CustomAgent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.agent_executor = None  # Will be initialized in on_ready event

    @commands.Cog.listener()
    async def on_ready(self):
        from langchain.agents import Tool, AgentExecutor, BaseMultiActionAgent
        from langchain import OpenAI, SerpAPIWrapper

        def random_word(query: str) -> str:
            print("\nNow I'm doing this!")
            return "foo"

        search = SerpAPIWrapper()
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="useful for when you need to answer questions about current events"
            ),
            Tool(
                name="RandomWord",
                func=random_word,
                description="call this to get a random word."
            )
        ]

        class FakeAgent(BaseMultiActionAgent):
            """Fake Custom Agent."""
    
            @property
            def input_keys(self):
                return ["input"]
    
            async def aplan(self, intermediate_steps, **kwargs):
                """Given input, decided what to do."""
                if len(intermediate_steps) == 0:
                    return [
                        AgentAction(tool="Search", tool_input=kwargs["input"], log=""),
                        AgentAction(tool="RandomWord", tool_input=kwargs["input"], log=""),
                    ]
                else:
                    return AgentFinish(return_values={"output": "bar"}, log="")
        
        agent = FakeAgent()
        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    @commands.command()
    async def querytxt(self, ctx, *, user_input: str):
        """Queries the custom agent."""
        if self.agent_executor is None:
            await ctx.send("Agent is not ready yet!")
            return

        result = await self.agent_executor.run(user_input)
        await ctx.send(result)

def setup(bot):
    bot.add_cog(CustomAgent(bot))
