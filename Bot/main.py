from discord.ext import commands
import json
import os
from os import path


client = commands.Bot(command_prefix=["$", "!"])
client.remove_command("help")


def read(file: str):
    return json.load(open(file))


def write(file: str, data: dict):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_json():
    if not path.exists("db"):
        os.mkdir("db")
    if not os.path.exists("db/db.json"):
        bad_words = {"bad_words": ["fuck", "cunt"], "version": 0, "warning_points": {}}
        write("db/db.json", bad_words)


create_json()

db = json.load(open("db/db.json", "r+"))


def version_no(v):
    db["version"] += 0.01
    write("db/db.json", db)
    return db["version"]
