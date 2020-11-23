import os
import json
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

def readAssociationFile():
	with open('repos.json', 'r') as f:
		reposDict = json.load(f)
	return reposDict

def updateAssociationFile(channel, repoName):
	reposDict = readAssociationFile()
	newRepo = {channel: repoName}
	reposDict.update(newRepo)
	with open('repos.json', 'w') as json_file:
		json.dump(reposDict, json_file)



async def check_association(ctx):
	reposDict = readAssociationFile()
	channel = str(ctx.message.channel.id)
	if channel in reposDict:
		repo= git.get_repo(reposDict[channel])
	else:
		await ctx.send("You have to specify a repository or associate one to this channel.")
	return repo

@bot.command(brief="associate a repo to this channel")
async def associate(ctx, repoName): #!git associate repo
	guild = ctx.message.guild.name
	channel = str(ctx.message.channel.id)
	updateAssociationFile(channel, repoName)
	await ctx.send('We associated repo '+repoName+' with channel '+ctx.message.channel.name+'\n')


@bot.command()
async def hello(ctx): #!git hello
	await ctx.send('Hi there '+ctx.message.author.name)

#TODO: make repoName argument optional 
@bot.command(brief="brief summary of repo")
async def summary(ctx, repoName=None):  #!git summary MLH-Fellowship/github-discord-bot
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	pulls = repo.get_pulls(state='open', sort='created').totalCount
	issues = repo.get_issues(state='open').totalCount - pulls
	contributors = repo.get_contributors().totalCount
	about=''
	if repo.description:
		about = repo.description[:100] #max 100 chars
	text = "\n".join(filter(None,
		[
		"Repo: "+repo.name,
		"About: "+about,
		"Stars: "+str(repo.stargazers_count), 
		"Contributors: "+str(contributors), 
		"Open issues: "+ str(issues),
		"Open pull requests: "+str(pulls)
		]))
	await ctx.send(text)


@bot.command(aliases=['new_repo'], brief='creates a new repo')
async def create_repo(ctx, repoName): #!git create_repo repo1
	repo = user.create_repo(repoName)
	await ctx.send("repository "+repoName+ " created!\n"+'Link: https://github.com/'+user.login+'/'+repoName)


@bot.command(brief='creates a new branch')
async def create_branch(ctx, repoName, sourceBranch, targetBranch): #!git create_branch ddd123-collab/repository1 main branch2
	repo = git.get_repo(repoName)
	source = repo.get_branch(sourceBranch)
	repo.create_git_ref(ref=f"refs/heads/{targetBranch}", sha=source.commit.sha)
	await ctx.send("branch "+targetBranch+" created!\n"+'Link: https://github.com/'+repoName+'/tree/'+targetBranch)

# display open and closed issues

@bot.command(brief='displays issues')
async def issues(ctx, repoName=None, state='open'): # !git issues MLH-Fellowship/github-discord-bot open
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	issues = repo.get_issues(state=state)
	if(issues.totalCount == 0):
		await ctx.send("There are no issues that match your query")
	else: 
		for i in issues:
			await ctx.send('Issue Title: ' + i.title + '\nIssue Number: ' + str(i.number) +'\nIssue Link: https://github.com/' + repo.name + '/issues/' + str(i.number))

@bot.command(brief='displays recent issues')
async def recent_issues(ctx, repoName=None, state='open'): # !git recent_issues MLH-Fellowship/github-discord-bot open
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	issues = repo.get_issues(state=state)
	if(issues.totalCount == 0):
		await ctx.send("There are no issues that match your query")
	else:
		if issues.totalCount > 5:
			issues = issues[:5]
		for i in issues:
			await ctx.send('Issue Title: ' + i.title + '\nIssue Number: ' + str(i.number) +'\nIssue Link: http

# display individual issue
@bot.command()
async def issue(ctx, repoName, number): # !git issue MLH-Fellowship/github-discord-bot 15
	repo = g.get_repo(repoName)
	issue = repo.get_issue(number=int(number))
	await ctx.send('Issue Title: ' + issue.title + '\nIssue Number: ' + str(issue.number) +'\nIssue Link: https://github.com/' + repoName + '/issues/' + str(issue.number))

# display open pull requests

@bot.command(brief='displays pull requests')
async def pull_requests(ctx,repoName=None, state='open'): # !git pull_requests MLH-Fellowship/github-discord-bot open
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	pulls = repo.get_pulls(state=state, sort='created')
	if(pulls.totalCount == 0):
		await ctx.send("There are no pull requests that match your query")
	else:
		for pr in pulls:
			await ctx.send('Pull Request Title: ' + pr.title + '\nPull Request Number: ' + str(pr.number) +'\nPull Request Link: https://github.com/' + repo.name + '/pull/' + str(pr.number))


# display individual PRs
@bot.command()
async def pull_request(ctx, repoName, number): # !git issues MLH-Fellowship/github-discord-bot open
	repo = g.get_repo(repoName)
	pull = repo.get_pull(number=int(number))
	await ctx.send('Pull Request Title: ' + pull.title + '\nPull Request Number: ' + str(pull.number) +'\nPull Request Link: https://github.com/' + repoName + '/pull/' + str(pull.number))

# create issue with assignee

@bot.command(brief='creates issue with assignee')
async def create_issue(ctx, repoName=None,title='title', username=''): # !git create_issue MLH-Fellowship/github-discord-bot issue_title Laurell876
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	created_issue = repo.create_issue(title=title, assignee=username)
	await ctx.send('Issue Title: ' + created_issue.title + '\nIssue Number: ' + str(created_issue.number) +'\nIssue Link: https://github.com/' + repo.name+ '/issues/' + str(created_issue.number))



bot.run(DISCORD_TOKEN)