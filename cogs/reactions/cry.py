import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import requests


class Cry(ezcord.Cog):
    @slash_command(description="crying (at something, because of something)")
    async def cry(self, ctx):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/cry")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        cry_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{ctx.author.mention} are crying"
        )
        # Here the gif(gif url) is added to the embed as an image.
        cry_embed.set_image(url=image)
        cry_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=cry_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Cry(bot))
