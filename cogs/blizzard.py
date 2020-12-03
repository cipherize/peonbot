from discord.ext import commands
from modules import blizzard
from tabulate import tabulate


class BlizzardAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def getequip(self, ctx, *, args):
        params = args.split("-")

        if len(params) != 2:
            await ctx.channel.send(
                "Sorry, but I need both the name and the realm, like Jiang-Aegwynn. Spaces and punctuation in the realm name are important!"
            )
            return

        equip_data = blizzard.get_equipment_summary(params[0], params[1])

        equip_list = [
            [item["slot"]["name"], item["name"], item["level"]["value"]]
            for item in equip_data
        ]

        equip_string = (
            "```\n" + tabulate(equip_list, ["Slot", "Item", "ILVL"]) + "\n```"
        )

        await ctx.channel.send(equip_string)


def setup(bot):
    bot.add_cog(BlizzardAPI(bot))
