import csv
from discord.ext import commands


class Covid(commands.Cog):
    def __init__(self, bot=None):
        if bot:
            self.bot = bot
        self._last_member = None
        self.data_us = []
        self.data_world = []

    @commands.command(
        name='covid',
        description='Returns COVID-19 statistics.',
        aliases=['cv', 'cv19', 'c19', 'covid19', 'corona', 'coronavirus']
    )
    async def sendtodiscord(self, ctx, country=None, state=None, county=None):
        await ctx.send('Temporary placeholder.')

    def covid(self, country=None, state=None, county=None):
        self.data_world = self.getdata_world()
        self.data_us = self.getdata_us()
        # if not country:
        #     self.getglobal()
        # elif not state:
        #     self.getcountry(country)
        # elif not county:
        #     self.getstate(country, state)
        # elif county:
        #     self.getcounty(country, state, county)
        return self

    @staticmethod
    def getdata_world():  # TODO Setup would/country data grab
        return

    @staticmethod
    def getdata_us(file_path='resources/covid19/time_series_covid19_confirmed_US.csv'):
        with open(file_path) as file:
            data = list(csv.reader(file.read().splitlines(), delimiter=','))
        return data

    # TODO Create function to get new data

# Required in every cog, do not remove!
def setup(bot):
    bot.add_cog(Covid(bot))
