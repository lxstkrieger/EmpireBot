import discord
from discord.commands import slash_command
import ezcord
import requests


class Memes(ezcord.Cog):
    @slash_command(description='sends a meme')
    async def meme(self, ctx):
        # The meme api query is made here.
        meme_response = requests.get('https://meme-api.com/gimme')

        if meme_response.status_code == 200:
            meme_data = meme_response.json()
            meme_url = meme_data.get('url')
            meme_embed = discord.Embed(
                color=discord.Color.magenta()
            )
            meme_embed.set_image(url=f"{meme_url}")
            meme_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=meme_embed)
        else:
            await ctx.send('Error fetching meme.')


def setup(bot: discord.Bot):
    bot.add_cog(Memes(bot))
