import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import logging
import requests
import os

class Crypto(ezcord.Cog):
    # Listener that runs when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')


def setup(bot: discord.Bot):
    bot.add_cog(Crypto(bot))