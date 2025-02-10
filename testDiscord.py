from lib.DiscordClient import DiscordClient
import discord

intents = discord.Intents.default()
intents.message_content = True
client = DiscordClient(intents)
client.start_bot()
