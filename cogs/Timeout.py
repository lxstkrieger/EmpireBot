# Import necessary modules for Discord API, extension library, logging, datetime, and humanfriendly
import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import datetime
from datetime import datetime
import humanfriendly

# Define Timeout as a Discord cog for handling timeouts
class Timeout(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # Listener that runs when the bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Slash command to put a member in timeout
    @slash_command()
    @commands.has_permissions(ban_members=True)
    async def timeout(self, ctx, member: discord.Member, time=None, reason=None):
        try:
            # Parse the human-readable time duration into seconds
            time = humanfriendly.parse_timespan(time)

            # Apply timeout to the member until the specified time
            await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)

            # Create and send an embed with information about the timeout
            timeout_embed = discord.Embed(
                description=f"{member} was put into timeout for {time}. Because of: {reason}",
                color=discord.Color.red()
            )
            timeout_embed.set_thumbnail(url=f"{member.display_avatar}")
            timeout_embed.set_image(url="https://media1.giphy.com/media/1AiMQkwz1cpFkzKYxJ/giphy.gif?cid=ecf05e473hdt4xa9ag1j7ztgpjscfmocjab22bfqpsns4irq&ep=v1_gifs_search&rid=giphy.gif&ct=g")
            await ctx.send(embed=timeout_embed)
        except Exception as e:
            # Log any errors that occur during the timeout command
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the Timeout cog when the bot is started
def setup(bot: discord.Bot):
    bot.add_cog(Timeout(bot))
