import discord
from discord.commands import slash_command
import ezcord


# Define a Discord cog for handling server information commands
class Serverinfo(ezcord.Cog):

    # Slash command to show server information
    @slash_command(description="shows the Server information's")
    async def serverinfo(self, ctx):
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

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Serverinfo(bot))
