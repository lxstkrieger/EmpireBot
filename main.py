import discord
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import yaml
import ezcord
# Load environment variables from .env file
load_dotenv()

# Set up Discord Intents with all flags enabled
intents = discord.Intents.all()

# Retrieve debug guilds from environment variable and convert them to a list of integers
debug_guilds_env = os.environ.get('DEBUG_GUILDS', '')
debug_guilds = [int(guild_id) for guild_id in debug_guilds_env.split(',') if guild_id]


# Create a Discord Bot instance with specified intents and debug guilds
bot = ezcord.Bot(intents=intents, debug_guilds=debug_guilds)

with open(os.path.abspath("languages/commands.yaml"), encoding="utf-8") as file:
    commands = yaml.safe_load(file)
    print(commands)





# Configure logging with a rotating file handler
log_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_folder_path = '/etc/logs/'
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

file_handler = RotatingFileHandler(log_folder_path + 'bot.log', encoding='utf-8', maxBytes=5 * 1024 * 1024, backupCount=2)
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
    bot.load_cogs(subdirectories=True)
    bot.run(os.getenv("TOKEN"))


# Run the bot with the specified token from the environment variable

