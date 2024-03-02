import discord
from datetime import datetime

from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import logging


class Bans(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Get a list of members who are banned from this server!")
    # Requires the 'ban_members' permission to execute this command
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        try:
            # Defers the response to avoid timeout errors
            await ctx.defer()
            # Creates an Embed for the list of bans with title, timestamp, and color
            bans_embed = discord.Embed(title=f"List of Bans in {ctx.guild}", timestamp=datetime.now(),
                                       color=discord.Colour.red())

            # Iterates through the list of banned users in the server
            async for entry in ctx.guild.bans():

                # Checks if there are already 25 bans added to the Embed
                if len(bans_embed.fields) >= 25:
                    break

                # Checks if the total size of the Embed is exceeding a limit
                if len(bans_embed) > 5900:
                    bans_embed.add_field(name="Too many bans to list", value="", inline=True)
                else:
                    # Adds information about the banned user to the Embed
                    bans_embed.add_field(name=f"Ban",
                                         value=f"Username: {entry.user.name}#{entry.user.discriminator}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}",
                                         inline=False)
                    bans_embed.set_footer(text=f"Embed created from {self.bot.user}")

            # Sends the Embed as a response
            await ctx.respond(embed=bans_embed)

        except Exception as e:
            # Logs an error to the bot.log file if there is an exception
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # This function sends a message when the user have not the permissions or when other things happen
    @bans.error
    async def banserror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need ban members permissions to do this!")
        else:
            await ctx.respond(f"Something went wrong: ```{error}```.")
            raise error


def setup(bot: discord.Bot):
    bot.add_cog(Bans(bot))
