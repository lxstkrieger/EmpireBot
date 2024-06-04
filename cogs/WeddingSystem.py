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
            not_marry = discord.Embed(
                color= discord.Color.red(),
                description=f"{ctx.author.mention}, you are already married!")
            await ctx.response(embed=not_marry, ephemeral=True)
        elif user_married:
            not_marry2 = discord.Embed(
                color= discord.Color.red(),
                description=f"{user.mention} is already married!")
            await ctx.response(embed=not_marry2, ephemeral=True)
        else:
            cursor.execute('''
                INSERT INTO wedding_system (guild_id, user_id, partner_id, married)
                VALUES (?, ?, ?, ?)
            ''', (ctx.guild.id, ctx.author.id, user.id, True))
            conn.commit()
            marry_embed = discord.Embed(
                color=discord.Color.green(),
                description=f"Congratulations {ctx.author.mention} and {user.mention}, are now married!")
            marry_embed.set_footer(text=f"Embed created from {self.bot.user}")

            await ctx.response(embed=marry_embed,ephemeral=False)
        conn.close()

    async def devorce(self, ctx, user: discord.Member):
        conn = sqlite3.connect('Wedding.db')  # Connect to your database
        cursor = conn.cursor()

        # Check if the author is married to the specified user
        cursor.execute('''
            SELECT * FROM wedding_system
            WHERE (user_id = ? AND partner_id = ?) OR (user_id = ? AND partner_id = ?)
            AND married = ?
        ''', (ctx.author.id, user.id, user.id, ctx.author.id, True))
        marriage = cursor.fetchone()

        if marriage:
            cursor.execute('''
                DELETE FROM wedding_system
                WHERE (user_id = ? AND partner_id = ?) OR (user_id = ? AND partner_id = ?)
                AND married = ?
            ''', (ctx.author.id, user.id, user.id, ctx.author.id, True))
            conn.commit()
            divorce_embed = discord.Embed(
                color=discord.Color.green(),
                description=f"{ctx.author.mention} and {user.mention}, you are now divorced.")
            divorce_embed.set_footer(text=f"Embed created by {self.bot.user}")

            await ctx.response.send_message(embed=divorce_embed, ephemeral=False)
        else:
            not_divorce = discord.Embed(
                color=discord.Color.red(),
                description=f"{ctx.author.mention}, you are not married to {user.mention}.")
            await ctx.response.send_message(embed=not_divorce, ephemeral=True)

        conn.close()




def setup(bot: discord.Bot):
    bot.add_cog(WeddingSystem(bot))