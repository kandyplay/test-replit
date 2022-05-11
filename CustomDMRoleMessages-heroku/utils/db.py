from json import load, dump


def load_members():
    with open("./data/members.json") as f:
        return load(f)


def update_members(data):
    with open("./data/members.json", "w") as f:
        dump(data, f, indent=4)
