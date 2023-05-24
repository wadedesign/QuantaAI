import json
import nextcord
import os
from nextcord.ext import commands
import google.generativeai as genai

class GenerativeAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
        with open("data/googleconfig.json", "r") as f:
            self.google = json.load(f)
            
        genai.configure(api_key=self.google["API_KEY"])
    
    
    @nextcord.slash_command("googlechater")
    async def main(self, interaction: nextcord.Interaction):   
        pass
    
    @commands.command()
    async def chatgoogle(self, ctx, *messages):
        ctx.send("Generating response...")
        
        response = genai.chat(messages=messages)
        
        if response.last:
            await ctx.send(response.last)
        else:
            await ctx.send("An error occurred: No response generated.")
        
    @commands.command()
    async def getmodel(self, ctx, model):
        
        model = genai.get_model(model)
        
        await ctx.send(model)
        
    @commands.command()
    async def listmodels(self, ctx):
        
        for model in genai.list_models():
            await ctx.send(model)
            
            
    @commands.command()
    async def trivia2(self, ctx):
        # Generate a trivia question using the GPT-3.5 Turbo model
        response = genai.chat(messages=[{"role": "system", "content": "You are a trivia bot."},
                                        {"role": "user", "content": "Give me a trivia question."}])

        if response.last:
            await ctx.send(response.last)
        else:
            await ctx.send("An error occurred: No response generated.")

    @commands.command()
    async def answer2(self, ctx, *, user_answer):
        # Check if the user's answer is correct
        if user_answer.lower() == self.current_answer.lower():
            await ctx.send("Correct!")
        else:
            await ctx.send(f"Sorry, the correct answer was {self.current_answer}")
def setup(bot):
    bot.add_cog(GenerativeAI(bot))