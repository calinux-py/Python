import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
#discord api token
TOKEN = 'Your discord API'

CHANNEL_ID = 1155345464741331055  # replace with your channel ID

#url we want to extract stuff from
URL = "https://www.battlemetrics.com/servers/7dtd/22746546?playerCount=RT"

intents = discord.Intents.default()
client = discord.Client(intents=intents)


def get_server_info():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        player_count_text = soup.find(string="Player count").find_next().text.strip()
        player_count_numeric = int(player_count_text.split('/')[0])
        uptime_text = soup.find(string="Current server time").find_next().text.strip()
        world_age_text = soup.find(string="World age").find_next().text.strip()

        downtime_history_index = uptime_text.find("Downtime History")
        if downtime_history_index != -1:
            uptime_text = uptime_text[:downtime_history_index].strip()
        return player_count_numeric, uptime_text, world_age_text
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching server information: {e}")
        return None, None, None


@tasks.loop(seconds=90)
async def send_server_info():
    global last_player_count, first_run
    player_count, uptime, world_age = get_server_info()

    if player_count is not None and uptime and world_age:
        if first_run or (last_player_count is not None and player_count != last_player_count):
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                await channel.send("**-----------------------------------------**")
                await channel.send("7 Days to Die -- PoBx Server 3")
                await channel.send(f"\n```powershell\n-[ Players ]: [{player_count}]```")
                await channel.send(f"```powershell\n-[ Time    ]: [{uptime}]```")
                await channel.send(f"```powershell\n-[ Age     ]: [{world_age}]```")
                await channel.send("**-----------------------------------------**")
            first_run = False
        last_player_count = player_count


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    send_server_info.start()


last_player_count = None
first_run = True
client.run(TOKEN)
