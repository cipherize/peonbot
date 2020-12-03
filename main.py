#!/usr/bin/env python3

from discord.ext.commands import Bot

from modules import db
from modules.config import config

bot = Bot(command_prefix=config.bot.prefix)


@bot.event
async def on_ready():
    print("INFO: Bot connected as {0.user}.".format(bot))
    print(db.db_test())


for cog in config.bot.cogs.autoload:
    bot.load_extension(f"cogs.{cog}")

print("INFO: Connecting to Discord API...")
bot.run(config.discord.api.token)
