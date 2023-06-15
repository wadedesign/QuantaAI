import os
import nextcord
from nextcord.ext import commands
import random
from pymongo import MongoClient
import urllib.parse

level = ['NoobMemer', 'MemeRular', 'MemeStar', 'AlphaMemer']
levelnum = [5, 10, 15, 20]

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
levelling_collection = db["levelling"]

def user_level_info(current_xp, lvl):
    if current_xp > lvl * 100:
        current_xp = current_xp - lvl * 100
        lvl += 1
        return current_xp, lvl
    else:
        return current_xp, lvl

def update_user_roles_info(user_id, role):
    user = levelling_collection.find_one({"user_id": user_id})
    roles_list = user.get("user_roles", "").split(",")
    if role not in roles_list:
        roles_list.append(role)
    roles_str = ",".join(roles_list)
    levelling_collection.update_one({"user_id": user_id}, {"$set": {"user_roles": roles_str}})

def colour_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return nextcord.Colour.from_rgb(r, g, b)

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("levelsys cog is ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == '--rank':
            return None

        if not message.author.bot:
            user = levelling_collection.find_one({"user_id": message.author.id})
            
            if user is None:
                role_guild = message.author.guild.roles
                roles_list = []
                for role in role_guild:
                    roles_list.append(role.name)
                roles_str = ",".join(roles_list)
                newuser = {
                    "user_id": message.author.id,
                    "username": message.author.name,
                    "server_name": message.guild.name,
                    "user_roles": roles_str,
                    "xp": 0,
                    "current_xp": 0,
                    "level": 1
                }
                levelling_collection.insert_one(newuser)
            else:
                current_xp = user["current_xp"]
                lvl = user["level"]
                xp = user["xp"] + 10
                current_xp += 10
                cur_xp, user_level = user_level_info(current_xp, lvl)
                levelling_collection.update_one(
                    {"user_id": message.author.id},
                    {"$set": {"current_xp": cur_xp, "xp": xp, "level": user_level}}
                )
                if lvl >= user_level:
                    pass
                else:
                    user_dm = await message.author.create_dm()
                    embed = nextcord.Embed(description=f"well done {message.author.mention}! You leveled up to **level: {user_level}**!", colour=colour_generator())
                    await user_dm.send(embed=embed)
                    for i in range(len(level)):
                        if user_level == levelnum[i]:
                            await message.author.add_roles(
                                nextcord.utils.get(message.author.guild.roles, name=level[i]))
                            update_user_roles_info(message.author.id, level[i])
                            embed = nextcord.Embed(description=f"{message.author.mention} you have gotten role **{level[i]}**!!!")
                            embed.set_thumbnail(url=message.author.avatar_url)
                            await user_dm.send(embed=embed)

    @nextcord.slash_command(name="qlevel")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="qrank", description="Check your rank")
    async def qrank(self, interaction: nextcord.Interaction):
        print(f"Checking stats for user ID: {interaction.user.id}")
        
        # Fetch user's stats from the database
        user = levelling_collection.find_one({"user_id": interaction.user.id})
    
        # If user has no stats, send a message saying so and return
        if user is None:
            embed = nextcord.Embed(
                title="🤔 Your rank stats", 
                description="You haven't sent any messages, so you have no rank!", 
                color=colour_generator()
            )
            await interaction.channel.send(embed=embed)
            return
    
        # Calculate user's level progress and rank
        total_xp = user["xp"]
        current_xp = user["current_xp"]
        lvl = user["level"]
        max_val = (lvl + 1) * 100
        box_ratio = int(max_val / 20)
        green_box = int(current_xp / box_ratio)
        white_box = 20 - green_box
        rank = 1

        # Get the rankings from the database and find the user's rank
        rankings = levelling_collection.find().sort("xp", -1)
        for r in rankings:
            if r["user_id"] == interaction.user.id:
                break
            rank += 1

        # Create and send the embed with the user's stats
        embed = nextcord.Embed(
            title="📈 Your rank stats", 
            description=interaction.user.mention, 
            color=colour_generator()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(name="Level", value=lvl, inline=True)
        embed.add_field(name="Total XP", value=f'{total_xp}', inline=True)
        embed.add_field(name="XP Progress", value=f"{current_xp}/{max_val}", inline=True)
        embed.add_field(name="Rank", value=f"{rank}/{rankings.count()}", inline=True)
        embed.add_field(
            name="Progress Bar", 
            value=f"{green_box * ':blue_square:'}{white_box * ':white_large_square:'}", 
            inline=True
        )
        await interaction.channel.send(embed=embed)


    @main.subcommand(name="qleaderboard", description="Check the server's leaderboard")
    async def qleaderboard(self, interaction: nextcord.Interaction):
        rankings = levelling_collection.find().sort("xp", -1).limit(10)
        i = 1

        embed = nextcord.Embed(title="🏆 Leaderboard:", color=colour_generator())

        for x in rankings:
            try:
                temp = interaction.guild.get_member(x["user_id"])
                tempxp = x["xp"]
                embed.add_field(
                    name=f"{i}. {temp.display_name}", 
                    value=f"Total XP: {tempxp}",
                    inline=False
                )
                i += 1
            except:
                pass

            if i == 11:
                break

        embed.set_footer(text="Top 10 users by XP")
        await interaction.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(LevelSys(bot))
