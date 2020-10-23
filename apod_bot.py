import discord
from os import listdir
from discord.ext import commands
from configparser import ConfigParser
from systemd.daemon import notify, Notification
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cogs.astronomy import Astronomy


class apodBot:  # TODO Block args from passing mentions
    """
    Represents apodBot which functions with Discord. The bot is only started when apodBot.run() is called.

    Parameters
    -----------
    config_file: Optional[:class:`str`]
        Represents the path to the config.ini. Defaults to 'config.ini' if no path is given.
    """
    def __init__(self, config_file='config.ini', cogs_directory='cogs'):
        self.running = False  # Used to prevent on_ready being run during reconnect

        # Import configs
        try:
            print('Importing configurations...', flush=True)
            self.config = ConfigParser()
            self.config.read(config_file)
            if not self.config.sections() or 'CLIENT' not in self.config.sections():
                raise ImportError
        except ImportError:
            exit('Error on importing configurations!')

        # Init bot
        print('Initializing bot...', flush=True)
        self.bot = commands.Bot(
            command_prefix='!apod ',  # TODO Find a way to include trailing spaces from ConfigParser('config.ini')
            # command_prefix=self.config['COMMAND']['call_string'],
            description="Astronomy Picture of the Day Bot",
            owner_id=132679831337959425,
            case_insensitive=True  # TODO Figure out if this actually works
        )
        self.cogs = [i[:-3] for i in listdir(cogs_directory) if i.endswith('.py')]  # Sets cogs directory
        self.cogs = ['cogs.' + cog for cog in self.cogs]
        self.sched = AsyncIOScheduler()

        # Init decorators as definitions
        print('Initializing decorators...')
        self.on_ready = self.bot.event(self.on_ready)

    # Set status
    async def set_status(self, status):
        """|coro|

        Sets status on Discord bot.

        Parameters
        -----------
        status: :class:`str`
            Sets status string.
        """
        print('Setting status...', flush=True)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=status))

    async def load_cogs(self):
        """|coro|

        Loads cogs from directory
        """
        print('Loading cogs...')
        for cog in self.cogs:
            self.bot.load_extension(cog)

    async def load_scheds(self):
        """|coro|

        Schedules tasks
        """
        print('Scheduling tasks...')
        t = self.config['ASTRONOMY']['announcement_time'].split(':')
        self.sched.add_job(func=Astronomy.announce,
                           args=[self.bot],
                           trigger=CronTrigger(hour=t[0], minute=t[1], second=t[2]))
        del t
        self.sched.start()

    async def on_ready(self):
        """|coro|

        Called when bot is ready.
        """
        if self.running:  # Used to prevent on_ready being run during reconnect
            return
        self.running = True
        await self.load_cogs()
        await self.set_status(self.config['CLIENT']['status'])  # Set Discord Status
        await self.load_scheds()
        notify(Notification.READY)  # Sends systemd notification
        print('Logged in as {0.user}'.format(self.bot) + '!\n', flush=True)

    def start(self):
        """|func|

        Creates a connection to Discord and starts bot.
        """
        print('Starting bot...', flush=True)
        self.bot.run(self.config['CLIENT']['token'], bot=True, reconnect=True)


if __name__ == '__main__':
    apodBot().start()
