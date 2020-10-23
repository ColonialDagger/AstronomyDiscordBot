from discord.ext import commands
from random import randint


class Randoms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(
        name='coin',
        description='Clips a coin.',
        context=True
    )
    async def coin(self, ctx):
        if randint(0, 1) == 1:
            await ctx.send('Heads.')
        else:
            await ctx.send('Tails.')

    @commands.command(
        name='randomint',
        description='Returns a random integer between two numbers.',
        context=True,
        aliases=['randint']
    )
    async def randomint(self, ctx, *args):
        await ctx.send(randint(int(args[0]), int(args[1])))

    @commands.command(
        name='randomlist',
        description='Returns a random item from a given list.',
        context=True,
        aliases=['randlist']
    )
    async def randomlist(self, ctx, *args):
        await ctx.send(args[randint(0, len(args))])


# Required in every cog, do not remove!
def setup(bot):
    bot.add_cog(Randoms(bot))
