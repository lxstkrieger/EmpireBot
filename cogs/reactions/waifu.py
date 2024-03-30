import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import requests


class Waifu(ezcord.Cog):
    @slash_command(description="gave you an picture from an Waifu")
    async def waifu(self, ctx):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/waifu")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        waifu_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{ctx.author.mention} Waifu"
        )
        # Here the gif(gif url) is added to the embed as an image.
        waifu_embed.set_image(url=image)
        waifu_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=waifu_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Waifu(bot))
