import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import ezcord

# Define Unban as a Discord cog for handling unbans
class Unban(ezcord.Cog):
    # Slash command to unban a specified member
    @slash_command(name="unban", description="Unbans the specified member.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, reason: Option(str, "Enter a reason for the unban", required=False, default='no reason given')):
        # Unban the specified user from the guild
        await ctx.guild.unban(user)

        # Create an embed with information about the success of the unban
        unban_embed = discord.Embed(
            title="Success",
            description=f"{user.mention} has been unbanned.",
            color=discord.Color.green()
        )
        unban_embed.add_field(name="Reason", value=reason)
        unban_embed.set_image(url="https://media1.tenor.com/m/B3iUTS5HXAAAAAAC/quby-cute.gif")
        unban_embed.set_thumbnail(url=f"{user.display_avatar}")

        # Send the embed as an ephemeral response to the command user
        await ctx.response.send_message(embed=unban_embed, ephemeral=True)

# Function to set up the cog when the bot is started
def setup(bot: discord.Bot):
    bot.add_cog(Unban(bot))
