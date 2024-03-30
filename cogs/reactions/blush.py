import discord
from discord.commands import slash_command
import ezcord
import requests


class Blush(ezcord.Cog):

    @slash_command(description="blushes")
    async def blush(self, ctx):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/blush")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        blush_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{ctx.author.mention} blushes"
        )
        # Here the gif(gif url) is added to the embed as an image.
        blush_embed.set_image(url=image)
        blush_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=blush_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Blush(bot))
