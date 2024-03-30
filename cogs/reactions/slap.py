import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import requests


class Slap(ezcord.Cog):
    @slash_command(description="someone slap's someone")
    async def slap(self, ctx, member: discord.Member):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/slap")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        slap_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{ctx.author.mention} slap's {member.mention}"
        )
        # Here the gif(gif url) is added to the embed as an image.
        slap_embed.set_image(url=image)
        slap_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=slap_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Slap(bot))
