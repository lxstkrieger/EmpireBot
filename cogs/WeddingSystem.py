import discord
from discord.ext import commands
import sqlite3

class WeddingSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def marry(self, ctx, user: discord.Member):
        conn = sqlite3.connect('Wedding.db')
        cursor = conn.cursor()

        # Check whether the author is already married on this server
        cursor.execute('''
            SELECT * FROM wedding_system
            WHERE user_id = ? AND married = ? AND guild_id = ?
        ''', (ctx.author.id, True, ctx.guild.id))
        author_married = cursor.fetchone()

        # Check whether the other user is already married on this server
        cursor.execute('''
            SELECT * FROM wedding_system
            WHERE partner_id = ? AND married = ? AND guild_id = ?
        ''', (user.id, True, ctx.guild.id))
        user_married = cursor.fetchone()

        if author_married:
            not_marry = discord.Embed(
                color=discord.Color.red(),
                description=f"{ctx.author.mention}, you are already married on this server!")
            await ctx.send(embed=not_marry)
        elif user_married:
            not_marry2 = discord.Embed(
                color=discord.Color.red(),
                description=f"{user.mention} is already married on this server!")
            await ctx.send(embed=not_marry2)
        else:
            cursor.execute('''
                INSERT INTO wedding_system (guild_id, user_id, partner_id, married)
                VALUES (?, ?, ?, ?)
            ''', (ctx.guild.id, ctx.author.id, user.id, True))
            conn.commit()
            marry_embed = discord.Embed(
                color=discord.Color.green(),
                description=f"Congratulations {ctx.author.mention} and {user.mention}, you are now married on this server!")
            marry_embed.set_footer(text=f"Embed created by {self.bot.user}")

            await ctx.send(embed=marry_embed)
        conn.close()

    async def devorce(self, ctx, user: discord.Member):
        conn = sqlite3.connect('Wedding.db')
        cursor = conn.cursor()

        # Check if the author is married to the specified user on this server
        cursor.execute('''
            SELECT * FROM wedding_system
            WHERE ((user_id = ? AND partner_id = ?) OR (user_id = ? AND partner_id = ?))
            AND married = ? AND guild_id = ?
        ''', (ctx.author.id, user.id, user.id, ctx.author.id, True, ctx.guild.id))
        marriage = cursor.fetchone()

        if marriage:
            cursor.execute('''
                DELETE FROM wedding_system
                WHERE ((user_id = ? AND partner_id = ?) OR (user_id = ? AND partner_id = ?))
                AND married = ? AND guild_id = ?
            ''', (ctx.author.id, user.id, user.id, ctx.author.id, True, ctx.guild.id))
            conn.commit()
            divorce_embed = discord.Embed(
                color=discord.Color.green(),
                description=f"{ctx.author.mention} and {user.mention}, you are now divorced on this server.")
            divorce_embed.set_footer(text=f"Embed created by {self.bot.user}")

            await ctx.send(embed=divorce_embed)
        else:
            not_divorce = discord.Embed(
                color=discord.Color.red(),
                description=f"{ctx.author.mention}, you are not married to {user.mention} on this server.")
            await ctx.send(embed=not_divorce)

        conn.close()


def setup(bot):
    bot.add_cog(WeddingSystem(bot))
