from dataclasses import dataclass
from typing import List

import discord
from discord import Client
import discord.ext.commands as commands

from config import config


@dataclass()
class RoleMapping:
    needed: List[discord.Role]
    effect: discord.Role


def has_role(who: discord.Member, what_role: discord.Role):
    """Return true if member has one role."""
    for role in who.roles:
        if role.id == what_role.id:
            return True
    return False


def has_roles(who: discord.Member, what_roles: List[discord.Role]):
    """Return true if member has all roles in list.

    Not optimized but uuuuh
    """
    for what_role in what_roles:
        flag = False
        for role in who.roles:
            if role.id == what_role.id:
                flag = True
        if flag is False:
            return False
    return True


class RoleMapper(commands.Cog):
    """If you have roles [1, 2, 3], you get role x."""

    server: discord.Guild
    combinations: List[RoleMapping]

    def __init__(self, client):
        self._client: Client = client

        self.combinations = []

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        self.server = self._client.get_guild(int(config.data['settings']['server']))
        for role in config.data["mappings"]:
            self.combinations.append(
                RoleMapping(list(map(lambda id: self.server.get_role(int(id)), role["requirements"])),
                            self.server.get_role(role['effect'])))
        for role in self.combinations:
            print(",".join(map(lambda role: role.name, role.needed)), "=>", role.effect.name)

    async def refresh_roles(self, member: discord.Member):
        for role in self.combinations:
            needed = role.needed
            result = role.effect
            if not has_roles(member, needed) and has_role(member, result):
                print("wrongly have {}, removing".format(result))
                await member.remove_roles(result)
            if has_roles(member, needed) and not has_role(member, result):
                print("missing {}, adding".format(result))
                await member.add_roles(result)

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        await self.refresh_roles(after)

    @commands.command("rerun")
    async def rerun_roles(self, ctx: discord.ext.commands.Context):
        """Rerun checks on every user."""
        server: discord.Guild = ctx.guild
        if server is None:
            await ctx.send("Not in a server!")
            return
        for member in server.members:
            print(f"Checking {member.name}")
            await self.refresh_roles(member)
        await ctx.send("Ok done!")


def setup(bot):
    """Load the anarchy extension.
    Args:
        bot (discord.Client) - The discord bot to attach to.
    """
    nsfw_roles: RoleMapper = RoleMapper(bot)
    bot.add_cog(nsfw_roles)
