import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord
import sqlite3
from typing import Optional
import os
import logging

# If you want to give roles to the user at any specific level upgrade, add them here
level_roles = ["Level-5+", "Level-10+", "Level-15+"]
level_thresholds = [5, 10, 15]

# Define a Discord cog for handling the leveling system
class Levelsys(ezcord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.DB_path = os.path.abspath(os.getenv("DATABASE_PATH", "databases"))
        db_file = os.path.join(self.DB_path, 'Levelsystem.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create the levels table in the database if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS levels (
                guild_id INTEGER,
                user_id INTEGER,
                xp INTEGER,
                level INTEGER,
                PRIMARY KEY (guild_id, user_id)
            )
        ''')
        self.conn.commit()

    # Listener that runs when a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            guild_id = message.guild.id
            user_id = message.author.id

            # Check if the user exists in the database, and if not, insert them with initial values
            self.cursor.execute('''
                INSERT OR IGNORE INTO levels (guild_id, user_id, xp, level)
                VALUES (?, ?, 0, 1)
            ''', (guild_id, user_id))

            # Increment the user's XP
            self.cursor.execute('''
                UPDATE levels SET xp = xp + ? WHERE guild_id = ? AND user_id = ?
            ''', (25, guild_id, user_id))

            # Get current XP and level
            self.cursor.execute('''
                SELECT xp, level FROM levels WHERE guild_id = ? AND user_id = ?
            ''', (guild_id, user_id))

            xp, level = self.cursor.fetchone()

            # Check if the user leveled up
            if xp >= level * 100:
                # Update the user's XP and level, and give roles if necessary
                self.cursor.execute('''
                    UPDATE levels SET xp = 0, level = level + 1
                    WHERE guild_id = ? AND user_id = ?
                ''', (guild_id, user_id))

                for i in range(len(level_roles)):
                    if level + 1 == level_thresholds[i]:
                        await self.check_and_assign_role(message.guild, message.author, level_roles[i])

                # Commit changes to the database
                self.conn.commit()

    # Helper function to check and assign a role to a user
    async def check_and_assign_role(self, guild, user, role_name):
        try:
            # Check if the role exists, otherwise create it
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                permissions = discord.Permissions(send_messages=True, read_messages=True)
                role = await guild.create_role(name=role_name, permissions=permissions)

            # Add the role to the user
            await user.add_roles(role)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # Slash command to show the rank of a specific user
    @slash_command(description="shows the rank from a specific user")
    async def rank(self, ctx, user: Optional[discord.Member]):
        try:
            userr = user or ctx.author

            guild_id = ctx.guild.id
            user_id = userr.id

            # Get user's data from the database
            self.cursor.execute('''
                SELECT xp, level FROM levels WHERE guild_id = ? AND user_id = ?
            ''', (guild_id, user_id))
            result = self.cursor.fetchone()
            if result is not None:
                xp, lvl = result
                await ctx.respond(f"{userr.mention} is at Level {lvl} with {xp} XP.", ephemeral=True)
            else:
                # If no data is found, provide a helpful embed
                rank_embed = discord.Embed(
                    color=discord.Color.red(),
                    description="Es sind keine Daten vorhanden."
                )
                rank_embed.add_field(name="how i get xp?", value="You get XP when you write messages")
                rank_embed.set_thumbnail(url=ctx.author.display_avatar)
                rank_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=rank_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # Slash command to show the server leaderboard
    @slash_command(description="shows the server leaderboard")
    async def leaderboard(self, ctx):
        try:
            range_num = 10
            guild_id = ctx.guild.id

            # Get top N users from the database and create an embed
            self.cursor.execute('''
                SELECT user_id, level FROM levels WHERE guild_id = ? ORDER BY level DESC
            ''', (guild_id,))

            rows = self.cursor.fetchmany(range_num)
            leaderboard_embed = discord.Embed(
                title=f'{ctx.guild.name} Leaderboard',
                color=discord.Color.gold()
            )

            # Add fields to the embed for each user in the top N
            for rank, row in enumerate(rows, start=1):
                user_id, level = row
                member = ctx.guild.get_member(user_id)
                leaderboard_embed.add_field(
                    name=f'{rank}. {member.display_name}' if member else f'{rank}. User Left',
                    value=f'Level {level}',
                    inline=False
                )
                leaderboard_embed.set_thumbnail(url=ctx.guild.icon)
                leaderboard_embed.set_footer(text=f"Embed created from {self.bot.user}")

            # Respond with the leaderboard embed
            await ctx.respond(embed=leaderboard_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # Slash command to reset the rank and associated roles of a user (requires ban_members permission)
    @slash_command(description="reset's your rank and rank roles")
    @commands.has_permissions(ban_members=True)
    async def rank_reset(self, ctx, user: Optional[discord.Member]):
        try:
            member = user or ctx.author

            # Remove assigned roles
            for role_name in level_roles:
                role = discord.utils.get(member.guild.roles, name=role_name)
                if role is not None:
                    await role.delete()

            # Delete user's data from the database
            self.cursor.execute('''
                DELETE FROM levels WHERE guild_id = ? AND user_id = ?
            ''', (ctx.guild.id, member.id))

            # Commit changes to the database
            self.conn.commit()

            # Respond with a confirmation embed
            rank_reset_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{member.mention}'s data and associated roles have been reset."
            )
            rank_reset_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=rank_reset_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started


def setup(bot):
    bot.add_cog(Levelsys(bot))
