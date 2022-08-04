import json
import logging
import sys
from config import config

import discord
from discord.ext import commands

from discord.ext.commands import Bot


async def send_cmd_help(ctx):
    cmd = ctx.command
    em = discord.Embed(title=f'Usage: {ctx.prefix + cmd.name + " " + cmd.signature}', color=discord.Color.green())
    em.description = cmd.help
    return em


async def on_command_error(ctx, error):
    send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments,
                 commands.UserInputError)

    if isinstance(error, commands.CommandNotFound):  # fails silently
        pass

    elif isinstance(error, send_help):
        _help = await send_cmd_help(ctx)
        await ctx.send(embed=_help)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    config.load()

    intents = discord.Intents.default()
    intents.members = True
    client = Bot(config.data['settings']['prefix'], intents=intents)

    client.add_listener(on_command_error, "on_command_error")

    client.load_extension("role_mapper")
    client.run(config.data['settings']["token"])


if __name__ == "__main__":
    main()
