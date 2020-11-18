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

user = g.get_user()

@bot.command()
async def hello(ctx): #!git hello
	await ctx.send('Hi there '+ctx.message.author.name)

@bot.command()
async def create_repo(ctx, repoName): #!git create_repo repo1
	repo = user.create_repo(repoName)
	await ctx.send("repository "+repoName+ " created!")

# create a new branch

@bot.command()
async def create_branch(ctx, repoName, sourceBranch, targetBranch): #!git create_branch ddd123-collab/repository1 main branch2
	repo = g.get_repo(repoName)
	source = repo.get_branch(sourceBranch)
	repo.create_git_ref(ref=f"refs/heads/{targetBranch}", sha=source.commit.sha)
	await ctx.send("branch "+targetBranch+" created!")

# display open and closed issues
# TODO: add default state
@bot.command()
async def issues(ctx, repoName, state): # !git issues MLH-Fellowship/github-discord-bot open
	repo = g.get_repo(repoName)
	issues = repo.get_issues(state=state)
	if(issues.totalCount == 0):
		await ctx.send("There are no issues that match your query")
	else: 
		for i in issues:
			await ctx.send('Issue Title: ' + i.title + '\nIssue Number: ' + str(i.number) +'\nIssue Link: https://github.com/' + repoName + '/issues/' + str(i.number))


# display open pull requests

@bot.command()
async def pull_requests(ctx, repoName, state): # !git pull_requests MLH-Fellowship/github-discord-bot open
	repo = g.get_repo(repoName)
	pulls = repo.get_pulls(state=state, sort='created')
	if(pulls.totalCount == 0):
		await ctx.send("There are no pull requests that match your query")
	else:
		for pr in pulls:
			await ctx.send('Pull Request Title: ' + pr.title + '\nPull Request Number: ' + str(pr.number) +'\nPull Request Link: https://github.com/' + repoName + '/pull/' + str(pr.number))


# create issue with assignee

@bot.command()
async def create_issue(ctx, repoName,title, username): # !git create_issue MLH-Fellowship/github-discord-bot issue_title Laurell876
	repo = g.get_repo(repoName)
	created_issue = repo.create_issue(title=title, assignee=username)
	await ctx.send('Issue Title: ' + created_issue.title + '\nIssue Number: ' + str(created_issue.number) +'\nIssue Link: https://github.com/' + repoName + '/issues/' + str(created_issue.number))



bot.run(DISCORD_TOKEN)