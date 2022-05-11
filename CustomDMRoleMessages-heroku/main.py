# Built-in libraries
from datetime import time, datetime
from os import listdir, getenv, path
from json import dump

# Installed libraries
from disnake import Intents
from disnake.ext import commands, tasks

# Local utilities
import config
from utils import db

# Declare Discord permission intents and initialize bot
intents = Intents.default()
intents.members = True
bot = commands.Bot(intents=intents)


@bot.listen()
async def on_ready():
    print(f"{bot.user} is connected to Discord and listening for events.")


@tasks.loop(time=time(0, 0))
async def auto_remove_role():
    """
    Iterate bot guilds and find the auto_remove_role by the ID assigned in config
    Remove that role from any members in data/members.json where datetime timestamp
    has been passed
    """
    await bot.wait_until_ready()
    auto_remove_role_id = int(config.AUTO_REMOVE_ROLE)
    now_timestamp = datetime.timestamp(datetime.utcnow())

    for guild in bot.guilds:
        auto_remove_role = guild.get_role(auto_remove_role_id)

        if auto_remove_role:

            # load the member and timestamp from members.json
            data = db.load_members()
            members = data["members"]

            # iterate members from json
            for index, member in enumerate(members):
                for member_id, timestamp in member.items():

                    # if json timestampe is older than now_timestamp, get member and remove role
                    if timestamp < now_timestamp:
                        guild_member = guild.get_member(int(member_id))
                        if guild_member:
                            if auto_remove_role in guild_member.roles:
                                # remove the role and remove the member_id, timestamp from json
                                await guild_member.remove_roles(auto_remove_role)
                                members.pop(index)

            # update members.json with new data
            db.update_members(data)


def load_cogs(bot):
    """iterate /cogs and load .py as bot extensions"""
    for filename in listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


def check_members_json():
    """If members.json does not exist, create it"""
    if not path.exists("./data/members.json"):
        with open("./data/members.json", "w") as f:
            dump({"members": []}, f)


if __name__ == "__main__":
    check_members_json()
    load_cogs(bot)
    auto_remove_role.start()
    bot.run(getenv("TOKEN"))
