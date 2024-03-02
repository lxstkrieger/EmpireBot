import discord
from discord.ext import commands
from discord.commands import slash_command
import requests
import logging


class Memes(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description='sends a meme')
    async def meme(self, ctx):
        try:
            # The meme api query is made here.
            meme_response = requests.get('https://meme-api.com/gimme')

            if meme_response.status_code == 200:
                meme_data = meme_response.json()
                meme_url = meme_data.get('url')
                meme_embed = discord.Embed(
                    color=discord.Color.magenta()
                )
                meme_embed.set_image(url=f"{meme_url}")
                meme_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=meme_embed)
            else:
                await ctx.send('Error fetching meme.')
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Memes(bot))
