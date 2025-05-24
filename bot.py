
# This example requires the 'message_content' intent.
import os
import discord
from dotenv import load_dotenv

# Load env file
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
BACKUP_DIR = os.getenv('BACKUP_DIR')
BACKUP_CATEGORY = "backup"
LOG_CHANNEL_NAME = "bot-log"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

log_channel = None

async def log_to_channel(msg):
    if log_channel:
        await log_channel.send(msg)
    else:
        print(f"[LOG]: {msg}")
    

@client.event
async def on_ready():
    global log_channel
    print(f'Logged in as {client.user}')
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == LOG_CHANNEL_NAME:
                log_channel = channel
                print(f"Found log channel: #{LOG_CHANNEL_NAME}")
                return

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # check message is in the backup category
    if not message.channel.category or message.channel.category.name.lower() != "backup":
        return
    channel_name = message.channel.name.lower()

    try:
        if channel_name == 'text':
            await log_to_channel(f"Text found in #text")
        elif channel_name == 'links':
            await log_to_channel(f"Link found in #link") 
        elif channel_name == 'images' and message.attachments:
            await log_to_channel(f"Image found in #images")
        elif channel_name == 'video' and message.attachments:
            await log_to_channel(f"Video found in #video")
        elif channel_name == 'files' and message.attachments:
            await log_to_channel(f"File found in #files")
    except Exception as e:
        print(f"Error processing message: {e}")
# if token isn't found
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN not found in .env file")
client.run(TOKEN)
