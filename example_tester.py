"""
A functional demo of all possible test cases. This is the format you will want to use with your testing bot.
The command below runs it in interactive mode
    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN


To run the bot in cli mode:
usage: example_tester.py [-h] [-c channel]
                     [--run {all,test_reply_matches} | --stats]
                     target_bot_id tester_bot_token
"""


import asyncio
import sys
from distest import TestCollector
from distest import run_interactive_bot, run_dtest_bot
from discord import Embed

# The tests themselves

test_collector = TestCollector()
created_channel = None

# @test_collector()
# async def test_ping(interface):
#     await interface.assert_reply_contains("!git hello", "Hi there lcseville876")


# @test_collector()
# async def test_delayed_reply(interface):
#     message = await interface.send_message(
#         "Say some stuff, but at 4 seconds, say 'yeet'"
#     )
#     await interface.get_delayed_reply(5, interface.assert_message_equals, "yeet")


# @test_collector()
# async def test_reaction(interface):
#     await interface.assert_reaction_equals("React with \u2714 please!", u"\u2714")


# HELLO TEST
@test_collector()
async def test_hello_command(interface):
    await interface.assert_reply_contains("!git hello", "> :wave: Hi there MLH-github-bot")


# SINGLE ISSUE TEST
@test_collector()
async def test_single_issues_command(interface):
    await interface.assert_reply_equals("!git issue MLH-Fellowship/github-discord-bot 15", '> Issue Title: Associate repository to a channel\n > Issue Number: 15\n > Issue Link: https://github.com/github-discord-bot/issues/15')

# SINGLE PULL REQUEST TEST
@test_collector()
async def test_single_pull_request_command(interface):
    await interface.assert_reply_equals("!git pull_request MLH-Fellowship/github-discord-bot 27", '> Pull Request Title: added link to create repository/branch\n > Pull Request Number: 27\n > Pull Request Link: https://github.com/github-discord-bot/pull/27')


# @test_collector()
# async def test_channel_create(interface):
#     await interface.send_message("Create a tc called yeet")
#     created_channel = await interface.assert_guild_channel_created("yeet")


# # @test_collector
# # async def test_pin_in_channel(interface):
# #     await interface.send_message("Pin 'this is cool' in yeet")
# #     await interface.assert_guild_channel_pin_content_equals(created_channel )


# @test_collector()
# async def test_channel_delete(interface):
#     await interface.send_message("Delete that TC bro!")
#     await interface.assert_guild_channel_deleted("yeet")


# @test_collector()
# async def test_silence(interface):
#     await interface.send_message("Shhhhh...")
#     await interface.ensure_silence()


# @test_collector()
# async def test_reply_contains(interface):
#     await interface.assert_reply_contains(
#         "Say something containing 'gamer' please!", "gamer"
#     )


# @test_collector()
# async def test_reply_matches(interface):
#     await interface.assert_reply_matches(
#         "Say something matching the regex `[0-9]{1,3}`", r"[0-9]{1,3}"
#     )


# @test_collector()
# async def test_ask_human(interface):
#     await interface.ask_human("Click the Check!")


# @test_collector()
# async def test_embed_matches(interface):
#     embed = (
#         Embed(
#             title="This is a test!",
#             description="Descriptive",
#             url="http://www.example.com",
#             color=0x00FFCC,
#         )
#             .set_author(name="Author")
#             .set_thumbnail(
#             url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
#         )
#             .set_image(
#             url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
#         )
#     )

#     # This image is in WikiMedia Public Domain
#     await interface.assert_reply_embed_equals("Test the Embed!", embed)


# @test_collector()
# async def test_embed_part_matches(interface):
#     embed = Embed(title="Testing Title.", description="Wrong Description")
#     await interface.assert_reply_embed_equals(
#         "Test the Part Embed!", embed, attributes_to_check=["title"]
#     )


# @test_collector()
# async def test_reply_has_image(interface):
#     await interface.assert_reply_has_image("Post something with an image!")


# @test_collector()
# async def test_reply_on_edit(interface):
#     message = await interface.send_message("Say 'Yeah, that cool!'")
#     await asyncio.sleep(1)
#     await interface.edit_message(message, "Say 'Yeah, that is cool!'")
#     await interface.assert_message_contains(message, "Yeah, that is cool!")


# @test_collector()
# async def test_send_message_in_channel(interface):
#     message = await interface.send_message("Say stuff in another channel")
#     await interface.wait_for_message_in_channel("here is a message in another channel", 694397509958893640)


# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)