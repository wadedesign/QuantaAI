import nextcord
import json
from utils.WF2.WadderUtils import getConfig, updateConfig
from nextcord.ext import commands

# Need to do the on_message event listener for nudity

class AntiNudityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name = 'antinudity')
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def antinudity(self, ctx, antiNudity):

        antiNudity = antiNudity.lower()

        if antiNudity == "true":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiNudity"] = True
            

            embed = nextcord.Embed(title ="antinudity", description ="ANTI_NUDITY_ENABLED_DESCRIPTION", color = 0x2fa737) # Green
        else:
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiNudity"] = False
            

            embed = nextcord.Embed(title ="antinudity", description = "ANTI_NUDITY_DISABLED_DESCRIPTION", color = 0xe00000) # Red
        
        await ctx.channel.send(embed = embed)
        
        updateConfig(ctx.guild.id, data)

 

def setup(bot):
    bot.add_cog(AntiNudityCog(bot))