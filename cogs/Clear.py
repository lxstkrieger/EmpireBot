import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import logging

# Define a Discord cog for handling clear-related commands


class Clear(ezcord.Cog):
    # Listener that runs when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Command for clearing a specified number of messages in a channel
    @slash_command(description="clears a channel with your amount")
    @commands.has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)  # NOTE: This line appears twice and can be removed as it's redundant.
    async def clear(self, ctx, amount: int = 1000):
        try:
            # Purge messages in the channel up to the specified amount
            await ctx.channel.purge(limit=amount)

            # Create an Embed to announce the cleared messages, including a thumbnail with a gif
            clear_embed = discord.Embed(
                title=f"{amount} Messages got purged",
                description=f"This Message delete after 3 Seconds",
                color=discord.Color.magenta()
            )
            clear_embed.set_thumbnail(url="https://media4.giphy.com/media/jAYUbVXgESSti/giphy.gif?cid=ecf05e47wrxukzkng5pw6kule2v7lk64cnal1km55s8kw0dp&ep=v1_gifs_search&rid=giphy.gif&ct=g")
            clear_embed.set_footer(text=f"Embed created from {self.bot.user}")

            # Send the clear embed to the channel where the command was executed, with delete_after set to 3 seconds
            await ctx.respond(embed=clear_embed, delete_after=3)

        except Exception as e:
            # Log an error to the bot.log file if there is an exception
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Clear(bot))
