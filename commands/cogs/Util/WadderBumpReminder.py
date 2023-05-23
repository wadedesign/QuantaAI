
import nextcord
import time
import traceback
import json
import os

from nextcord.ext import commands, tasks


class ServerConfig:
    def __init__(self, file_path="data/server_configs.json"):
        self.file_path = file_path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.data = json.load(f)
        else:
            self.save()

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f)

    def get(self, guild_id, key, default=None):
        guild_data = self.data.get(str(guild_id), {})
        return guild_data.get(key, default)

    def set(self, guild_id, key, value):
        guild_id = str(guild_id)
        if guild_id not in self.data:
            self.data[guild_id] = {}
        self.data[guild_id][key] = value
        self.save()

    def remove(self, guild_id, key):
        guild_id = str(guild_id)
        if guild_id in self.data:
            if key in self.data[guild_id]:
                del self.data[guild_id][key]
                self.save()

class BumpReminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.peng = nextcord.AllowedMentions(
            everyone=False,
            roles=True,
            users=True,
            replied_user=False
        )
        self.bump_reminders = {}
        self.server_config = ServerConfig()

    @commands.Cog.listener("on_message")
    async def on_bump_message(self, message):
        if message.author.id != 1097375209666908180 or len(message.embeds) == 0 or not message.guild:
            return
        if "bump done" not in str(message.embeds[0].description).lower():
            return
        g = {"bump_reminders": True}  # replace this with your own logic to get server config
        if not g['bump_reminders']:
            return
        next_bump_time = time.time() + 60 * 60 * 2

        bumper = None
        async for msg in message.channel.history(limit=3):
            if msg.content.lower().startswith("!d bump"):
                bumper = msg.author.id

        self.bump_reminders.update({
            message.guild.id: {
                'channel_id': message.channel.id,
                'time': next_bump_time,
                'bumper': message.author.id if bumper is None else bumper,
                'reward': g['bump_reminders'].get('reward')
            }
        })
        await message.add_reaction("⏱️")

        reward_id = self.bump_reminders[message.guild.id].get('reward')
        if reward_id is None:
            return
        role = message.guild.get_role(reward_id)
        if role is None:
            return
        if bumper is None:
            return
        lemao_bumper = message.guild.get_member(bumper)
        if lemao_bumper is None:
            return

        await lemao_bumper.add_roles(role)
        await message.channel.send(
            f"{lemao_bumper.mention} You have been rewarded the {role.mention} role for **2 hours**.",
            delete_after=5
        )

    @tasks.loop(seconds=30)
    async def bumploop(self):
        await self.client.wait_until_ready()
        try:
            time_now = time.time()
            for guild_id, e in self.bump_reminders.items():
                bump_reminders_enabled = self.server_config.get(guild_id, "bump_reminders", default=True)
                if not bump_reminders_enabled:
                    continue
                if e.get('time') is not None:
                    if round(e['time']) <= round(time_now):
                        try:
                            await self.client.get_channel(e['channel_id']).send(
                                f"<@&{e['role']}>" if e['role'] is not None else f"<@{e['bumper']}>",
                                embed=nextcord.Embed(title="It's Bump Time", description="Please bump using `!d bump`."),
                                allowed_mentions=self.peng
                            )
                        except Exception:
                            pass
                        e.update({"time": None})
                        role_id = e.get("reward")
                        if role_id is not None:
                            channel = self.client.get_channel(e['channel_id'])
                            guild = channel.guild
                            role = guild.get_role(role_id)
                            member = guild.get_member(e.get('bumper'))
                            if role is not None and member is not None:
                                await member.remove_roles(role)
        except Exception:
            traceback.print_exc()


def setup(client):
    client.add_cog(BumpReminder(client))
