import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord


# Define a Discord cog for handling kick-related commands
class Kick(ezcord.Cog):
    # Command for kicking a user from the server
    @slash_command(description="Kick a user")
    async def kick(self, ctx, member: discord.Member):
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

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Kick(bot))
