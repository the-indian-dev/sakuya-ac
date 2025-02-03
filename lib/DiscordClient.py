import discord
import asyncio
from lib.PacketManager.packets.FSNETCMD_TEXTMESSAGE import FSNETCMD_TEXTMESSAGE
from config import DISCORD_TOKEN, CHANNEL_ID

class DiscordClient(discord.Client):
    
    def __init__(self, intents, parent=None):
        super().__init__(intents=intents)
        self.parent = parent
    
    async def on_ready(self):
        await self.check_messages()
        
    async def on_message(self, message):
        if message.channel.id == CHANNEL_ID:
            if message.author.id == self.user.id:
                return
            author = message.author.name
            content = message.content
            messageToSendToClients = FSNETCMD_TEXTMESSAGE.encode(author, content)
            if self.parent:
                self.parent.send_to_all(messageToSendToClients)
    
    async def send_message(self, message):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            message = await channel.send(message)
    
    async def check_messages(self):
        while True:
            if self.parent:
                for message in self.parent.chatLog:
                    await self.send_message(message)
                    self.parent.chatLog.remove(message)
            await asyncio.sleep(1)
    
    def start_bot(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.check_messages())
        self.run(DISCORD_TOKEN)
        
