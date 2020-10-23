import tools
from discord.ext import commands
from random import randint


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(
        name='gay',
        description='Checks whether a given argument is gay.',
        context=True
    )
    async def gay(self, ctx, *args):  # TODO Make lines more concise, fix
        # low = [x.lower() for x in args]
        # low = [x.replace('ll', 'l') for x in low]
        # low2 = [x.replace('k', 'c') for x in low]
        # colonial = ['colonialdagger', 'colonjabber', 'colonial', 'colon', 'jabber', 'colonjabber']
        # if not low[0].isalpha() or not low2[0].isalpha():
        #     await ctx.send('Only letters are allowed, {0.user}, you fucker.'.format(ctx.message.author.name))
        #     return
        # if low:
        #     if 'orange' in low and 'clan' in low:
        #         await ctx.send('Orange clan not gay.')
        #     elif 'matrix' in low and 'clan' in low:
        #         await ctx.send('Matrix clan super gay.')
        #     elif low[0] in ['periodic', 'chicken', 'periodicchicken'] in low:
        #         await ctx.send('Periodic Chicken is Canadian gay, the worst kind of gay.')
        #     elif 'twist' in low:
        #         await ctx.send('Do not insult the chin. <:Chin:762429659916271646>')
        #     elif 'sharky' in low:
        #         await ctx.send('Sharky ist schwul, sag es nicht Adolf.')
        #     elif low[0] in colonial or low2[0] in colonial:
        #         await ctx.send(ctx.message.author.name + ' is gay.')
        #     else:
        #         await ctx.send(args[0] + ' is gay.')
        # else:
        #     await ctx.send(ctx.message.author.name + ' is gay.')
        await ctx.send('Orange is mega gay.')

    @commands.command(
        name='warcrime',
        description='Returns a war crime.',
        context=True
    )
    async def warcrime(self, ctx):
        try:
            warcrimes = tools.readfile('resources/warcrime.txt')
            await ctx.send(warcrimes[randint(0, len(warcrimes))])
        except FileNotFoundError:
            print('No warcrime.txt file!')


# Required in every cog, do not remove!
def setup(bot):
    bot.add_cog(Fun(bot))
