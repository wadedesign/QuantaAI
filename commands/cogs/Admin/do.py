import datetime
import os
import nextcord
from nextcord.ext import commands
from loguru import logger
import openai

openai_model_engine = "text-davinci-003"  # You can change this to another OpenAI model engine if you'd like

openai.api_key = "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"


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.log_message(message)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.log_edit(before, after)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_delete(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log_member_join(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_member_remove(member)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.log_member_update(before, after)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.log_member_ban(guild, user)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await self.log_member_unban(guild, user)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.log_role_create(role)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.log_role_delete(role)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        await self.log_role_update(before, after)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await self.log_channel_create(channel)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.log_channel_delete(channel)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        await self.log_channel_update(before, after)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        await self.log_emoji_update(guild, before, after)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        await self.log_guild_update(before, after)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        await self.log_voice_state_update(member, before, after)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.log_invite_create(invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.log_invite_delete(invite)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.log_reaction_add(reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.log_reaction_remove(reaction, user)

    @commands.Cog.listener()
    async def on_integration_update(self, guild):
        await self.log_integration_update(guild)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        await self.log_user_update(before, after)

    @commands.Cog.listener()
    async def on_stage_instance_create(self, stage_instance):
        await self.log_stage_instance_create(stage_instance)

    @commands.Cog.listener()
    async def on_stage_instance_delete(self, stage_instance):
        await self.log_stage_instance_delete(stage_instance)

    @commands.Cog.listener()
    async def on_stage_instance_update(self, before, after):
        await self.log_stage_instance_update(before, after)

    @commands.Cog.listener()
    async def on_sticker_create(self, sticker):
        await self.log_sticker_create(sticker)

    @commands.Cog.listener()
    async def on_sticker_delete(self, sticker):
        await self.log_sticker_delete(sticker)

    @commands.Cog.listener()
    async def on_sticker_update(self, before, after):
        await self.log_sticker_update(before, after)

    @commands.Cog.listener()
    async def on_webhook_update(self, channel):
        await self.log_webhook_update(channel)

    async def setup_logger(self, interaction: nextcord.Interaction):
        existing_channel = nextcord.utils.get(interaction.guild.text_channels, name="📝・qlogger")
        if existing_channel:
            await interaction.response.send_message("Logger channel already exists!", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
            }
            channel = await interaction.guild.create_text_channel("logger", overwrites=overwrites)
            await interaction.response.send_message(f"Logger channel created: {channel.mention}", ephemeral=True)

    async def log_embed(self, logger_channel, title, description, color=nextcord.Color.blue(), timestamp=None):
        embed = nextcord.Embed(title=title, description=description, color=color)
        if timestamp:
            embed.timestamp = timestamp
        await logger_channel.send(embed=embed)

    async def detect_language(self, text: str) -> str:
        completions = openai.Completion.create(
            engine=openai_model_engine,
            prompt=f"Detect the language of the following text and provide the name in lowercase:\n\n{text}\n\nLanguage:",
            max_tokens=16,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return completions.choices[0].text.strip()

    async def translate_text(self, source_language: str, target_language: str, text: str) -> str:
        completions = openai.Completion.create(
            engine=openai_model_engine,
            prompt=f"Translate from {source_language} to {target_language}: {text}",
            max_tokens=64,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return completions.choices[0].text.strip()

    async def log_message(self, message):
        print(f"Message content at the beginning: {message.content}")
        is_private = message.guild is None

        # Check if the message was sent by a bot
        if message.author.bot:
            return
        print(f"Message content after checking for bot: {message.content}")

        # Log the message to the logger channel
        logger_channel = nextcord.utils.get(message.guild.text_channels, name="logger")
        print(f"Logger channel: {logger_channel}")

        if not is_private:
            if logger_channel:
                channel_name = message.channel.mention
                await self.log_embed(
                    logger_channel, "Message Sent", f"{message.author.mention} said in {channel_name}: {message.content}"
                )
            else:
                print("Logger channel not found.")

            try:
                with open("log/messages.txt", "a", encoding="utf-8") as file:
                    log_entry = f"{message.guild.name} - {message.channel.name} - {message.author.name}#{message.author.discriminator}: {message.content}\n"
                    file.write(log_entry)
                    print("Log entry written to file.")
            except Exception as e:
                print(f"Error writing to log file: {e}")

        # Call the OpenAI API to analyze the message content
        response = openai.Moderation.create(input=message.content)
        print("OpenAI API called.")

        # Check if the API flagged the message as inappropriate
        if response["results"][0]["flagged"]:
            print("Message flagged as inappropriate.")

            # Delete the flagged message
            await message.delete()
            print("Flagged message deleted.")

            # Warn the user
            warning_message = (
                f"{message.author.mention}, your message has been deleted because it was flagged as inappropriate. Please review our community guidelines and ensure your future messages comply with them."
            )
            await message.channel.send(warning_message)
            print("User warned about the flagged message.")

            # Log the flagged message to the logger channel
            if logger_channel:
                await self.log_embed(logger_channel, "Flagged Message", f"{message.author.mention} said: {message.content}")
            else:
                print("Logger channel not found.")

            # Log the categories and category scores associated with the flagged message
            categories = response["results"][0]["categories"]
            category_scores = response["results"][0]["category_scores"]
            category_list = []
            for category, score in category_scores.items():
                if score > 0.987:
                    category_list.append(f"{category} ({score:.2f})")
            if category_list:
                category_string = ", ".join(category_list)
                if logger_channel:
                    await self.log_embed(logger_channel, "Flagged Message Details", f"Flagged message: {message.content}\nCategories: {category_string}")
                else:
                    print("Logger channel not found.")

    async def log_edit(self, before, after):
        if before.author.bot:
            return

        logger_channel = nextcord.utils.get(before.guild.text_channels, name="logger")
        if logger_channel and before.content != after.content:
            await self.log_embed(
                logger_channel,
                "Message Edited",
                f"{before.author.mention} edited their message:\n\n**Before:** {before.content}\n**After:** {after.content}",
            )

    async def log_delete(message):
        if message.author.bot:
            return

        logger_channel = nextcord.utils.get(message.guild.text_channels, name="logger")
        if logger_channel:
            embed = nextcord.Embed(title="Message Deleted", color=0xFF0000)
            embed.add_field(name="Author", value=message.author.mention, inline=False)
            embed.add_field(name="Content", value=message.content, inline=False)
            embed.set_footer(text="Deleted message")
            await logger_channel.send(embed=embed)

    async def log_member_join(self, member):
        # Log the event
        logger.info(f"{member} joined the server.")
        logger_channel = nextcord.utils.get(member.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Member Joined",
                f"{member.mention} joined the server.",
                color=nextcord.Color.green(),
                timestamp=datetime.datetime.utcnow(),
            )

        # Send a welcome message to the member
        welcome_message = (
            f"Welcome to the server, {member.mention}!\n\nWe are glad to have you join our community. Please make yourself at home and feel free to explore our server. If you have any questions, don't hesitate to ask our friendly staff or fellow members. \n\nAlso, don't forget to introduce yourself in the #introductions channel so we can get to know you better. Have fun!"
        )
        embed = nextcord.Embed(title="Welcome to our server!", description=welcome_message, color=nextcord.Color.blurple())
        avatar_url = member.avatar.url if member.avatar else member.default_avatar_url
        embed.set_thumbnail(url=avatar_url)
        await member.send(embed=embed)

    async def log_member_remove(self, member):
        logger_channel = nextcord.utils.get(member.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Member Left",
                f"{member.mention} left the server.",
                color=nextcord.Color.red(),
                timestamp=datetime.datetime.utcnow(),
            )

    async def log_member_update(self, before, after):
        logger_channel = nextcord.utils.get(before.guild.text_channels, name="logger")
        if logger_channel:
            if before.nick != after.nick:
                await self.log_embed(
                    logger_channel,
                    "Nickname Changed",
                    f"{after.mention} changed their nickname:\n\n**Before:** {before.nick}\n**After:** {after.nick}",
                )

            before_roles = set(before.roles)
            after_roles = set(after.roles)
            added_roles = after_roles - before_roles
            removed_roles = before_roles - after_roles

            for role in added_roles:
                await self.log_embed(
                    logger_channel,
                    "Role Added",
                    f"{after.mention} was given the {role.mention} role.",
                    color=nextcord.Color.green(),
                )

            for role in removed_roles:
                await self.log_embed(
                    logger_channel,
                    "Role Removed",
                    f"{after.mention} lost the {role.mention} role.",
                    color=nextcord.Color.red(),
                )

    async def log_member_ban(self, guild, user):
        logger_channel = nextcord.utils.get(guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel, "Member Banned", f"{user.mention} was banned from the server.", color=nextcord.Color.red()
            )

    async def log_member_unban(self, guild, user):
        logger_channel = nextcord.utils.get(guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Member Unbanned",
                f"{user.mention} was unbanned from the server.",
                color=nextcord.Color.green(),
            )

    async def log_role_create(self, role):
        logger_channel = nextcord.utils.get(role.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel, "Role Created", f"Role {role.mention} was created.", color=nextcord.Color.green()
            )

    async def log_role_delete(self, role):
        logger_channel = nextcord.utils.get(role.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel, "Role Deleted", f"Role {role.name} was deleted.", color=nextcord.Color.red()
            )

    async def log_role_update(self, before, after):
        logger_channel = nextcord.utils.get(before.guild.text_channels, name="logger")
        if logger_channel:
            if before.name != after.name:
                await self.log_embed(
                    logger_channel,
                    "Role Renamed",
                    f"Role **{before.name}** was renamed to **{after.name}**",
                )

    async def log_channel_create(self, channel):
        logger_channel = nextcord.utils.get(channel.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Channel Created",
                f"Channel {channel.mention} was created.",
                color=nextcord.Color.green(),
            )

    async def log_channel_delete(self, channel):
        logger_channel = nextcord.utils.get(channel.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Channel Deleted",
                f"Channel **{channel.name}** was deleted.",
                color=nextcord.Color.red(),
            )

    async def log_channel_update(self, before, after):
        logger_channel = nextcord.utils.get(before.guild.text_channels, name="logger")
        if logger_channel:
            if before.name != after.name:
                await self.log_embed(
                    logger_channel,
                    "Channel Renamed",
                    f"Channel **{before.name}** was renamed to **{after.name}**",
                )

    async def log_emoji_update(self, guild, before, after):
        logger_channel = nextcord.utils.get(guild.text_channels, name="logger")
        if logger_channel:
            added_emojis = set(after) - set(before)
            removed_emojis = set(before) - set(after)

            for emoji in added_emojis:
                await self.log_embed(
                    logger_channel,
                    "Emoji Added",
                    f"Emoji {emoji} was added to the server.",
                    color=nextcord.Color.green(),
                )

            for emoji in removed_emojis:
                await self.log_embed(
                    logger_channel,
                    "Emoji Removed",
                    f"Emoji {emoji} was removed from the server.",
                    color=nextcord.Color.red(),
                )

    async def log_guild_update(self, before, after):
        logger_channel = nextcord.utils.get(before.text_channels, name="logger")
        if logger_channel:
            if before.name != after.name:
                await self.log_embed(
                    logger_channel,
                    "Server Name Changed",
                    f"Server name was changed from **{before.name}** to **{after.name}**",
                )

            if before.region != after.region:
                await self.log_embed(
                    logger_channel,
                    "Server Region Changed",
                    f"Server region was changed from **{before.region}** to **{after.region}**",
                )

            if before.icon != after.icon:
                embed = nextcord.Embed(title="Server Icon Changed", color=nextcord.Color.blue())
                embed.set_thumbnail(url=after.icon_url)
                await logger_channel.send(embed=embed)

            if before.owner != after.owner:
                await self.log_embed(
                    logger_channel,
                    "Server Owner Changed",
                    f"Server ownership was transferred from {before.owner.mention} to {after.owner.mention}",
                )

    async def log_voice_state_update(self, member, before, after):
        logger_channel = nextcord.utils.get(member.guild.text_channels, name="logger")
        if logger_channel:
            if before.channel != after.channel:
                if before.channel is None:
                    await self.log_embed(
                        logger_channel,
                        "Voice Channel Joined",
                        f"{member.mention} joined voice channel {after.channel.name}.",
                        color=nextcord.Color.green(),
                    )
                elif after.channel is None:
                    await self.log_embed(
                        logger_channel,
                        "Voice Channel Left",
                        f"{member.mention} left voice channel {before.channel.name}.",
                        color=nextcord.Color.red(),
                    )
                elif after.channel.guild is not None:
                    await self.log_embed(
                        logger_channel,
                        "Voice Channel Moved",
                        f"{member.mention} moved from voice channel {before.channel.name} to {after.channel.name}.",
                    )

            if before.self_mute != after.self_mute:
                state = "muted" if after.self_mute else "unmuted"
                await self.log_embed(
                    logger_channel,
                    "Voice State Updated",
                    f"{member.mention} {state} themselves in voice channel {after.channel.name}.",
                )

            if before.self_deaf != after.self_deaf:
                state = "deafened" if after.self_deaf else "undeafened"
                await self.log_embed(
                    logger_channel,
                    "Voice State Updated",
                    f"{member.mention} {state} themselves in voice channel {after.channel.name}.",
                )

    async def log_invite_create(self, invite):
        logger_channel = nextcord.utils.get(invite.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Invite Created",
                f"Invite {invite.code} was created by {invite.inviter.mention} for channel {invite.channel.mention}.",
                color=nextcord.Color.green(),
            )

    async def log_invite_delete(self, invite):
        logger_channel = nextcord.utils.get(invite.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Invite Deleted",
                f"Invite {invite.code} was deleted for channel {invite.channel.mention}.",
                color=nextcord.Color.red(),
            )

    async def log_reaction_add(self, reaction, user):
        logger_channel = nextcord.utils.get(reaction.message.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Reaction Added",
                f"{user.mention} added {reaction.emoji} reaction to a message in {reaction.message.channel.mention}.",
            )

    async def log_reaction_remove(self, reaction, user):
        logger_channel = nextcord.utils.get(reaction.message.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Reaction Removed",
                f"{user.mention} removed {reaction.emoji} reaction from a message in {reaction.message.channel.mention}.",
            )

    async def log_integration_update(self, guild):
        logger_channel = nextcord.utils.get(guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(logger_channel, "Integration Updated", "An integration was updated on the server.")

    async def log_user_update(self, bot, before, after):
        if before.avatar != after.avatar or before.name != after.name or before.discriminator != after.discriminator:
            for guild in bot.guilds:
                logger_channel = nextcord.utils.get(guild.text_channels, name="logger")
                if logger_channel:
                    await self.log_embed(
                        logger_channel,
                        "User Updated",
                        f"{before.mention} updated their profile. (avatar, username, or discriminator)",
                    )

    async def log_stage_instance_create(self, stage_instance):
        logger_channel = nextcord.utils.get(stage_instance.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Stage Instance Created",
                f"Stage instance **{stage_instance.topic}** was created.",
            )

    async def log_stage_instance_delete(self, stage_instance):
        logger_channel = nextcord.utils.get(stage_instance.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel,
                "Stage Instance Deleted",
                f"Stage instance **{stage_instance.topic}** was deleted.",
            )

    async def log_stage_instance_update(self, before, after):
        logger_channel = nextcord.utils.get(before.guild.text_channels, name="logger")
        if logger_channel:
            if before.topic != after.topic:
                await self.log_embed(
                    logger_channel,
                    "Stage Instance Updated",
                    f"Stage instance topic was changed from **{before.topic}** to **{after.topic}**",
                )

    async def log_sticker_create(self, sticker):
        logger_channel = nextcord.utils.get(sticker.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel, "Sticker Created", f"Sticker **{sticker.name}** was created."
            )

    async def log_sticker_delete(self, sticker):
        logger_channel = nextcord.utils.get(sticker.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(
                logger_channel, "Sticker Deleted", f"Sticker **{sticker.name}** was deleted."
            )

    async def log_sticker_update(self, before, after):
        logger_channel = nextcord.utils.get(before.guild.text_channels, name="logger")
        if logger_channel:
            if before.name != after.name:
                await self.log_embed(
                    logger_channel,
                    "Sticker Updated",
                    f"Sticker **{before.name}** was updated to **{after.name}**",
                )

    async def log_webhook_update(self, channel):
        logger_channel = nextcord.utils.get(channel.guild.text_channels, name="logger")
        if logger_channel:
            await self.log_embed(logger_channel, "Webhook Updated", f"A webhook was updated in channel {channel.mention}.")

def setup(bot):
    bot.add_cog(Logger(bot))