"""
This bot is a sample bot that is used to demonstrate the testing functionality.
It does not run the tests, just exists to have tests run on it.
    Run with:
        python example_target.py TARGET_TOKEN
"""
import asyncio
import sys
import discord


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()


@client.event
async def on_ready():
    print("Ready")


text_channel_id = None


@client.event
async def on_message(message):
    if message.author.id is client.user.id:
        return
    sent = None
    # Hello Test
    if message.content == "ping?":
        await asyncio.sleep(1)
        sent = await message.channel.send("pong!")


client.run(DISCORD_TOKEN)