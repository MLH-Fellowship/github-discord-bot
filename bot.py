import os
from github import Github
from pprint import pprint
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!git ')

# get current user

user = g.get_user()
print(user.name) 

# for repo in user.get_repos():
#     print(repo.name)


@bot.command()
async def hello(ctx): #!git hello
	await ctx.send('Hi there '+ctx.message.author.name)

@bot.command()
async def create_repo(ctx, repoName): #!git create_repo repo1
	repo = user.create_repo(repoName)
	await ctx.send("repository "+repoName+ " created!")


# display open and closed issues
@bot.command()
async def issues(ctx, repoName, state): # !git issues MLH-Fellowship/github-discord-bot open/closed
	print(state)
	repo = g.get_repo(repoName)
	issues = repo.get_issues(state=state)
	for i in issues:
		await ctx.send('Issue Title: ' + i.title + '\nIssue Number: ' + str(i.number))


bot.run(DISCORD_TOKEN)