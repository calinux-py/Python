import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks

#discord bot api
TOKEN = 'YOUR DISCORD API'
CHANNEL_ID = 1155345464741331055  # discord channel id
URL = "https://www.battlemetrics.com/servers/7dtd/22746546?playerCount=RT" #url to extract data from

intents = discord.Intents.default()
client = discord.Client(intents=intents)

#what to extract
def get_server_info():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        player_count_text = soup.find(string="Player count").find_next().text.strip()
        player_count_numeric = int(player_count_text.split('/')[0])
        uptime_text = soup.find(string="Current server time").find_next().text.strip()
        world_age_text = soup.find(string="World age").find_next().text.strip()
        return player_count_numeric, uptime_text, world_age_text
    except (requests.RequestException, ValueError, requests.HTTPError) as e:
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
                try:
                    day = int(uptime.split(',')[0].split(' ')[1])
                    day += 1  # add +1 to day
                except (IndexError, ValueError):
                    day = None
                await channel.send("**-----------------------------------------**")
                await channel.send("7 Days to Die -- PoBx Server 3")
                await channel.send(f"\n```powershell\n-[ Players     ]: [{player_count}]```")
                await channel.send(
                    f"```powershell\n-[ Day/Time    ]: [{uptime.split(',')[0].split(' ')[0]} {day},{uptime.split(',')[1]}]```")
                await channel.send(f"```powershell\n-[ World Age   ]: [{world_age}]```")

                if day is not None:
                    if day % 7 == 0:
                        await channel.send(f"```powershell\n-[HORDE NIGHT! BE PREPARED!]```")
                    else:
                        days_until_horde = 7 - (day % 7)
                        await channel.send(f"```powershell\n-[ Horde Night ]: [{days_until_horde} Days]```")

                await channel.send("**-----------------------------------------**")
            first_run = False
        last_player_count = player_count


@client.event
async def on_ready():
    print(f'{client.user} is home!')
    send_server_info.start()


last_player_count = None
first_run = True
client.run(TOKEN)
