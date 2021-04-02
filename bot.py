#region LOGGING SETUP
import logging, os, datetime
now = datetime.datetime.now()
timeFormat = f"{now.hour}_{now.minute} {now.day}-{now.month}-{now.year}"
if not os.path.exists("./logs/"): os.makedirs("./logs/")
open(f"./logs/{timeFormat}.log", 'w')
logging.basicConfig(filename=f"./logs/{timeFormat}.log", encoding='utf-8', level=logging.DEBUG,
    format="[@%(module)s.%(funcName)s   %(levelname)s   %(asctime)s] %(message)s", datefmt="%H:%M:%S")
#endregion

import json, discord, random
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

# import update_commands # update commands on bot startup
# del update_commands

intent = discord.Intents.default()
intent.members = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intent)
slash = SlashCommand(bot)
data = json.load(open('./data.json'))

slash.auto_register = False 
slash.auto_delete = False

if not os.path.exists("./botstorage.json"):
    open('botstorage.json', 'w').write(r"{}")

clientCommands = json.load(open("./commands.json"))

botstorage = json.load(open("./botstorage.json"))

games = [ # EVERY KIRBY GAMES AHAHHAAHAHAH YES
    "Kirby's Dream Land for the Game Boy",
    "Kirby's Adventure for the NES",
    "Kirby's Dream Land 2 for the Game Boy",
    "Kirby Super Star for the SNES",
    "Kirby's Dream Land 3 for the SNES",
    "Kirby 64: The Crystal Shard for the Nintendo 64",
    "Kirby: Squeak Squad for the Nintendo DS",
    "Kirby Returns to Dream Land for the Wii",
    "Kirby: Triple Delux for the Nintendo 3DS",
    "Kirby: Planet Robobot for the Nintendo 3DS",
    "Kirby: Star Allies for the Nintendo Switch",
    "Kirby's Pinball Land for the Game Boy",
    "Kirby's Dream Course for the SNES",
    "Kirby's Block Ball for the Game Boy",
    # "Kirby's Toy Box for the Broadcast Satellaview [Japan Only]",  no longer playable
    "Kirby's Star Stacker for the Game Boy",
    "Kirby Tilt 'n' Tumble for the Game Boy Color",
    "Kirby Air Ride for the GameCube",
    "Kirby Slide for the Game Boy Advance (E-reader)",
    "Kirby: Canvas Curse for the Nintendo DS",
    "Kirby's Epic Yarn for the Wii",
    "Kirby Mass Attack for the Nintendo DS",
    "Kirby Fighters Deluxe for the Nintendo 3DS",
    "Dedede's Drum Dash Deluxe for the Nintendo 3DS",
    "Kirby and the Rainbow Curse for the Wii U",
    "Team Kirby Clash Deluxe for the Nintendo 3DS",
    "Kirby's Blowout Blast for the Nintendo 3DS",
    "Kirby Battle Royale for the Nintendo 3DS ",
    "Super Kirby Clash for the Nintendo Switch",
    "Kirby Fighters 2 for the Nintendo Switch",
]

responses = [ # what the fuck else does kirb say
    "Poyo!",
]

#region functions
def updateStorage():
    json.dump(botstorage, open("./botstorage.json", 'w'))

async def UpdateGuildData(guildID, newData):
    try:
        
        botstorage["guilds"][guildID] = newData

        updateStorage()
        return ("SUCCESS", 0)
    
    except Exception as e:
        await reportError(UpdateGuildData, e, **locals())
        logging.error(f'Failed to update server data for {guildID}\nreason: {e}')
        return ("FAILED", e)


def getDictCommandFromName(name:str):
    for x in clientCommands:
        if x.get("name") is not None:
            if x['name'] == name: return x
        else:
            if x["base"] == name: return x
    
    return

async def reportError(func, error, **variables):
    errorReportChann:discord.TextChannel = bot.get_channel(826563450981056542)
    
    varInfo = ""
    for key in variables.keys():
        varInfo += f"{key} = `{variables[key]}`\n"
    await errorReportChann.send(f"Error in func `{func.__name__}`\n```{error}```\nField Variables:\n{varInfo}")


#endregion
#region events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{random.choice(games)} | v{data['version']}"))
    logging.info(f"{bot.user} is online and usable")

@bot.event
async def on_message(message:discord.Message):

    try:
        if message.author == bot.user or message.author.bot:
            return

        if botstorage["guilds"].get(message.guild.id) is not None:
            for x in botstorage["guilds"][str(message.guild.id)]["words"]:
                if x in message.content:
                    await message.channel.send(random.choice(responses))
                
    except Exception as e:
        await reportError(on_message, e, **locals())


#endregion

#region user commands

#endregion


#region admin commands

@commands.is_owner()
@slash.slash(name="command")
async def _command(ctx:SlashContext):
    pass

#endregion

if __name__ == "__main__":
    bot.run(data['token'])