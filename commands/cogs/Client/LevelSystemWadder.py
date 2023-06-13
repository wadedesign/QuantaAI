import os
import nextcord
from nextcord.ext import commands
import random
import sqlite3

level = ['NoobMemer', 'MemeRular', 'MemeStar', 'AlphaMemer']
levelnum = [5, 10, 15, 20]

db_path = os.path.join("data", "levelling.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS levelling (user_id INTEGER PRIMARY KEY, username TEXT, server_name TEXT, user_roles TEXT, xp INTEGER, current_xp INTEGER, level INTEGER)''')

def user_level_info(current_xp, lvl):
    if current_xp > lvl * 100:
        current_xp = current_xp - lvl * 100
        lvl += 1
        return current_xp, lvl
    else:
        return current_xp, lvl

def update_user_roles_info(user_id, role):
    c.execute("SELECT user_roles FROM levelling WHERE user_id=?", (user_id,))
    roles_list = c.fetchone()[0].split(',')
    if role not in roles_list:
        roles_list.append(role)
    roles_str = ','.join(roles_list)
    c.execute("UPDATE levelling SET user_roles=? WHERE user_id=?", (roles_str, user_id))
    conn.commit()

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
            c.execute("SELECT * FROM levelling WHERE user_id=?", (message.author.id,))
            stats = c.fetchone()

            if stats is None:
                role_guild = message.author.guild.roles
                roles_list = []
                for role in role_guild:
                    roles_list.append(role.name)
                roles_str = ','.join(roles_list)
                newuser = (message.author.id, message.author.name, message.guild.name, roles_str, 0, 0, 1)
                c.execute("INSERT INTO levelling VALUES (?,?,?,?,?,?,?)", newuser)
                conn.commit()
            else:
                current_xp = stats[5]
                lvl = stats[6]
                xp = stats[4] + 10
                current_xp += 10
                cur_xp, user_level = user_level_info(current_xp, lvl)
                c.execute("UPDATE levelling SET current_xp=?, xp=?, level=? WHERE user_id=?", (cur_xp, xp, user_level, message.author.id))
                conn.commit()
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
        c.execute("SELECT * FROM levelling WHERE user_id=?", (interaction.user.id,))
        stats = c.fetchone()
    
        # If user has no stats, send a message saying so and return
        if stats is None:
            embed = nextcord.Embed(
                title="🤔 Your rank stats", 
                description="You haven't sent any messages, so you have no rank!", 
                color=colour_generator()
            )
            await interaction.channel.send(embed=embed)
            return
    
        # Calculate user's level progress and rank
        total_xp = stats[4]
        current_xp = stats[5]
        lvl = stats[6]
        max_val = (lvl + 1) * 100
        box_ratio = int(max_val / 20)
        green_box = int(current_xp / box_ratio)
        white_box = 20 - green_box
        rank = 1

        # Get the rankings from the database and find the user's rank
        c.execute("SELECT user_id FROM levelling ORDER BY xp DESC")
        rankings = c.fetchall()
        for r in rankings:
            if r[0] == interaction.user.id:
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
        embed.add_field(name="Rank", value=f"{rank}/{len(rankings)}", inline=True)
        embed.add_field(
            name="Progress Bar", 
            value=f"{green_box * ':blue_square:'}{white_box * ':white_large_square:'}", 
            inline=True
        )
        await interaction.channel.send(embed=embed)


    @main.subcommand(name="qleaderboard", description="Check the server's leaderboard")
    async def qleaderboard(self, interaction: nextcord.Interaction):
        c.execute("SELECT * FROM levelling ORDER BY xp DESC")
        rankings = c.fetchall()
        i = 1

        embed = nextcord.Embed(title="🏆 Leaderboard:", color=colour_generator())

        for x in rankings:
            try:
                temp = interaction.guild.get_member(x[0])
                tempxp = x[4]
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