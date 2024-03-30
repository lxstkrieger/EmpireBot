import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.pages import Paginator, Page
import ezcord
import logging

# Define a Discord cog for handling help-related commands
class Help(ezcord.Cog):
    # Listener that runs when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # Command for displaying help information using a paginated embed
    @slash_command(description="help command")
    async def help(self, ctx):
        try:
            # Define pages for the help command, each page containing information about specific command categories
            my_pages = [
                Page(
                    embeds=[
                        discord.Embed(
                            title="Moderation commands",
                            color=discord.Color.magenta(),
                        ).add_field(name="kick command", value=" kick's a User  ``` /kick <@Member>```", inline=False)
                        .add_field(name="ban command", value=" ban's a User  ``` /ban <@Member>```", inline=False)
                        .add_field(name="bans command", value=" shows banned Users  ``` /bans```", inline=False)
                        .add_field(name="unban command", value=" unban's a User  ``` /unban <@Member> or <MemberID>```", inline=False)
                        .add_field(name="timeout command", value=" timeout's a User  ``` /timeout <@Member> <Duration in Seconds>```", inline=False)
                        .set_thumbnail(url=ctx.guild.icon)
                        .set_footer(text=f"Embed created from {self.bot.user}")
                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="Warnsystem Commands",
                                      color=discord.Color.magenta(),
                                      description="Moderator Only commands"
                                      ).add_field(name="Warn Command", value=" Warn a User  ``` /warn <@Member>```", inline=False)
                                       .add_field(name="Warnings Command", value=" Shows Warns from a Specific User  ``` /warnings <@Member>```", inline=False)
                                       .add_field(name="Unwarn Command", value=" Unwarn's a Specific User(delete last given warn)  ``` /unwarn <@Member>```", inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                                       .set_footer(text=f"Embed created from {self.bot.user}")
                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="Fun Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="baka command", value=" A User is a BAKA  ``` /baka <@Member>```", inline=False)
                                       .add_field(name="hug command", value=" Hug a User  ``` /hug <@Member>```", inline=False)
                                       .add_field(name="punch command", value=" Punch a User  ``` /punch <@Member>```", inline=False)
                                       .add_field(name="kiss command", value=" Kiss a User  ``` /kiss <@Member>```", inline=False)
                                       .add_field(name="kitsune command", value=" you are a Kitsune(Fox)  ``` /kiss <@Member>```", inline=False)
                                       .add_field(name="sleep command", value=" You are sleeping  ``` /sleep ```", inline=False)
                                       .add_field(name="slap command", value=" Slap a User  ``` /slap <@Member>```", inline=False)
                                       .add_field(name="tic tac toe command", value=" play tic tac toe with someone  ``` /tic``", inline=False)
                                       .add_field(name="blush command", value=" anyone ist blushing ``` /blush ```", inline=False)
                                       .add_field(name="cry command", value=" you are crying ``` /cry ```",inline=False)
                                       .add_field(name="dance command", value=" you are dancing ``` /dance ```", inline=False)
                                       .add_field(name="lurk command", value=" you lurk ``` /lurk ```", inline=False)
                                       .add_field(name="peck command", value=" you peck someone ``` /peck ```", inline=False)
                                       .add_field(name="poke command", value=" pocke someone ``` /pocke ```", inline=False)
                                       .add_field(name="shoot command", value=" shoot at someone ``` /shoot ```", inline=False)
                                       .add_field(name="shrug command", value=" shrug someone ``` /shrug ```", inline=False)
                                       .add_field(name="smile command", value=" smile ``` /smile ```", inline=False)
                                       .add_field(name="smug command", value=" smug someone ``` /smug ```", inline=False)
                                       .add_field(name="stare command", value=" stare at someone ``` /stare ```", inline=False)
                                       .add_field(name="think command", value=" think about it ``` /think ```", inline=False)
                                       .add_field(name="tickle command", value=" tickle someone ``` /tickle ```", inline=False)
                                       .add_field(name="wave command", value=" wave to someone ``` /wave ```", inline=False)
                                       .add_field(name="wink command", value=" wick to someone ``` /wink ```", inline=False)
                                       .add_field(name="waifu command", value=" sends Waifu Images ``` /wink ```", inline=False)
                                       .add_field(name="yeet command", value=" yeet someone ``` /yeet ```", inline=False)
                                       .add_field(name="memes command", value=" sending Memes ``` /meme ```", inline=False)
                                       .add_field(name="neko command", value=" sending Neko Images ``` /neko ```", inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                                       .set_footer(text=f"Embed created from {self.bot.user}")
                    ],
                ),

                Page(
                    embeds=[
                        discord.Embed(title="Ticketsystem Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="create Ticket command",
                                                  value=" Create a Ticket  ``` /createticket```", inline=False)
                                       .add_field(name="close Ticket command", value=" Close a Ticket(Moderator Only)  ``` /closeticket```", inline=False)
                                       .add_field(name="Setup Ticketsystem command", value=" Setup Ticketsystem(Administrator Only)  ``` /setupticketsystem```", inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                                       .set_footer(text=f"Embed created from {self.bot.user}")

                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="Levelsystem Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="Rank Command", value=" Show's Rank from a User  ``` /rank <@Member>```", inline=False)
                                       .add_field(name="Leaderboard Command", value=" Show's the Server Leaderboard  ``` /leaderboard ```", inline=False)
                                       .add_field(name="Reset Rank Command", value=" Resets the rank and rank role from a specific Member.(MOD ONLY)  ``` /rank_reset ```", inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                                       .set_footer(text=f"Embed created from {self.bot.user}")

                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="TempVoice Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="Lock Voice Command", value=" Locking the Voice Channel  ``` /lock```", inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                                       .set_footer(text=f"Embed created from {self.bot.user}")
                    ],
                ),
            ]

            # Create a paginator and respond with paginated help information
            paginator = Paginator(pages=my_pages)
            await paginator.respond(ctx.interaction, ephemeral=True)

        except Exception as e:
            # Log an error to the bot.log file if there is an exception
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

# Function to set up the cog when the bot is started
def setup(bot: discord.Bot):
    bot.add_cog(Help(bot))
