from discord.ext import commands
from datetime import datetime


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(
        name='ping',
        description='Returns bot latency.',
        aliases=['p']
    )
    async def ping(self, ctx):
        dt = datetime.utcnow()-ctx.message.created_at
        if dt.seconds == 0:
            await ctx.send('Pong! Latency: ' + str(dt.microseconds)[:3] + 'ms')
        else:
            await ctx.send('Pong! Latency: ' + str(dt.seconds) + '.' + str(dt.microseconds)[:3] + 's')


# Required in every cog, do not remove!
def setup(bot):
    bot.add_cog(Ping(bot))
