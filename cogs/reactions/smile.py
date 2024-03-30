import discord
from discord.commands import slash_command
import ezcord
import requests


class Smile(ezcord.Cog):
    @slash_command(description="someone is just smileing")
    async def smile(self, ctx):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/smile")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        smile_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{ctx.author.mention} smiles"
        )
        # Here the gif(gif url) is added to the embed as an image.
        smile_embed.set_image(url=image)
        smile_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=smile_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Smile(bot))
