import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Baka(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Bakaing someone xD")
    async def baka(self, ctx, member: discord.Member):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/baka")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        baka_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{member.mention} is a BAKA BAKA BAKA BAKA !!!!"
        )
        # Here the gif(gif url) is added to the embed as an image.
        baka_embed.set_image(url=image)
        baka_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=baka_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Baka(bot))
