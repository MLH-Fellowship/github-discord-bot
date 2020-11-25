"""
This bot is a sample bot that is used to demonstrate the testing functionality.
It does not run the tests, just exists to have tests run on it.
    Run with:
        python example_target.py TARGET_TOKEN
"""
import asyncio
import sys
import os
import discord
from github import Github

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
git = Github(GITHUB_TOKEN)


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


    # Hello Command
    if message.content == "!git hello":
        await asyncio.sleep(1)
        sent = await message.channel.send('> :wave: Hi there ' + str(client.user.name))
    
    # Single issue command
    if message.content == "!git issue MLH-Fellowship/github-discord-bot 15":
        repo = git.get_repo("MLH-Fellowship/github-discord-bot")
        issue = repo.get_issue(number=int(15))
        await message.channel.send('> Issue Title: ' + issue.title + '\n > Issue Number: ' + str(issue.number) +'\n > Issue Link: https://github.com/' + repo.name + '/issues/' + str(issue.number))


    if message.content.startswith("Say something containing 'gamer'"):
        await asyncio.sleep(1)
        sent = await message.channel.send("gamers r00l")
    if message.content.startswith("Post something with an image!"):
        await asyncio.sleep(1)
        sent = await message.channel.send("https://imgs.xkcd.com/comics/ui_vs_ux.png")
    if message.content.startswith("React with"):
        await asyncio.sleep(1)
        sent = await message.add_reaction("\u2714")
    if message.content.startswith("Click the Check!"):
        await asyncio.sleep(1)
        sent = await message.add_reaction("\u2714")
    if message.content.startswith("Test the Embed!"):
        await asyncio.sleep(1)
        embed = discord.Embed(
            title="This is a test!",
            description="Descriptive",
            url="http://www.example.com",
            color=0x00FFCC,
        )
        embed.set_author(name="Author")
        embed.set_image(
            url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
        )
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
        )
        sent = await message.channel.send(embed=embed)
    if message.content.startswith("Test the Part Embed!"):
        await asyncio.sleep(1)
        embed = discord.Embed(title="Testing Title.", description="Right Description!")
        sent = await message.channel.send(embed=embed)
    if message.content.startswith("Say some stuff, but at 4 seconds, say 'yeet'"):
        await asyncio.sleep(1)
        await message.channel.send("hahaha!")
        await message.channel.send("No!")
        await message.channel.send("Ok...")
        await asyncio.sleep(2.5)
        sent = await message.channel.send("yeet")
    if message.content.startswith("Create a tc called yeet"):
        global text_channel_id
        await asyncio.sleep(1)
        text_channel = await message.guild.create_text_channel("yeet")
        text_channel_id = text_channel.id
    if message.content.startswith("Delete that TC bro!"):
        await asyncio.sleep(1)
        text_channel = client.get_channel(text_channel_id)
        await text_channel.delete()
    if sent is not None:
        print("Message sent: {}".format(sent.clean_content))
    if message.content.startswith("Say stuff in another channel"):
        await asyncio.sleep(1)
        await client.get_channel(694397509958893640).send("here is a message in another channel")


@client.event
async def on_message_edit(before, after):
    sent = None
    if after.content.startswith("Say 'Yeah, that is cool!'"):
        await asyncio.sleep(1)
        sent = await after.channel.send("Yeah, that is cool!")
    if sent is not None:
        print("Message sent: {}".format(sent.clean_content))


client.run(sys.argv[1])