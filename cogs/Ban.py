import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import logging

# Define a Discord cog for handling ban-related commands


class Ban(ezcord.Cog):
    # Listener that runs when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Command for banning a user
    @slash_command(description="Ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        try:
            # Ban the mentioned user
            await ctx.guild.ban(member)

            # Create an Embed to announce the ban, including a thumbnail of the banned user's profile picture
            # The embed also features a small funny gif as an image
            ban_embed = discord.Embed(
                color=discord.Color.red(),
                description=f"{member.mention} got banned"
            )
            ban_embed.set_thumbnail(url=member.display_avatar)
            ban_embed.set_image(url="https://media1.giphy.com/media/hSXiJbWunRqZMr0KTE/giphy.gif?cid=ecf05e47c1tyzvsa9muz9l7y4m2hitfojqoqbjw8p393qcgk&ep=v1_gifs_search&rid=giphy.gif&ct=g")
            ban_embed.set_footer(text=f"Embed created from {self.bot.user}")

            # Send the ban embed to the channel where the command was executed, with ephemeral set to True
            # to make the response visible only to the command issuer
            await ctx.respond(embed=ban_embed, ephemeral=True)

        except Exception as e:
            # Log an error to the bot.log file if there is an exception
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Ban(bot))
