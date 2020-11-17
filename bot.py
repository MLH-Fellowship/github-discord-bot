import os
from github import Github
from pprint import pprint
import discord
from discord.ext import commands
from dotenv import load_dotenv
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

g = Github(GITHUB_TOKEN)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

# get current user
user = g.get_user("Laurell876")
print(user.name)
#repo = g.get_repo("MartinHeinz/python-project-blueprint")

#for repo in g.get_user().get_repos():
#    print(repo.name)

@bot.command(name='git')
async def test(ctx):
	response = 'hey dirtbag'
	await ctx.send(response)

#discord.Client()

'''
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("hey dirtbag")
'''
bot.run(DISCORD_TOKEN)