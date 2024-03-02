# Import necessary modules from the Discord API and extension library
import discord
from discord.ext import commands
from discord.commands import slash_command
import logging

# Define a Discord cog for handling kick-related commands
class Kick(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # Listener that runs when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Command for kicking a user from the server
    @slash_command(description="Kick a user")
    async def kick(self, ctx, member: discord.Member):
        try:
            # Check if the command issuer has the necessary permissions to kick members
            if ctx.author.guild_permissions.kick_members:
                # Kick the specified member from the server
                await ctx.guild.kick(member)

                # Create an Embed to announce the kick, including a thumbnail with the kicked user's avatar
                kick_embed = discord.Embed(
                    color=discord.Color.red(),
                    description=f"{member.mention} got kicked"
                )
                kick_embed.set_thumbnail(url=member.display_avatar)
                kick_embed.set_image(url="https://media1.tenor.com/m/5JmSgyYNVO0AAAAC/asdf-movie.gif")
                kick_embed.set_footer(text=f"Embed created from {self.bot.user}")

                # Send the kick embed to the channel where the command was executed, with ephemeral set to True
                # to make the response visible only to the command issuer
                await ctx.respond(embed=kick_embed, ephemeral=True)

        except Exception as e:
            # Log an error to the bot.log file if there is an exception
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Kick(bot))
