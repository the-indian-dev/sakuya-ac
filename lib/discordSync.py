import aiohttp
import asyncio
from config import *
from lib.PacketManager.packets.FSNETCMD_TEXTMESSAGE import FSNETCMD_TEXTMESSAGE as txtMsgr
from logging import debug, warning

BOT_TOKEN = DISCORD_TOKEN

# API Base URL
BASE_URL = 'https://discord.com/api/v10'

# Headers for making API requests
HEADERS = {
    'Authorization': f'Bot {BOT_TOKEN}',
    'Content-Type': 'application/json'
}

# Function to send a message to a specific Discord channel
async def discord_send_message(channel_id, content):
    url = f'{BASE_URL}/channels/{channel_id}/messages'
    payload = {
        'content': content
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=HEADERS) as response:
            if response.status in [200, 201]:
                pass
            else:
                warning(f'Failed to send message. Status Code: {response.status} | {await response.text()}')

# Function to fetch messages from a specific Discord channel
async def discord_fetch_messages(channel_id, last_message_id=None):
    debug("Fetching messages...")  # Debugging
    url = f'{BASE_URL}/channels/{channel_id}/messages'
    params = {'limit': 1}
    if last_message_id:
        params['after'] = last_message_id

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as response:
            if response.status == 200:
                messages = await response.json()
                debug(f"Fetched messages: {messages}")  # Debugging
                return messages
            else:
                print(f"Failed to fetch messages: {response.status} | {await response.text()}")
                return []


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
                                playerList.remove(player)  # Remove disconnected players
                                continue  # Skip this player
                            player.streamWriterObject.write(encoded_msg)
                            await player.streamWriterObject.drain()
                        on_new_message(message)
        await asyncio.sleep(1)  # Poll every second (adjust as needed)
