from modules import blizzard, db
from discord.ext import commands


class CharManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def claim(self, ctx, *, args):
        params = args.split("-")

        if len(params) != 2:
            await ctx.channel.send(
                "Sorry, but I need both the name and the realm, like Jiang-Aegwynn. Spaces and punctuation in the realm name are important!"
            )
            return

        char_name = params[0]
        realm_name = params[1]
        realm_slug = blizzard.get_realm_slug(realm_name)

        if not realm_slug:
            await ctx.channel.send(
                "I don't know about that realm. Spaces and punctuation are important!"
            )
            return

        result = db.get_char_owner(char_name, realm_slug)

        if result:
            await ctx.channel.send("Someone has already claimed that character!")
            return

        db.set_char_owner(ctx.message.author.id, char_name, realm_slug)

        await ctx.channel.send(f"Done! {args} is now registered as yours.")

    @commands.command()
    async def list(self, ctx):
        results = db.get_my_characters(ctx.message.author.id)
        if not results:
            await ctx.channel.send("You haven't claimed any characters!")
        else:
            output = [
                "{}-{}".format(result[0], blizzard.get_realm_name(result[1]))
                for result in results
            ]

            output.insert(0, "```")
            output.append("```")
            await ctx.channel.send("\n".join(output))


def setup(bot):
    bot.add_cog(CharManagement(bot))
