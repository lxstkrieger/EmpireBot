# Import necessary modules from the Discord API and extension library
import discord
from discord.ext import commands
from discord.commands import slash_command
import logging

# Define a Discord cog for handling server information commands
class Serverinfo(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # Listener that runs when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Slash command to show server information
    @slash_command(description="shows the Server information's")
    async def serverinfo(self, ctx):
        try:
            # Create an embed with various server information fields
            serverinfo_embed = discord.Embed(
                title=f"Serverinfo for {ctx.guild.name}",
                color=discord.Color.blurple()
            )
            serverinfo_embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            serverinfo_embed.add_field(name="Guild Created at", value=ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            serverinfo_embed.add_field(name="Member count", value=f"{ctx.guild.member_count}", inline=True)
            serverinfo_embed.add_field(name="Number of Roles", value=f"{len(ctx.guild.roles)}", inline=False)
            serverinfo_embed.add_field(name="Number of Channels", value=f"{len(ctx.guild.channels)}", inline=False)
            serverinfo_embed.set_thumbnail(url=ctx.guild.icon)
            serverinfo_embed.set_footer(text=f"Embed created from {self.bot.user}")

            # Respond with the serverinfo embed, visible only to the command issuer
            await ctx.respond(embed=serverinfo_embed, ephemeral=True)
        except Exception as e:
            # Log an error to the bot.log file if there is an exception
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Serverinfo(bot))
