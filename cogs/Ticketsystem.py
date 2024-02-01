import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import sqlite3
import os

# Establish a connection to the SQLite database
DB_path = os.path.abspath(os.getenv("DATABASE_PATH", "databases"))
db_file = os.path.join(DB_path, 'Ticketsystem.db')
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Initialize the database table if it does not exist
cursor.execute('''
          CREATE TABLE IF NOT EXISTS ticket_permissions (
              guild_id INTEGER,
              user_id INTEGER,
              support_role_name TEXT,
              channel_id INTEGER
          )
          ''')
conn.commit()


class Ticketsystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Create a new Ticket")
    async def createticket(self, ctx):
        try:
            # Create a new ticket channel
            ticket_channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.display_name}")
            # Set permissions for the user in the ticket channel
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True,
                                                 embed_links=True, attach_files=True, read_message_history=True,
                                                 external_emojis=True)

            # Get the 'Support Team' role
            rolesearch = discord.utils.get(ctx.guild.roles, name="🙋🏻‍♂️Support Team🙋🏻‍♂️")

            if rolesearch:
                # Set permissions for default role, author, and support team role in the ticket channel
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
                    ctx.author: discord.PermissionOverwrite(send_messages=True, read_messages=True),
                    rolesearch: discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True,
                                                            embed_links=True, attach_files=True, read_message_history=True,
                                                            external_emojis=True, manage_channels=True)
                }

                await ticket_channel.edit(overwrites=overwrites)

                # Respond with a message indicating that the ticket channel was created
                await ctx.respond(f"Your Ticket Channel was Created. Here's Your Ticket: {ticket_channel.mention}", ephemeral=True)

                # Save permissions to the database
                cursor.execute('''
                          INSERT INTO ticket_permissions (guild_id, user_id, support_role_name, channel_id)
                          VALUES (?, ?, ?, ?)
                          ''', (ctx.guild.id, ctx.author.id, "🙋🏻‍♂️Support Team🙋🏻‍♂️", ticket_channel.id))
                conn.commit()

            else:
                # Respond with an error if the 'Support Team' role is not found
                await ctx.send("Error: Role '🙋🏻‍♂️Support Team🙋🏻‍♂️' not found. Please create the role before using the ticket system.")

            # Send an initial message to the ticket channel
            embed = discord.Embed(color=0xff8103)
            embed.add_field(name="Support Ticket", value=f"Ticket by {ctx.author.mention}", inline=False)
            embed.add_field(name="Option:", value=":lock: - ```/closeticket - <#ticket>```", inline=False)
            embed.set_footer(text=f"Ticket | {ctx.author}")
            await ticket_channel.send(embed=embed)
            await ticket_channel.send(
                f"Hello, {ctx.author.mention}! Please describe your problem so that a 🙋🏻‍♂️Support Team🙋🏻‍♂️ can help you.")

        except Exception as e:
            # Log any errors that occur during ticket creation
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description="Close a Ticket(Only Team Member can Use This!)")
    async def closeticket(self, ctx):
        try:
            # Check permissions in the database before closing the ticket
            cursor.execute('''
                      SELECT * FROM ticket_permissions
                      WHERE guild_id=? AND (user_id=? OR support_role_name IN (?))
                      AND channel_id=?
                      ''', (ctx.guild.id, ctx.author.id, "🙋🏻‍♂️Support Team🙋🏻‍♂️", ctx.channel.id))
            result = cursor.fetchone()

            if result:
                await ctx.channel.delete()
            else:
                await ctx.send("You don't have the permission to close this ticket.")

        except Exception as e:
            # Log any errors that occur during ticket closure
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description="Setup the Ticketsystem")
    @commands.has_permissions(administrator=True)
    async def setupticketsystem(self, ctx):
        try:
            # Create the 'Support Team' role
            await ctx.guild.create_role(name="🙋🏻‍♂️Support Team🙋🏻‍♂️", colour=discord.Colour(0xE03400))

            # Create an information embed indicating successful installation
            setup_embed = discord.Embed(
                title="Information",
                description="Ticket System was successfully installed. | Attention: If you run `/setupticketsystem` again, the ticket system will no longer work and report an error. Since there are 2 roles of ticket helper, you have to delete one. This code is still in development. For problems/questions, contact me on Discord: Talha2018#0001",
                color=0x00ff00
            )
            setup_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.send(embed=setup_embed)

        except Exception as e:
            # Log any errors that occur during ticket system setup
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(Ticketsystem(bot))
