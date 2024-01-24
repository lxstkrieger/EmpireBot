import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import logging


class Userinfo(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="shows info from a specific user")
    async def userinfo(self, ctx, member: Option(discord.Member, autocomplete=True, required=True)):
        try:
            userinfo_embed = discord.Embed(
                title="Userinfo for",
                description=f"{member.mention}",
                color=discord.Color.blurple()
            )
            userinfo_embed.add_field(name="Server Joined at", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            userinfo_embed.add_field(name="Highest role", value=f"{member.top_role.mention}", inline=True)
            userinfo_embed.add_field(name="Nickname", value=f"{member.nick}")
            userinfo_embed.add_field(name="User ID", value=f"{member.id}")
            userinfo_embed.add_field(name=f"Avatar Image", value=f"{member.avatar.url}")
            userinfo_embed.set_thumbnail(url=member.avatar)
            userinfo_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=userinfo_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Userinfo(bot))
