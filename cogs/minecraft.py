import re
import discord
from tools import import_configs
from discord.ext import commands
from mcstatus import MinecraftServer


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.config = import_configs()

    @commands.command(
        name='minecraft',
        description='Checks status of a given server.',
        context=True,
        aliases=['mc']
    )
    async def mcserver(self, ctx, ip=None, thumbnail=None):
        if ip is None:  # If no IP set, use default from config.ini
            ip = self.config['MINECRAFT']['server_ip']
        if thumbnail is None:  # If no thumbnail set, use default from config.ini
            thumbnail = self.config['MINECRAFT']['server_thumbnail']
        try:
            server = MinecraftServer.lookup(ip)
            query = server.query()
        except:
            return print('error')
        name = query.raw['hostname']
        name = re.sub('§.|\[.*', '', name).split('\n')
        print('Collected MC server information for ' + name[0].strip())
        embed = discord.Embed(title=name[0].strip(), colour=discord.Colour.blue())
        embed.add_field(name='Players', value=str(query.players.online) + '/' + str(query.players.max))
        embed.add_field(name='Latency', value=str(server.ping()) + ' ms')
        embed.add_field(name='Version', value=query.software.version)
        embed.add_field(name='MOTD', value=name[1].strip(), inline=False)
        embed.add_field(name='Gametype', value=query.raw['gametype'], inline=False)
        embed.add_field(name='Map', value=query.raw['map'])
        embed.add_field(name='Server Type', value=query.software.brand)
        embed.set_thumbnail(url=thumbnail)
        if query.software.plugins:  # Get plugins if any are installed
            plugins = query.software.plugins
            plugins = ' '.join([str(i) for i in plugins])
            embed.add_field(name='Plugins', value=plugins)
        if query.players.online > 0:  # Gets player names if available
            players = '\n'.join(query.players.names[:5])
            embed.add_field(name='Current players', value=players)
        await ctx.send(embed=embed)


# Required in every cog, do not remove!
def setup(bot):
    bot.add_cog(Minecraft(bot))
