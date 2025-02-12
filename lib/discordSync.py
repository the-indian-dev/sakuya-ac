import aiohttp
import asyncio
from config import *
from lib.PacketManager.packets.FSNETCMD_TEXTMESSAGE import FSNETCMD_TEXTMESSAGE as txtMsgr
from logging import debug, warning
import re

BOT_TOKEN = DISCORD_TOKEN

# API Base URL
BASE_URL = 'https://discord.com/api/v10'

# Headers for making API requests
HEADERS = {
    'Authorization': f'Bot {BOT_TOKEN}',
    'Content-Type': 'application/json'
}

# Function to send a message to a specific Discord channel
async def discord_send_message(channel_id:int, message:str, santize_message:bool = True):
    """
    Santizes the message of @everyone and @here pings
    and then sends the message to given channel id
    """
    if santize_message : message = re.sub(r'@(?:everyone|here)', '', message)
    url = f'{BASE_URL}/channels/{channel_id}/messages'
    payload = {
        'content': message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=HEADERS) as response:
            if response.status in [200, 201]:
                pass
            else:
                warning(f'Failed to send message. Status Code: {response.status} | {await response.text()}')

# Function to fetch messages from a specific Discord channel

async def discord_fetch_messages(channel_id, last_message_id=None):
    url = f'{BASE_URL}/channels/{channel_id}/messages'
    params = {'limit': 1}
    if last_message_id:
        params['after'] = last_message_id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    warning(f"Failed to fetch messages. Status Code: {response.status} | {await response.text()}")
                    return []
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        warning(f"Network error while fetching messages: {e}")
        return []  # Return empty list to avoid crashing


# Callback function when a new message is detected
def on_new_message(message):
    author = message['author']
    # Skip messages from bots (including this bot itself)
    if author.get('bot'):  # Safely get the 'bot' key (returns None if key does not exist)
        return

    username = author['username']
    content = message['content']
    debug(f'New Discord message from {username}: {content}')

# Asynchronous function to monitor a Discord channel for new messages
async def monitor_channel(channel_id, playerList:list):
    last_message_id = None
    while True:
        # Fetch new messages
        messages = await discord_fetch_messages(channel_id, last_message_id)
        if messages:
            # Process only the latest message
            message = messages[0]
            if messages:
                message = messages[0]
                if last_message_id is None or message['id'] > last_message_id:  # Ensure only newer messages are processed
                    last_message_id = message['id']
                    if not message['author'].get('bot'): # Skip messages from bot
                        encoded_msg = txtMsgr.encode(f"[Discord] {message['author']['username']}: {message['content']}", True)
                        for player in playerList:
                            if player.streamWriterObject.is_closing():
                                if not player.is_a_bot:
                                    asyncio.create_task(discord_send_message(channel_id, f"{player.username} has left the server!"))
                                playerList.remove(player)  # Remove disconnected players
                                continue
                            player.streamWriterObject.write(encoded_msg)
                            await player.streamWriterObject.drain()
                        on_new_message(message)
        await asyncio.sleep(1)  # Poll every second (adjust as needed)
