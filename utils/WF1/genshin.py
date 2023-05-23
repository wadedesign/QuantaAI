import aiohttp
import nextcord

async def characterlist():
    url = "https://api.genshin.dev/characters"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json(content_type=None)
    return data
    
async def weaponlist():
    url = "https://api.genshin.dev/weapons"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json(content_type=None)
    return data

async def potionlist():
    url = "https://api.genshin.dev/consumables/potions"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json(content_type=None)
    return data

async def nationlist():
    url = "https://api.genshin.dev/nations"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json(content_type=None)
    return data

async def enemylist():
    url = "https://api.genshin.dev/enemies/"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json(content_type=None)
    return data

async def elementlist():
    url = "https://api.genshin.dev/elements"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json(content_type=None)
    return data

# genshin CHARACTER info
def gicinfo(ctx, data, url):
    embed = nextcord.Embed(
        title=f"{data['rarity']} ⭐ {data['name']}",
        colour=nextcord.Color.blue(),
        description=data["description"],
    )

    embed.add_field(name="Vision", value=data["vision"])
    embed.add_field(name="Weapon", value=data["weapon"])
    embed.add_field(name="Nation", value=data["nation"])
    embed.add_field(name="Birthday", value=f"{data['birthday']}"[6:])
    embed.add_field(name="Constellation", value=data["constellation"])

    embed.set_thumbnail(url=f"{url}/icon")
    embed.set_image(url=f"{url}/portrait")
    return embed


# genshin SKILL TALENT character
def gicskill(ctx, data):

    skills = "\n\n".join([f"**{i['name']} | {i['unlock']}**\n{i['description']}" for i in data["skillTalents"]])

    embed = nextcord.Embed(
        title=f"{data['rarity']} ⭐ {data['name']} Skill Talents",
        colour=nextcord.Color.blue(),
        description=skills,
    )
    return embed


# genshin PASSIVE TALENT character
def gicpassive(ctx, data):

    passives = "\n\n".join(
        [
            f"**{i['name']} | {i['unlock']}**\n{i['description']}"
            for i in data["passiveTalents"]
        ]
    )

    embed = nextcord.Embed(
        title=f"{data['rarity']} ⭐ {data['name']} Passive Talents",
        colour=nextcord.Color.blue(),
        description=passives,
    )

    return embed


# genshin Constellations character
def gicconst(ctx, data):

    consts = "\n\n".join(
        [
            f"**{i['name']} | {i['unlock']}**\n{i['description']}\n*Level: {i['level']}*"
            for i in data["constellations"]
        ]
    )

    embed = nextcord.Embed(
        title=f"{data['rarity']} ⭐ {data['name']} Constellations",
        colour=nextcord.Color.blue(),
        description=consts,
    )

    return embed

class GenchinCharacter(nextcord.ui.View):
    def __init__(self, data, ctx):
        self.data = data
        self.ctx = ctx
        super().__init__()

    @nextcord.ui.button(emoji="🌠", label="Skill Talents", style=nextcord.ButtonStyle.blurple)
    async def skill(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=gicskill(self.ctx, self.data), ephemeral=True)

    @nextcord.ui.button(emoji="💫", label="Passive Talents", style=nextcord.ButtonStyle.danger)
    async def passive(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=gicpassive(self.ctx, self.data), ephemeral=True)

    @nextcord.ui.button(emoji="🌌", label="Constellations", style=nextcord.ButtonStyle.blurple)
    async def const(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=gicconst(self.ctx, self.data), ephemeral=True)


# genshin ENEMY info
def gieinfo(ctx, data, url):

    name = data.get("name")
    if not name:
        name = data.get("id")

    desc = data.get("description")
    if not desc:
        des = "No Data"

    embed = nextcord.Embed(title=name, description=desc, colour=nextcord.Color.blue())

    embed.add_field(name="🌎 Region", value=data["region"])
    embed.add_field(name="🌀 Type", value=data["type"])

    element = data.get("elements")
    if not element:
        try:
            element = data["element"]
        except:
            element = "No Data"
    embed.add_field(name="🕵️ Elements", value=", ".join(element))

    embed.add_field(name="🧬 Family", value=data["family"])

    mora = data.get("mora-gained")
    if not mora:
        mora = "No Data"
    embed.add_field(name="<:Mora:888859791689154591> Mora", value=mora)

    embed.set_image(url=f"{url}/portrait.png")
    embed.set_thumbnail(url=f"{url}/icon.png")

    return embed


# genshin ENEMY drops
def giedrops(ctx, data):

    name = data.get("name")
    if not name:
        name = data["id"]

    dropdata = data.get("drops")
    if not dropdata:
        dropdata = "No Data"
    else:
        dropdata = "\n\n".join([f"**{i['rarity']}⭐ {i['name']}**:\n*Minimum Level: {i['minimum-level']}*" for i in data["drops"]])

    embed = nextcord.Embed(title=f"{name} Drops", colour=nextcord.Color.blue(), description=dropdata)
    

    return embed


# genshin ENEMY artifacts
def gieartifacts(ctx, data):

    name = data.get("name")
    if not name:
        name = data["id"]

    artifacts = data.get("artifacts")
    if not artifacts:
        artifacts = "No Data"
    else:
        artifacts = "\n\n".join([f"**{i['rarity']} ⭐ {i['name']}**:\n*Set: {i['set']}*" for i in data["artifacts"]])

    embed = nextcord.Embed(title=f"{name} Artifacts", colour=nextcord.Color.blue(), description=artifacts)
    

    return embed


# genshin ELEMENT description
def gieelement(ctx, data):

    name = data.get("name")
    if not name:
        name = data["id"]

    element = data.get("elemental-descriptions")
    if not element:
        element = "No Data"
    else:
        element = "\n\n".join([f"**{i['element'].title()}:**\n{i['description']}" for i in data["elemental-descriptions"]])

    embed = nextcord.Embed(
        title=f"{name} Elemental Description",
        colour=nextcord.Color.blue(),
        description=element)
    

    return embed


class GenshinEnemy(nextcord.ui.View):
    def __init__(self, data, ctx):
        self.data = data
        self.ctx = ctx
        super().__init__()

    @nextcord.ui.button(emoji="💰", label="Drops", style=nextcord.ButtonStyle.green)
    async def drops(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=giedrops(self.ctx, self.data), ephemeral=True)

    @nextcord.ui.button(emoji="🥇", label="Artifacts", style=nextcord.ButtonStyle.danger)
    async def artifacts(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=gieartifacts(self.ctx, self.data), ephemeral=True)

    @nextcord.ui.button(emoji="🌠", label="Elemental Description", style=nextcord.ButtonStyle.blurple)
    async def elements(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=gieelement(self.ctx, self.data), ephemeral=True)

