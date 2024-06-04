import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import sqlite3
import os

DB_path = os.path.abspath(os.getenv("DATABASE_PATH", "databases"))
db_file = os.path.join(DB_path, 'Wedding.db')
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Initialize the database table if it does not exist
cursor.execute('''
          CREATE TABLE IF NOT EXISTS wedding_system (
              guild_id INTEGER,
              user_id INTEGER,
              partner_id INTEGER,
              married BOOLEAN,
          )
          ''')
conn.commit()
class WeddingSystem(ezcord.Cog):
    async def marry(self, ctx, user: discord.Member):
        conn = sqlite3.connect('Wedding.db')  # Connect to your database
        cursor = conn.cursor()

        # Check whether the author is already married
        cursor.execute('''
            SELECT * FROM wedding_system
            WHERE user_id = ? AND married = ?
        ''', (ctx.author.id, True))
        author_married = cursor.fetchone()

        # Check whether the other user is already married
        cursor.execute('''
            SELECT * FROM wedding_system
            WHERE partner_id = ? AND married = ?
        ''', (user.id, True))
        user_married = cursor.fetchone()

        if author_married:
            await ctx.send(f"{ctx.author.mention}, du bist bereits verheiratet!")
        elif user_married:
            await ctx.send(f"{user.mention} ist bereits verheiratet!")
        else:
            cursor.execute('''
                INSERT INTO wedding_system (guild_id, user_id, partner_id, married)
                VALUES (?, ?, ?, ?)
            ''', (ctx.guild.id, ctx.author.id, user.id, True))
            conn.commit()
            await ctx.send(f"Herzlichen Glückwunsch {ctx.author.mention} und {user.mention}, ihr seid jetzt verheiratet!")

        conn.close()



def setup(bot: discord.Bot):
    bot.add_cog(WeddingSystem(bot))