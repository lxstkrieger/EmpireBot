import discord
from discord.ext import commands
import ezcord

# Define a Discord cog for handling temporary voice channels
class TemporaryVoice(ezcord.Cog):
    # Class variables to store temporary channels and categories
    temporary_channels = []
    temporary_categories = []

    # Constructor to initialize the cog with the bot instance
    def __init__(self, bot):
        self.bot = bot

    # Listener that runs when a user's voice state is updated
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # Define a possible channel name based on the member's name
        possible_channel_name = f"{member.name}'s area"

        # Check if the member joined a channel
        if after.channel:
            # Check if the joined channel is named "temp"
            if after.channel.name == "temp":
                # Clone the channel with a personalized name and move the member to it
                temp_channel = await after.channel.clone(name=possible_channel_name)
                await member.move_to(temp_channel)
                # Add the new temporary channel to the list
                self.temporary_channels.append(temp_channel.id)

            # Check if the joined channel is named 'teams'
            if after.channel.name == 'teams':
                # Create a category and associated text and voice channels
                temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
                await temporary_category.create_text_channel(name="text")
                temp_channel = await temporary_category.create_voice_channel(name="voice")
                await member.move_to(temp_channel)
                # Add the new temporary category to the list
                self.temporary_categories.append(temp_channel.id)

        # Check if the member left a channel
        if before.channel:
            # Check if the left channel is a temporary channel
            if before.channel.id in self.temporary_channels:
                # Delete the channel if no members are left in it
                if len(before.channel.members) == 0:
                    await before.channel.delete()

            # Check if the left channel is a temporary category
            if before.channel.id in self.temporary_categories:
                # Delete all channels in the category and then delete the category if no members are left in any channel
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()

# Function to set up the cog when the bot is started


def setup(bot: discord.Bot):
    bot.add_cog(TemporaryVoice(bot))
