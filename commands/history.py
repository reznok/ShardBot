import requests
import json
import datetime

config = json.loads(open('config.json').read())  # Load Configs
BEARER_TOKEN = config["shardbound_token"]
CACHE_TIME = 5  # cache time in minutes

cache = {}


def get_live_data(user):
    headers = {"Authorization": "{0}".format(BEARER_TOKEN),
               "User-Agent": "game=Tactics, engine=UE4, version=4.14.3-0+++UE4+Release-4.14"}
    request = requests.get(
        "https://st-george.spiritwalkgames.com/api/v1/user/history/show/{0}".format(user),
        headers=headers)
    if request.status_code == 200:
        return json.loads(request.text)
    else:
        raise Exception("Could Not Find User")


def check_if_cached(user):
    if user in cache.keys():
        time_difference = datetime.datetime.now() - cache[user]["timestamp"]
        time_difference_in_minutes = time_difference / datetime.timedelta(minutes=1)
        print("Time Difference: %s" % time_difference_in_minutes)
        if time_difference_in_minutes <= CACHE_TIME:
            print("User Is Cached")
            return True
    return False

async def history(client, message):
    WIN = 0
    LOSS = 1
    CONCEDE = 2
    ENEMY_FORFEIT = 3

    user = message.content.split("!history ")[1]
    formatted_user = user.replace("#", "%23").lower()

    print("Looking Up: {0}".format(formatted_user))

    if check_if_cached(formatted_user):
        match_history = cache[formatted_user]["history"]
    else:
        try:
            match_history = get_live_data(formatted_user)
            if len(match_history["games"]) == 0:
                raise Exception
            cache[formatted_user] = {"history": match_history, "timestamp": datetime.datetime.now()}
        except Exception:
            await client.send_message(message.channel, "Could Not Find User: %s" % formatted_user)
            return

    wins = len([game for game in match_history["games"] if game["adjusted_end_condition"] == WIN])
    losses = len([game for game in match_history["games"] if game["adjusted_end_condition"] == LOSS])
    concedes = len([game for game in match_history["games"] if game["adjusted_end_condition"] == CONCEDE])
    enemy_forfeits = len([game for game in match_history["games"] if game["adjusted_end_condition"] == ENEMY_FORFEIT])

    highest_streak = 0
    counter = 0

    for game in match_history["games"]:
        if game["adjusted_end_condition"] == WIN or game["adjusted_end_condition"] == ENEMY_FORFEIT:
            counter += 1
        else:
            if counter > highest_streak:
                highest_streak = counter
            counter = 0

    # Needed for if you didn't lose your very first game
    if counter > highest_streak:
        highest_streak = counter

    formatted_message = "```"
    formatted_message += "{0} | Last Updated: {1} (PST)\n".format(user, cache[formatted_user]["timestamp"].strftime("%Y-%m-%d %H:%M"))
    formatted_message += "--------------------------------------------------------------------------\n"
    formatted_message += "Games Played: {0}\n".format(wins + losses + concedes + enemy_forfeits)
    formatted_message += "Wins: {0} | Losses: {1}\n".format(wins + enemy_forfeits, losses + concedes)
    formatted_message += "Win Rate: {0}\n".format(
        str(int((wins + enemy_forfeits) / (wins + losses + concedes + enemy_forfeits) * 100)) + "%")
    formatted_message += "Highest Win Streak: {0} Games".format(highest_streak)
    formatted_message += "```"
    await client.send_message(message.channel, formatted_message)
    return
