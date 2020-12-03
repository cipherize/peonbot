import random
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        phrase_list = [
            "Ready to work.",
            "Yes?",
            "Hmmm?",
            "What you want?",
            "Something need doing?",
            "Whaaat?",
            "Me busy. Leave me alone!",
            "No time for play.",
            "Me not that kind of orc!",
        ]

        await ctx.channel.send(random.choice(phrase_list))


def setup(bot):
    bot.add_cog(BasicCommands(bot))
