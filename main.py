import discord
import json

BOT_ABOUT = """
```
Written By: Reznok#1688 (Discord)
---------------------------------
ShardBot is a Discord bot built for ShardBound.
Currently in development. For feature requests, ping me on Discord!
```
"""

BOT_HELP = """
```
ShardBot by Reznok#1688 (Discord)
----------------------------------------------------
!sb card_name           | Display A Card
!history user           | Display User Match History
!about                  | Learn about ShardBot!
```
"""

# Commands #

from commands.history import history
from commands.card_lookup import card_lookup

config = json.loads(open('config.json').read())  # Load Configs
client = discord.Client()


def is_admin(author):
    """
    Is this user a bot admin?
    :param author: message.author
    :return: bool
    """
    if str(author).lower() in config["admins"]:
        return True
    return False


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!history'):
        print("History | " + str(message.author) + " | " + message.content)
        await history(client, message)

    if message.content.startswith('!sb'):
        print("Card Lookup | " + str(message.author) + " | " + message.content)
        await card_lookup(client, message)

    if message.content.startswith('!about'):
        print("About | " + str(message.author) + " | " + message.content)
        await client.send_message(message.channel, BOT_ABOUT)

    if message.content.startswith('!help'):
        print("About | " + str(message.author) + " | " + message.content)
        await client.send_message(message.channel, BOT_HELP)

client.run(config["discord_token"])
