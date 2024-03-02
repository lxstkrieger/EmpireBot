import discord
from discord.ext import commands
from discord.commands import slash_command


class pterodactylControl(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # TODO: Implement Private Pterodactyl Panel and to Control it via Discord Bot (Planing)
def setup(bot: discord.Bot):
    bot.add_cog(pterodactylControl(bot))
