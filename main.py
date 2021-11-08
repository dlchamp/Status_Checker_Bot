'''
This is a simply bot designed for @Courier :envelope:
As requested, this bot will simply run a status check at 1PM local time every day
If the members' status == the STATUS_MESSAGE variable, a message is sent to the channel
designated by the MESSAGE_CHANNEL variable
'''

import os
import datetime
import nextcord
from nextcord.ext import tasks
from itertools import cycle
from dotenv import load_dotenv

'''
Input the ID of the channel you wish to have messages sent to.
ID must be wrapped in the ' '
Input the status message you wish to check against for member custom status
Must also be wrapped in ' '
Input the time you wish for status check to run in hours:minutes (ex. 1:00) - 24 hour only
'''
GUILD_ID = '778812053980315649'
MESSAGE_CHANNEL = '902733099673202730'
STATUS_MESSAGE = 'discord.gg/wjmVRmjxXC'
TIME = '13:00'


'''
Should never have to adjust anything below this comment line.
'''

intents = nextcord.Intents.all()
bot = nextcord.Client(intents=intents)


def schedule_time(hour, minutes):
    set_time = datetime.time(hour,minutes)
    now = datetime.datetime.now()
    future = datetime.datetime.combine(now, set_time)
    if (future - now).days < 0:
        future = datetime.datetime.combine(now + datetime.timedelta(days=1), set_time)
    return (future - now).total_seconds()


@bot.event
async def on_ready():
    presence_check.start()
    print(f'Bot is online and connected as {bot.user.name} ({bot.user.id})')
    print(f'Connected to...')
    for name in bot.guilds:
        print(name)



@tasks.loop(hours=24)
async def presence_check():

    # Seperate TIME into hours, minutes
    # Sleep until designated time
    hour = TIME.split(":")[0]
    minutes = TIME.split(":")[1]
    await asyncio.sleep(schedule_time(hour,minutes))

    # Get channel from ID in variable
    channel = bot.get_channel(int(MESSAGE_CHANNEL))

    # Iterate through guild members and check their custom status
    # If custom status matches keyword, send message to designated channel
    for guild in bot.guilds:
        if guild.id == int(GUILD_ID):
            for member in guild.members:
                for a in member.activities:
                    if isinstance(a,nextcord.CustomActivity):
                        print(f'{member.name} | {a}')
                        activity = a.name
                        if STATUS_MESSAGE in activity:
                            print('Status match')
                            await channel.send(f'{member.name} needs XP. Status set to our group.')
                        else:
                            print("Status mismatch")




load_dotenv()
bot.run(os.getenv('TOKEN'))