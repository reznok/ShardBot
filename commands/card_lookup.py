import requests

async def card_lookup(client, message):
    card = message.content.split("!sb ")[1]
    card = card.replace(" ", "-").lower()
    url = "https://www.shardveil.com/images/cards/placeholder/{0}.png".format(card)
    if requests.get(url).status_code == 200:
        await client.send_message(message.channel, url)
    else:
        await client.send_message(message.channel, "Could Not Find Card")
    return
