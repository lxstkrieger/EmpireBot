import discord
from discord.ext import commands
from discord.commands import slash_command
import sqlite3
import os
class WeddingSystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.DB_path = os.path.abspath(os.getenv("DATABASE_PATH", "databases"))
        db_file = os.path.join(self.DB_path, 'WeddingsSystem.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

        #TODO: SQLite3 datenbank hinzufügen der jeden nueuen Nutzer aufnimmt in die datenbank der heiratet




def setup(bot: discord.Bot):
    bot.add_cog(WeddingSystem(bot))