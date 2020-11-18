import os
from github import Github
from pprint import pprint
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
git = Github(GITHUB_TOKEN)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!git ')

user = git.get_user()

@bot.command()
async def hello(ctx): #!git hello
	await ctx.send('Hi there '+ctx.message.author.name)


@bot.command(brief="brief summary of repo: number of issues, prs, stars, etc. Args: repoName")
async def summary(ctx, repoName): 
	repo = git.get_repo(repoName)
	pulls = repo.get_pulls(state='open', sort='created').totalCount
	issues = repo.get_issues(state='open').totalCount - pulls
	contributors = repo.get_contributors().totalCount
	stargazers = [ s for s in repo.get_stargazers() ]
	await ctx.send(
		"Stars: "+str(len(stargazers)) + '\n'
		"Contributors: "+str(contributors) + '\n'
		"Open issues: "+ str(issues)+'\n'+
		"Open pull requests: "+str(pulls)+'\n'
		
	)


@bot.command(aliases=['new_repo'], brief='creates a new repository. Args: repoName')
async def create_repo(ctx, repoName): #!git create_repo repo1
	repo = user.create_repo(repoName)
	await ctx.send("repository "+repoName+ " created!\n"+'Link: https://github.com/'+user.login+'/'+repoName)


@bot.command(brief='creates a new branch. Args: repoName sourceBranch targetBranch')
async def create_branch(ctx, repoName, sourceBranch, targetBranch): #!git create_branch ddd123-collab/repository1 main branch2
	repo = git.get_repo(repoName)
	source = repo.get_branch(sourceBranch)
	repo.create_git_ref(ref=f"refs/heads/{targetBranch}", sha=source.commit.sha)
	await ctx.send("branch "+targetBranch+" created!\n"+'Link: https://github.com/'+repoName+'/tree/'+targetBranch)

# display open and closed issues

@bot.command(brief='displays open and closed issues. Args: repoName state')
async def issues(ctx, repoName, state): # !git issues MLH-Fellowship/github-discord-bot open
	repo = git.get_repo(repoName)
	issues = repo.get_issues(state=state)
	if(issues.totalCount == 0):
		await ctx.send("There are no issues that match your query")
	else: 
		for i in issues:
			await ctx.send('Issue Title: ' + i.title + '\nIssue Number: ' + str(i.number) +'\nIssue Link: https://github.com/' + repoName + '/issues/' + str(i.number))


# display open pull requests

@bot.command(brief='displays open pull requests. Args: repoName state')
async def pull_requests(ctx, repoName, state): # !git pull_requests MLH-Fellowship/github-discord-bot open
	repo = git.get_repo(repoName)
	pulls = repo.get_pulls(state=state, sort='created')
	if(pulls.totalCount == 0):
		await ctx.send("There are no pull requests that match your query")
	else:
		for pr in pulls:
			await ctx.send('Pull Request Title: ' + pr.title + '\nPull Request Number: ' + str(pr.number) +'\nPull Request Link: https://github.com/' + repoName + '/pull/' + str(pr.number))


# create issue with assignee

@bot.command(brief='creates issue with assignee. Args: repoName issueTitle username')
async def create_issue(ctx, repoName,title, username): # !git create_issue MLH-Fellowship/github-discord-bot issue_title Laurell876
	repo = git.get_repo(repoName)
	created_issue = repo.create_issue(title=title, assignee=username)
	await ctx.send('Issue Title: ' + created_issue.title + '\nIssue Number: ' + str(created_issue.number) +'\nIssue Link: https://github.com/' + repoName + '/issues/' + str(created_issue.number))



bot.run(DISCORD_TOKEN)