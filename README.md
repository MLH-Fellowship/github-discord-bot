# github-discord-bot
**This bot allows you to associate a Github repo to a channel and get quick info, such as summary, recent issues, pull requests, etc**. 
## Commands:
- ``!git hello`` - says hi (to check if the bot is working)
- ``!git associate repoName`` - associate a repo to this channel (that way you don't have to specify it every time). Stored in JSON file. 
- ``!git summary`` - returns the description, number of stars, contributors, issues and prs
- ``!git issues `` - returns a list of issues (title, number, link). You can specify a maximum (the default is 10). 
- ``!git pull_requests`` - returns a list of prs (title, number, link). You can specify a maximum (the default is 5)
- ``!git issue number`` - return the issue info (title, number, link) given its number
- ``!git pull_request number`` - return the pull request info (title, number, link) given its number

## To use the bot on your server:
- simply copy and paste [this](https://discord.com/api/oauth2/authorize?client_id=778012965625921587&permissions=0&scope=bot) in your browser and choose the server that you want the bot to have access to. This bot only has one scope: bot. 

## Running Tests

- Because of the package being used to run tests a separate bot had to be used as a target bot for the tests instead of the main bot.
- This is due to the fact that the main bot uses the @bot.command annotation but the testing package is only compatible with the 
@client.event annotation

- run target bot for testing: ``python example_target.py $discord_target_bot_token``
- run test bot: ``python example_tester.py $clientId $discord_test_bot_token -c $channelId --run all``
