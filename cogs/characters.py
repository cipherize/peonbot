from modules import blizzard, db
from pprintpp import pprint
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

        if not blizzard.get_character_summary(char_name, realm_slug):
            await ctx.channel.send(
                "I can't find a character by that name on that realm."
            )
            return

        result = db.get_char_owner(char_name, realm_slug)

        if result:
            await ctx.channel.send("Someone has already claimed that character!")
            return

        db.set_char_owner(ctx.message.author.id, char_name, realm_slug)

        await ctx.channel.send(f"Done! {args} is now registered as yours.")

    @commands.command()
    async def unclaim(self, ctx, *, args):
        params = args.split("-")

        if len(params) != 2:
            await ctx.channel.send(
                "Sorry, but I need both the name and the realm, like Jiang-Aegwynn. Spaces and punctuation in the realm name are important!"
            )
            return

        char_name = params[0]
        realm_name = params[1]
        realm_slug = blizzard.get_realm_slug(realm_name)

        result = db.get_char_owner(char_name, realm_slug)

        if not blizzard.get_character_summary(char_name, realm_slug):
            await ctx.channel.send(
                "I can't find a character by that name on that realm."
            )
            return

        if not result:
            await ctx.channel.send(
                "Good news, you don't own that character! In fact, no one does."
            )
            return

        if result[0] != ctx.message.author.id:
            await ctx.channel.send(
                "Good news and bad news. Bad news: You can't unclaim that character. Good news: Because it isn't yours."
            )
            return

        result = db.del_char_owner(char_name, realm_slug)

        if not result:
            await ctx.channel.send(
                "Couldn't unclaim that character. Are you signed up for a raid?"
            )
        else:
            await ctx.channel.send(
                f"Okay! {char_name}-{realm_name} is no longer claimed by you."
            )

    @commands.command()
    async def mine(self, ctx):
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

    @commands.command()
    async def summary(self, ctx, *, args):
        params = args.split("-")

        if len(params) != 2:
            await ctx.channel.send(
                "Sorry, but I need both the name and the realm, like Jiang-Aegwynn. Spaces and punctuation in the realm name are important!"
            )
            return

        char_name = params[0]
        realm_name = params[1]
        realm_slug = blizzard.get_realm_slug(realm_name)

        result = blizzard.get_character_summary(char_name, realm_slug)

        if not result:
            await ctx.channel.send(
                "I can't find a character by that name on that realm."
            )
            return

        pprint(result)


def setup(bot):
    bot.add_cog(CharManagement(bot))
