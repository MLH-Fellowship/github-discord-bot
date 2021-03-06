import os
import json
from github import Github
from pprint import pprint
import discord
from discord.ext import commands
from dotenv import load_dotenv
import unittest
from unittest import IsolatedAsyncioTestCase
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
		await ctx.send("> You have to specify a repository or associate one to this channel.")
	return repo

@bot.command(aliases=['set_repo_name', 'repo_name'], brief="associate a repo to this channel")
async def associate(ctx, repoName): #!git associate repo
	guild = ctx.message.guild.name
	channel = str(ctx.message.channel.id)
	updateAssociationFile(channel, repoName)
	await ctx.send('> We associated repo '+repoName+' with channel '+ctx.message.channel.name+'\n')


def generateResponseForHello(ctx):
	return 'Hi there '+ctx.message.author.name

@bot.command(aliases=['hi', 'greetings'])
async def hello(ctx): #!git hello
	await ctx.send('> :wave: Hi there '+ctx.message.author.name)

#TODO: make repoName argument optional 
@bot.command(aliases=['info', 'get_data'], brief="brief summary of repo")
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
	link = 'https://github.com/' + str(repo.owner.login)+'/'+repo.name
	if repo.description:
		about = repo.description[:100] #max 100 chars
	text = "\n".join(filter(None,
		[
		"> **Repo: "+repo.name+"**",
		"> :eyes: About: "+about,
		"> :sparkles: Stars: "+str(repo.stargazers_count), 
		"> :nerd: Contributors: "+str(contributors), 
		"> :tools: Open issues:  "+ str(issues),
		"> :tools: Open pull requests: "+str(pulls),
		"> :heart: Link: "+link
		]))
	await ctx.send(text)


# display open and closed issues

@bot.command(aliases=['show_issues'], brief='displays issues')
async def issues(ctx, max=10, state='open', repoName=None): # !git issues MLH-Fellowship/github-discord-bot open
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	issues = repo.get_issues(state=state)
	if(issues.totalCount == 0):
		await ctx.send("> There are no issues that match your query")
		return
	if issues.totalCount>max:
		issues = issues[:max]
	text=''
	for i in issues:
		await ctx.send('> Issue Title: ' + i.title + '\n > Issue Number: ' + str(i.number) +'\n > Issue Link: https://github.com/' + str(repo.owner.login)+'/'+repo.name + '/issues/' + str(i.number))

# display individual issue
# TODO: refactor command to take in the title of the issue
@bot.command(aliases=['get_issue_by_number'])
async def issue(ctx, number=1, repoName=None): # !git issue MLH-Fellowship/github-discord-bot 15
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	issue = repo.get_issue(number=int(number))
	await ctx.send('> Issue Title: ' + issue.title + '\n > Issue Number: ' + str(issue.number) +'\n > Issue Link: https://github.com/' + str(repo.owner.login)+'/'+repo.name + '/issues/' + str(issue.number))


# GET ISSUE BY TITLE

@bot.command(aliases=['get_issue_by_title'])
async def issue_by_title(ctx, title, state, repoName=None): # !git issue_by_title title state MLH-Fellowship/github-discord-bot
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	issues = repo.get_issues(state=state)
	for issue in issues:
		if issue.title == title:
			await ctx.send('> Issue Title: ' + issue.title + '\n > Issue Number: ' + str(issue.number) +'\n > Issue Link: https://github.com/' + str(repo.owner.login)+'/'+repo.name + '/issues/' + str(issue.number))
			return
	await ctx.send("Issue not found")
	



# display open pull requests

@bot.command(aliases=['pr', 'get_pr', 'get_pr_by_state'], brief='displays pull requests')
async def pull_requests(ctx,max=5, repoName=None, state='open'): # !git pull_requests MLH-Fellowship/github-discord-bot open
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	pulls = repo.get_pulls(state=state, sort='created')
	if(pulls.totalCount == 0):
		await ctx.send("> There are no pull requests that match your query")
		return
	if pulls.totalCount>max:
		pulls = pulls[:max]
	for pr in pulls:
		await ctx.send('> Pull Request Title: ' + pr.title + '\n > Pull Request Number: ' + str(pr.number) +'\n > Issue Link: https://github.com/' + str(repo.owner.login)+'/'+repo.name+ '/pull/' + str(pr.number))


# display individual PRs
@bot.command(aliases=['single_pr', 'pr_by_number'])
async def pull_request(ctx, number=1, repoName=None): # !git pull_request 1 MLH-Fellowship/github-discord-bot
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	try:
		pull = repo.get_pull(number=int(number))
		await ctx.send('> Pull Request Title: ' + pull.title + '\n > Pull Request Number: ' + str(pull.number) +'\n > Issue Link: https://github.com/' + str(repo.owner.login)+'/'+repo.name + '/pull/' + str(pull.number))
	except:
		await ctx.send("Pull request not found")


bot.run(DISCORD_TOKEN)

'''
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


# create issue with assignee
@bot.command(brief='creates issue with assignee')
async def create_issue(ctx, repoName=None,title='title', username=''): # !git create_issue MLH-Fellowship/github-discord-bot issue_title Laurell876
	repo=''
	if repoName:
		repo = git.get_repo(repoName)
	else:
		repo = await check_association(ctx)
	created_issue = repo.create_issue(title=title, assignee=username)
	await ctx.send('> Issue Title: ' + created_issue.title + '\nIssue Number: ' + str(created_issue.number) +'\nIssue Link: https://github.com/' + repo.name+ '/issues/' + str(created_issue.number))
'''
