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

    # PULL REQUEST COMMAND
    if message.content.startswith("!git pull_request MLH-Fellowship/github-discord-bot 27"):
        repo=''
        repo = git.get_repo("MLH-Fellowship/github-discord-bot")
        pull = repo.get_pull(number=int(27))
        await message.channel.send('> Pull Request Title: ' + pull.title + '\n > Pull Request Number: ' + str(pull.number) +'\n > Pull Request Link: https://github.com/' + repo.name + '/pull/' + str(pull.number))

client.run(sys.argv[1])