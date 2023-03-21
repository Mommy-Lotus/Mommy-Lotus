import os

import disnake
import git
from disnake import TextChannel
from disnake.ext import commands
from genericpath import isdir, isfile

from config.app_config import config
from config.messages import Messages

bot = commands.Bot(command_prefix=config.default_prefix, intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(Messages.on_ready_bot.format(bot.user, bot.user.id))

    # set status for bot
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    await bot.change_presence(activity=disnake.Game(f"On commit {sha[:7]}"))
    bot_room: TextChannel = bot.get_channel(config.bot_dev_channel)
    if bot_room is not None:
        await bot_room.send(Messages.on_ready_bot.format(bot.user.mention, bot.user.id))

# load all cogs and remove extension from name
for name in os.listdir("./cogs"):
    filename = f"./cogs/{name}"
    modulename = f"cogs.{name}"

    if isfile(filename) and filename.endswith(".py"):
        bot.load_extension(modulename[:-3])

    if isdir(filename) and ("__init__.py" in os.listdir(filename)):
        bot.load_extension(modulename)


bot.run(config.key)
