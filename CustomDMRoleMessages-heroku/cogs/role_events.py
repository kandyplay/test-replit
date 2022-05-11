from datetime import datetime, timedelta

import config
from utils import db

from disnake import Embed, errors
from disnake.ext import commands


class RoleEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """print loaded message when cog is loaded and ready"""
        print(f"Cog loaded: {self.qualified_name}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        On member update event

        Parameters
        ----------
        before: Member object before update
        after: Member object after update
        """

        guild = before.guild
        member = before

        # Get discord objects from IDs in config
        roles_for_dm = (
            [guild.get_role(int(role_id)) for role_id in config.ROLES_FOR_DM]
            if not config.ROLES_FOR_DM is None
            else None
        )
        roles_for_msg = (
            [guild.get_role(int(role_id)) for role_id in config.ROLE_FOR_CHANNEL_MSG]
            if not config.ROLE_FOR_CHANNEL_MSG is None
            else None
        )
        send_channel_for_roles = (
            guild.get_channel(int(config.SEND_CHANNEL))
            if not config.SEND_CHANNEL is None
            else None
        )
        auto_remove_role = (
            guild.get_role(int(config.AUTO_REMOVE_ROLE))
            if not config.AUTO_REMOVE_ROLE is None
            else None
        )
        auto_remove_role_monitor = (
            [
                guild.get_role(int(role_id))
                for role_id in config.AUTO_REMOVE_ROLE_MONITOR
            ]
            if not config.AUTO_REMOVE_ROLE_MONITOR is None
            else None
        )

        # If new role assigned, get that role, otherwise None
        new_role = list(set(after.roles) - set(before.roles))
        # if a new role
        if new_role:
            new_role = new_role[0]
            # new role in DM roles
            if not new_role in before.roles and new_role in after.roles:
                if new_role in roles_for_dm:
                    # fetch the DM message:
                    dm_message = config.load_dm_msg(str(new_role.id))

                    embed = Embed(
                        title=f"{new_role} was added to your roles!",
                        description=dm_message,
                    )
                    if guild.icon:
                        embed.set_thumbnail(url=guild.icon.url)

                    # try to DM member, fail to target message
                    try:
                        await member.send(embed=embed)
                    except errors.Forbidden:
                        # DM failed, send message to target
                        target = config.get_error_target(guild)
                        if target:
                            await target.send(
                                f"Could not DM {member} due to their privacy settings."
                            )

                # if new role in auto_remove_role_monitor
                if (
                    new_role in auto_remove_role_monitor
                    and auto_remove_role in after.roles
                ):
                    data = db.load_members()
                    members = data["members"]
                    member_id = str(member.id)
                    future = datetime.timestamp(datetime.utcnow() + timedelta(days=7))

                    member_ids = [[k for (k, v) in item.items()] for item in members]
                    if not member_id in member_ids:
                        members.append({member_id: future})

                    db.update_members(data)

                # if new role in role for channel messages
                if new_role in roles_for_msg:
                    
                    message = (
                        config.load_channel_msg()
                        .replace("{member}", member.mention)
                        .replace("{role}", new_role.mention)
                    )
                    if not send_channel_for_roles is None:
                        await send_channel_for_roles.send(message)


def setup(bot):
    bot.add_cog(RoleEvents(bot))
