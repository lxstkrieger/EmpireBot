import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Dance(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="dancing")
    async def dance(self, ctx):
        try:
            # The api query is made here
            resp = requests.get("https://nekos.best/api/v2/dance")
            data = resp.json()
            # here the first result is taken and written to the variable image
            image = data["results"][0]["url"]

            # The embed is created here. Which will later send the gif
            dance_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} are dancing"
            )
            # Here the gif(gif url) is added to the embed as an image.
            dance_embed.set_image(url=image)
            dance_embed.set_footer(text=f"Embed created from {self.bot.user}")
            # The baka_embed is sent here
            await ctx.respond(embed=dance_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Dance(bot))