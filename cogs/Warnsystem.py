# Import necessary modules for Discord API, extension library, SQLite, and logging
import discord
from discord.ext import commands
from discord.commands import slash_command
import sqlite3
import os
import logging

# Define WarnSystem as a Discord cog for handling warning commands


class WarnSystem(commands.Cog):
    def __init__(self, bot):
        # Initialize the cog with necessary attributes
        self.bot = bot
        self.DB_path = os.path.abspath(os.getenv("DATABASE_PATH", "databases"))
        db_file = os.path.join(self.DB_path, 'Warnsystem.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    # Listener that runs when the bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Function to create the SQLite table for warnings
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            guild_id INTEGER,
                            user_id INTEGER,
                            reason TEXT)''')
        self.conn.commit()

    # Function to add a warning to the database
    def add_warning(self, guild_id, user_id, reason):
        self.cursor.execute("INSERT INTO warnings VALUES (?, ?, ?)", (guild_id, user_id, reason))
        self.conn.commit()

    # Function to get all warnings for a specific user
    def get_warnings(self, guild_id, user_id):
        self.cursor.execute("SELECT reason FROM warnings WHERE guild_id=? AND user_id=?", (guild_id, user_id))
        return self.cursor.fetchall()

    # Function to remove the last warning for a specific user
    def remove_last_warning(self, guild_id, user_id):
        self.cursor.execute("""
            DELETE FROM warnings
            WHERE rowid IN (
                SELECT rowid
                FROM warnings
                WHERE guild_id=? AND user_id=?
                ORDER BY rowid DESC
                LIMIT 1
            )
        """, (guild_id, user_id))
        self.conn.commit()

    # Slash command to warn a user
    @slash_command(description='Warn a user')
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        try:
            # Add warning to the database and respond with an embed
            self.add_warning(ctx.guild.id, member.id, reason)
            warn_embed = discord.Embed(color=discord.Color.red(), description=f"{member.mention} has been warned for: {reason}")
            warn_embed.set_thumbnail(url=member.display_avatar)
            warn_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=warn_embed, ephemeral=True)
        except Exception as e:
            # Log any errors that occur during the warn command
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # Slash command to show warnings for a specific user
    @slash_command(description="Show warnings for a specific user")
    async def warnings(self, ctx, member: discord.Member):
        try:
            # Get warnings from the database and respond with an embed
            warns = self.get_warnings(ctx.guild.id, member.id)
            if warns:
                formatted_warns = [f"{idx + 1}. {warn[0]}" for idx, warn in enumerate(warns)]
                warnings_embed = discord.Embed(color=discord.Color.blue(),
                                               description=f"{member.mention} has the following warnings:\n" + "\n".join(formatted_warns))
                warnings_embed.set_thumbnail(url=member.display_avatar)
                warnings_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=warnings_embed, ephemeral=True)
            else:
                no_warnings_embed = discord.Embed(
                    color=discord.Color.green(),
                    description=f"{member.mention} has no warnings.")
                no_warnings_embed.set_thumbnail(url=member.display_avatar)
                no_warnings_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=no_warnings_embed, ephemeral=True)
        except Exception as e:
            # Log any errors that occur during the warnings command
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # Slash command to remove the last warning for a specific user
    @slash_command(description='Remove the last warning for a specific user')
    @commands.has_permissions(ban_members=True)
    async def removewarn(self, ctx, member: discord.Member):
        try:
            # Remove the last warning and respond with an embed
            self.remove_last_warning(ctx.guild.id, member.id)
            remove_warn_embed = discord.Embed(
                color=discord.Color.green(),
                description=f"The last warning for {member.mention} has been removed."
            )
            remove_warn_embed.set_thumbnail(url=member.display_avatar)
            remove_warn_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=remove_warn_embed, ephemeral=True)
        except Exception as e:
            # Log any errors that occur during the removewarn command
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    # Function to close the connection when the cog is unloaded
    def cog_unload(self):
        self.conn.close()

# Function to set up the WarnSystem cog when the bot is started


def setup(bot):
    bot.add_cog(WarnSystem(bot))
