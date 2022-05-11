"""
Configure your bot using the variables below:  If you do not wish to use a specific
variable just set it to `None` (no backticks)
"""

#  can be a member ID, channel ID
ERROR_SEND_TARGET = 961713816406736946

# should be a comma separated list of role IDs you
# wish to monitor for custom DM messages
ROLES_FOR_DM = [
    962795004835807232,
    
]

# should be a comma separated list of role IDs you
# wish to monitor for sending channel messages
ROLE_FOR_CHANNEL_MSG = [
    967855271290486785,
    

]

# the ID for the channel you wish the ROLE_FOR_CHANNEL_MSG to be sent to.
SEND_CHANNEL = 932494503636504617

# the ID for the role you wish to auto remove when one of the
# roles in ROLE_FOR_DM is assigned to the member
AUTO_REMOVE_ROLE = 958788531755556884

# the IDs for the roles you want to check for to start time for AUTO_REMOVE_ROLE
AUTO_REMOVE_ROLE_MONITOR = [
    947256435174154240,
]


"""
message config functions - DO NOT ALTER
"""
from os import path, listdir


def load_dm_msg(role_id):
    path = None
    for file in listdir("./data/dm"):
        if role_id in file and file.endswith(".txt"):
            path = f"./data/dm/{file}"
            with open(path) as f:
                return f.read()


def load_channel_msg():
    with open("./data/channel/message.txt") as f:
        return f.read()


def get_error_target(guild):
    if ERROR_SEND_TARGET:
        member = guild.get_member(int(ERROR_SEND_TARGET))
        if member is None:
            channel = guild.get_channel(int(ERROR_SEND_TARGET))
            return channel

        return member
