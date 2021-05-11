#region LOGGING SETUP
import logging, os, datetime
now = datetime.datetime.now()
timeFormat = f"{now.hour}_{now.minute} {now.day}-{now.month}-{now.year}"
if not os.path.exists("./logs/"): os.makedirs("./logs/")
open(f"./logs/{timeFormat}.log", 'w')
logging.basicConfig(filename=f"./logs/{timeFormat}.log", encoding='utf-8', level=logging.DEBUG,
    format="[@%(module)s.%(funcName)s   %(levelname)s   %(asctime)s] %(message)s", datefmt="%H:%M:%S")
#endregion

import json, discord, random, kirbybioparser
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

# import update_commands # update commands on bot startup
# del update_commands

rawGithubHere = "https://raw.githubusercontent.com/megamaz/KirbyBot/master/"
githubHere = "https://github.com/megamaz/KirbyBot/blob/master/"
intent = discord.Intents.default()
intent.members = True
characterList = open("./characters.txt").read().splitlines()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intent)
slash = SlashCommand(bot)
data = json.load(open('./data.json'))
errorCode = 0
kirbyColor = discord.Color.from_rgb(247, 59, 204)
botErrorResponses = {}

# Example:
# {
#    "userID":{
#       "codes":["0xab", "0xcd"],
#       "resolved":False
#   }
# }
#

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

async def reportError(ctx, func, error, **variables):
    global errorCode # cuz I can't fucking modify it otherwise

    await ctx.send(f"Something went wrong!\nYour error code:{hex(errorCode)}\nYou can use **/supportServer** to report the error or **/errorReport**")

    errorReportChann:discord.TextChannel = bot.get_channel(826563450981056542)
    
    varInfo = ""
    for key in variables.keys():
        varInfo += f"{key} = `{variables[key]}`\n"
    await errorReportChann.send(f"Error#{hex(errorCode)}\nError in `{func}`\n```{error}```\nField Variables:\n{varInfo}")

    errorCode += 1

#endregion

#region events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{random.choice(games)} | v{data['version']}"))
    logging.info(f"{bot.user} is online and usable")


#endregion

#region user commands

@slash.subcommand(base="wiki", name="get")
async def wiki(ctx:SlashContext, character):
    try:
        await ctx.defer()
        if character not in characterList:
            possibleMatches = []
            for cl in characterList:
                totalMatch = 0
                for ind in range(len(character)):
                    if ind == len(cl):
                        break
                    if cl[ind] == character[ind]:
                        totalMatch += 1
                
                if totalMatch >= len(character)/2:
                    possibleMatches.append((cl, totalMatch.__int__()))
            
            possibleMatches.sort(key=lambda x: x[1])

            possibleMatches = [x[0] for x in possibleMatches]
            top5 = "\n".join(possibleMatches[:5])
            await ctx.send(embed=discord.Embed(title="Character Could not be found!", description=f"Hmmm... I don't know who that is! Did you mean:\n{top5}", color=kirbyColor)
            )
        else:
            if not os.path.exists(f"./characters/{character}/"):
                await ctx.send("Oh no! It appear I don't have that character in my database...")
            else:
                CharacterData = kirbybioparser.load(f"./characters/{character}/bio.json")
                emb = discord.Embed(title=CharacterData.name, color=kirbyColor).set_thumbnail(url=f"{rawGithubHere}characters/{character}/cover.png")
                emb.add_field(name="First Appearance", value=CharacterData.firstappear, inline=False)
                if CharacterData.quote:
                    emb.add_field(name="Quoted", value=CharacterData.quote, inline=False)
                if CharacterData.char_type:
                    emb.add_field(name="Status", value=', '.join(CharacterData.char_type), inline=False)
                emb.add_field(name="Info", value=CharacterData.bio, inline=False)
                await ctx.send(embed=emb)

    except Exception as e:
        await reportError(func="wiki", error=e, **locals())


@slash.slash(name="contribute")
async def contribute(ctx:SlashContext):
    try:
        await ctx.defer() # bot is thinking...
        await ctx.send("Thank you for your contribution!\nhttps://github.com/megamaz/KirbyBot", hidden=True)
    except Exception as e:
        reportError(func="contribute", error=e, **locals())
#endregion


#region admin commands


#endregion

if __name__ == "__main__":
    bot.run(data['token'])