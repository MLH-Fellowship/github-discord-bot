# github-discord-bot

## discord bot that interacts with Github API
- create repositories for teams
- create branches
- assigning people
- linking pull requests
- announcing merged pull reqs!



# Running Tests

Because of the package being used to run tests a separate bot had to be used as a target bot for the tests instead of the main bot.
This is due to the fact that the main bot uses the @bot.command annotation but the testing package is only compatible with the 
@client.event annotation

- run target bot for testing: python example_target.py $discord_target_bot_token
- run test bot: python example_tester.py $clientId $discord_test_bot_token -c $channelId --run all
