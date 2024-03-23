import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import logging
import requests


class Neko(ezcord.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="gave you an picture from an Neko")
    async def neko(self, ctx):
        try:
            # The api query is made here
            resp = requests.get("https://nekos.best/api/v2/neko")
            data = resp.json()
            # here the first result is taken and written to the variable image
            image = data["results"][0]["url"]

            # The embed is created here. Which will later send the gif
            neko_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} neko"
            )
            # Here the gif(gif url) is added to the embed as an image.
            neko_embed.set_image(url=image)
            neko_embed.set_footer(text=f"Embed created from {self.bot.user}")
            # The baka_embed is sent here
            await ctx.respond(embed=neko_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Neko(bot))
