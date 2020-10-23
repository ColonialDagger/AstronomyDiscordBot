import requests
import discord
import tools
import re
import json
from bs4 import BeautifulSoup
from os import mkdir, path
from discord.ext import commands


class Astronomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.config = tools.import_configs()

    @commands.command(
        name='apod',
        description='Returns Astronomy Picture of the Day by NASA.',
        context=True
    )
    async def astropix(self, ctx, arg1=''):
        """|coro|

        Sends Discord embed with Astronomy Picture of the Day as reply.

        Parameters
        -----------
        ctx: :class:`discord.ext.commands.context.Context`
        Context object provided by discord.py module.
        arg1: :class:`str`
        `sub` or `unsub` to subscribe/unsubscribe channel.
        """
        if arg1 == ('sub' or 'unsub'):  # Subs or unsubs channel
            if Astronomy.sub(ctx.guild.id, ctx.channel.id):
                await ctx.send('This channel has been subscribed to Astronomy Picture of the Day from NASA!')
            else:
                await ctx.send('This channel has been unsubscribed to Astronomy Picture of the Day from NASA.')
        elif arg1 == 'new':  # Gets new Astropix
            self.getnew()
        else:  # Sends Astropix
            if not path.exists('resources/apod/apod.txt') or not path.exists('resources/apod/apod.html'):
                self.getnew()
            response = tools.readfile('resources/apod/apod.txt')
            embed = discord.Embed(
                title=response[1],
                description=response[2],
                colour=discord.Colour.blue()
            )
            embed.set_author(name='Astronomy Picture of the Day')
            embed.set_footer(text='Credit: ' + response[3])
            embed.set_thumbnail(url=tools.import_configs()['ASTRONOMY']['thumbnail'])
            if 'youtube' in response[0]:  # Embed video or image, depending on which it is
                await ctx.send(response[0])
            else:
                embed.set_image(url=response[0])
            await ctx.send(embed=embed)

    @staticmethod
    def sub(guild, channel):
        guild = str(guild)
        with open('resources/apod/apod_channels.json') as f:
            data = json.load(f)

        if guild not in data:  # Add guild and channel if neither exist
            data[guild] = []
            data[guild].append(channel)
            new_addition = True
        else:
            if channel not in data[guild]:  # Add channel if guild exists
                data[guild].append(channel)
                new_addition = True
            else:  # Remove channel if guild and channel exists
                data[guild].remove(channel)
                new_addition = False
                if len(data[guild]) == 0:  # Remove guild if empty after removing channel
                    del data[guild]

        with open('resources/apod/apod_channels.json', 'w') as f:
            json.dump(data, f)
        return new_addition


    @staticmethod
    def getnew():
        """|static|

                Retrieves new Astronomy Picture of the Day from NASA
        """
        # Create storage directory
        for dir in ['resources', 'resources/apod']:
            try:
                mkdir(dir)
            except FileExistsError:
                pass

        # Get HTML
        html_file = requests.get(tools.import_configs()['ASTRONOMY']['url'])
        tools.savefile(html_file, 'resources/apod/apod.html')

        # Search for image or video
        soup = BeautifulSoup(html_file.content, 'html.parser')
        if soup.img:
            content = 'https://apod.nasa.gov/apod/' + soup.img['src']
        elif soup.iframe:
            content = soup.iframe['src']
        else:
            content = 'Content not found. Contact developer.'
        if 'youtube' in content:  # Gets YouTube URL if video
           content = 'https://www.youtube.com/watch?v=' + content[content.find('/embed/')+7:content.find('?')]

        # Get description
        body = soup.body.text
        desc = re.sub(' +',
                      ' ',
                      body[body.find('Explanation') + 15:])
        desc = re.sub(' +', ' ', re.sub('\n', ' ', desc[0:desc.find('\n\n\n')-1]))

        # Get title
        title = body[body.find('\n\n\n\n') + 6:]
        title = title[1:title.find('\n') - 2]

        # Get author
        author = re.sub(' +', ' ', body[body.find(':') + 3:body.find('Explanation') - 4].replace('\n', ' '))

        # Save to apod.txt
        data = [content, title, desc, author]
        tools.savefile(data, 'resources/apod/apod.txt')
        return print('Retrieved new APOD data.\n')

    @staticmethod
    async def announce(bot):
        """|static|

                Retrieves and announces new Astronomy Picture of the Day from NASA

        Parameters
        -----------
        bot: :class:`commands.bot.Bot`
        Bot class provided by discord.ext.commands
        """
        Astronomy.getnew()
        print('Broadcasting Astronomy Picture of the Day...')
        try:
            with open('resources/apod/apod_channels.json') as f:
                data = json.load(f)
            for guild in data:
                channels = data[guild]
                for i in channels:
                    ctx = bot.get_channel(int(i))
                    await Astronomy.astropix(Astronomy.astropix, ctx)
            return
        except FileNotFoundError:
            print('No subscribed channels to send Astropix to.')


# Required in every cog, do not remove!
def setup(bot):
    bot.add_cog(Astronomy(bot))
