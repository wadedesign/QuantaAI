import nextcord
import asyncio
from nextcord.ext import commands
from utils.WF2.WadderConfigs import RED_COLOR, EMOJIS
from utils.WF2.WadderEmbeder import error_embed
from typing import Union


async def wait_for_msg(ctx: commands.Context, timeout: int, msg_to_edit: nextcord.Message) -> Union[nextcord.Message, str]:
    def c(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await ctx.bot.wait_for("message", timeout=timeout, check=c)
        try:
            await msg.delete()
        except Exception:
            pass
        if msg.content.lower() == 'cancel':
            ctx.command.reset_cooldown(ctx)
            await msg_to_edit.edit(
                content="",
                embed=nextcord.Embed(
                    title=f"{EMOJIS['tick_no']} Cancelled!",
                    color=RED_COLOR
                )
            )
            return 'pain'
    except asyncio.TimeoutError:
        ctx.command.reset_cooldown(ctx)
        await msg_to_edit.edit(
            content="",
            embed=error_embed(
                f"{EMOJIS['tick_no']} Too late!",
                "You didn't answer in time! Please re-run the command."
            )
        )
        return 'pain'
    return msg
