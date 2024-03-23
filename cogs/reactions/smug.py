import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import logging
import requests


class Smug(ezcord.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="someone Smug's at you")
    async def smug(self, ctx):
        try:
            # The api query is made here
            resp = requests.get("https://nekos.best/api/v2/smug")
            data = resp.json()
            # here the first result is taken and written to the variable image
            image = data["results"][0]["url"]

            # The embed is created here. Which will later send the gif
            smug_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} smug's"
            )
            # Here the gif(gif url) is added to the embed as an image.
            smug_embed.set_image(url=image)
            smug_embed.set_footer(text=f"Embed created from {self.bot.user}")
            # The baka_embed is sent here
            await ctx.respond(embed=smug_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Smug(bot))
