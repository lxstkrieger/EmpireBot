import discord
from discord.commands import slash_command
import ezcord
import requests


class Sleep(ezcord.Cog):
    @slash_command(description="someone is sleeping")
    async def sleep(self, ctx):
        # The api query is made here
        resp = requests.get("https://nekos.best/api/v2/sleep")
        data = resp.json()
        # here the first result is taken and written to the variable image
        image = data["results"][0]["url"]

        # The embed is created here. Which will later send the gif
        sleep_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{ctx.author.mention} sleeps"
        )
        # Here the gif(gif url) is added to the embed as an image.
        sleep_embed.set_image(url=image)
        sleep_embed.set_footer(text=f"Embed created from {self.bot.user}")
        # The baka_embed is sent here
        await ctx.respond(embed=sleep_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Sleep(bot))
