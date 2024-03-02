import discord
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file
load_dotenv()

# Set up Discord Intents with all flags enabled
intents = discord.Intents.all()

# Retrieve debug guilds from environment variable and convert them to a list of integers
debug_guilds_env = os.environ.get('DEBUG_GUILDS', '')
debug_guilds = [int(guild_id) for guild_id in debug_guilds_env.split(',') if guild_id]

# Create a Discord Bot instance with specified intents and debug guilds
bot = discord.Bot(intents=intents, debug_guilds=debug_guilds)

# Configure logging with a rotating file handler
log_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = RotatingFileHandler('bot.log', maxBytes=5 * 1024 * 1024, backupCount=2)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(file_handler)

# Event handler for when the bot is ready


@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')

# Load all extensions (cogs) from the 'cogs' directory
if __name__ == "__main__":
    for root, dirs, files in os.walk("cogs"):
        for filename in files:
            if filename.endswith(".py"):
                module_name = os.path.join(root, filename)[:-3].replace(os.path.sep, '.')

                # Lade das Cog
                bot.load_extension(module_name)

# Run the bot with the specified token from the environment variable
bot.run(os.getenv("TOKEN"))
