from discord.ext import commands
import diceRolls
import character_manager
import asyncio
client = commands.Bot(command_prefix ='!')


#EXAMPLE COMMANDS
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.command()
async def passed(ctx):
    await ctx.send('Test passed')
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


#DICE ROLLS
@client.command()
async def coin(ctx):
    message = ctx.message.author.mention + diceRolls.coin()
    await ctx.send(message)
@client.command()
async def d4(ctx):
    message = ctx.message.author.mention + diceRolls.d4()
    await ctx.send(message)
@client.command()
async def d6(ctx):
    message = ctx.message.author.mention + diceRolls.d6()
    await ctx.send(message)
@client.command()
async def d8(ctx):
    message = ctx.message.author.mention + diceRolls.d8()
    await ctx.send(message)
@client.command()
async def d10(ctx):
    message = ctx.message.author.mention + diceRolls.d10()
    await ctx.send(message)
@client.command()
async def d12(ctx):
    message = ctx.message.author.mention + diceRolls.d12()
    await ctx.send(message)
@client.command()
async def d20(ctx):
    message = ctx.message.author.mention + diceRolls.d20()
    await ctx.send(message)
@client.command()
async def d100(ctx):
    message = ctx.message.author.mention + diceRolls.d100()
    await ctx.send(message)


#GAME MANAGEMENT
loaded_characters = {}
loaded_spells = {}
loaded_items = {}
creatingCharacter = False
@client.command(aliases=["loadC"])
async def loadCharacter(ctx):
    loaded_characters[ctx.message.author] = character_manager.LoadPlayerData(ctx.message.author)
    await ctx.send(ctx.message.author.mention + ", your character " +
                   loaded_characters[ctx.message.author].name + "is ready for adventure!")
@client.command(aliases = ["saveC"])
async def saveCharacter(ctx):
    character_manager.SavePlayerData(loaded_characters[ctx.message.author])
    del(loaded_characters[ctx.message.ctx.message.author])
    await ctx.send(ctx.message.author.mention + ", your character has been saved!")
@client.command(aliases = ["delC"])
async def deleteCharacter(ctx):
    character_manager.DeletePlayerData(loaded_characters[ctx.ctx.message.author])
    del(loaded_characters[ctx.ctx.message.author])
    await ctx.send(ctx.message.author.mention + ", your character has been deleted. See you on the next adventure!")
@client.command(aliases=["createC"])
async def createCharacter(ctx):
    #TODO: MAKE SURE THAT THIS COMMAND CANNOT BE CAST BY A PERSON WHO ALREADY HAS A CHARACTER ACTIVE
    #TODO: MAKE SURE THAT TYPING "cancel creation" CAN ACTUALLY CANCEL CREATION
    if ctx.message.author in list(loaded_characters.keys()):
        await ctx.send(ctx.message.author.mention + ", you already have a character! (Or in creation of one)")
        return
    loaded_characters[ctx.message.author] = None #Reserving space for no duplicates
    user = None #Done
    name = None #Done
    race = None #Done
    job = None #Done
    level = 1 #Done
    xp = 0 #Done
    xpToLevel = 300 #Done
    stats = None #Done
    proficiencies = None #Done - utilise by checking if a specific proficiency is in this list
    money = None #Done
    equipments = None #Needs item library
    inventory = None #Needs item library
    hitpoints = None #Done
    maxhitpoints = None #Done
    spells = None #Waiting for library

    await ctx.send("Starting character creation for user: " + ctx.message.author.mention + "\nAt any point, say" + " ``cancel creation``")
    user = str(ctx.message.author)
    def check(m):
        return m.author == ctx.message.author and m.content != "!createC"
    try:
        #NAMING PHASE
        await asyncio.sleep(0.5)
        await ctx.send("This is a story of a hero/heroine who people referred to as: \n(What is the name of your character?)")
        msg = await client.wait_for("message", check=check, timeout=60)
        name = msg.content
        await asyncio.sleep(0.5)
        await ctx.send("Name: " + name)

        #CHOOSING RACE AND CLASS
        await asyncio.sleep(1)
        await ctx.send("This hero/heroine is born between [    ] parents and grew up to be a [    ]. (Race and Class)")
        await asyncio.sleep(0.5)
        await ctx.send("> **Possible races:**\n> Human\n> Orc\n> Elf\n> Dwarf")
        await ctx.send("> **Possible classes:**\n> Fighter\n> Cleric\n> Ranger\n> Rogue\n> Wizard")
        isCreating = True
        while(isCreating):
            msg = await client.wait_for("message", check=check, timeout=60)
            msg = msg.content.split()
            race = msg[0]
            job = msg[1]
            if (race.lower() in ["human", "orc", "elf", "dwarf"]) and \
               (job.lower() in ["fighter", "cleric", "ranger", "rogue", "wizard"]):
                isCreating = False
            else:
                await asyncio.sleep(0.5)
                await ctx.send("Invalid race or class selected. Please try again")
        await asyncio.sleep(0.5)
        await ctx.send("You are a(n) " + race[0].upper() + race[1:].lower() + " " + job[0].upper() + job[1:].lower() + "!")

        #SETTING NUMERICAL ATTRIBUTES
        await asyncio.sleep(1)
        await ctx.send("You are now going to set your character attributes now. \nThe attributes are: Strength (Str), "
                       "Dexterity (Dex), Constitution (Con), Intelligence (Int), and Luck (Lck).")
        await asyncio.sleep(0.5)
        await ctx.send("For your race " + race + ", you will get " + raceBonusDesc(race))
        await ctx.send("For your class " + job + ", you will get " + classBonusDesc(job))
        await asyncio.sleep(0.5)
        await ctx.send("Your stats will be randomly rolled, although you will have your chance to assign it as you wish!")
        await asyncio.sleep(0.5)
        rolled = rollStats()
        await ctx.send("Your rolls are: " + str(rolled))
        await ctx.send("To assign your attributes as you wish, "
                       "list the numbers in this respective order:\nStr, Dex, Con, Int, Lck")
        setAttrs = True
        while(setAttrs):
            msg = await client.wait_for("message", check=check, timeout=60)
            msg = list(map(int, msg.content.strip(",").split()))
            print(msg)
            if sorted(msg) == sorted(rolled):
                setAttrs = False
                stats = msg
                print(stats)
            else:
                await ctx.send("Could you check your numbers again? It's not lining up")
        addBonus(stats, race, job)
        await ctx.send("Your stat:\n"
                       "Strength: " + str(stats[0]) + "\n" +
                       "Dexterity: " + str(stats[1]) + "\n" +
                       "Constitution: " + str(stats[2]) + "\n" +
                       "Intelligence: " + str(stats[3]) + "\n" +
                       "Luck: " + str(stats[4]))

        #HITPOINTS
        await asyncio.sleep(1)
        await ctx.send("Your HP will be half of your constitution, rounded down, with race dice roll. This can be increased as you level up.")
        hpRoll = diceRolls.d8() if race in ["orc", "dwarf"] else diceRolls.d6()
        await ctx.send("You rolled a " + hpRoll[-1] + "!")
        maxhitpoints = stats[2]//2 + int(hpRoll[-1])
        await ctx.send("Your Max HP is: " + str(maxhitpoints))
        hitpoints = maxhitpoints

        #PROFICIENCIES
        await asyncio.sleep(1)
        await ctx.send("Proficiency are essentially traits that gives your character mastery in using weapons, items, or spells")
        await asyncio.sleep(1)
        await ctx.send("Proficiencies currently in game are: "
                       "\nOne-handed Weapon Mastery" #CONSIDER MAKING THIS INTO A FUNCTION FOR AREA OF EXPANSION
                       "\nTwo-handed Weapon Mastery"
                       "\nRanged Weapon Mastery"
                       "\nMagic Mastery"
                       "\nTrap Handling Mastery"
                       "\nPersuasive Speaking"
                       "\nShield Mastery")
        await ctx.send("For your class " + job + ", you will get " + classBonusDesc(job, 1))
        proficiencies = [x.strip() for x in classBonusDesc(job, 1).split(",")]
        print(proficiencies)

        #MONEY, EQUIPMENTS, AND ITEMS
        money = 50
        equipments = {"helmet":None, "armor":None, "shoes":None, "rightHand":None, "leftHand":None, "rings":None}





    except asyncio.TimeoutError:
        await ctx.send("Timeout: Character creation canceled!")

    except IndexError:
        await ctx.send("Yeah, you messed up your message spacing. Try again?")

def raceBonusDesc(race):
    if race.lower() == "human":
        return "1 additional point in every attribute except luck."
    elif race.lower() == "orc":
        return "3 additional points in strength and 1 in constitution"
    elif race.lower() == "elf":
        return "3 additional points in intelligence and 1 point in luck"
    elif race.lower() == "dwarf":
        return "1 additional point in  strength and intelligence, 2 in constitution"
    else:
        return "- wait, what race did you pick...? Did I allow you?"
def classBonusDesc(job, type=0):
    """
    :param job: Take in a string, this determines the job
    :param type: Take in a number, this determines what the function should search for (default = 0)
    0 = attribute points, 1 = Proficiency, (leave open for future expansion possibility)
    :return:
    """
    if job.lower() == "fighter":
        if type == 0:
            return "1 additional point in strength and dexterity"
        elif type == 1:
            return "One-handed Weapon Mastery, Two-handed Weapon Mastery, Shield Mastery"

    elif job.lower() == "cleric":
        if type == 0:
            return "1 additional point in constitution and intelligence"
        elif type == 1:
            return "One-handed Weapon Mastery, Shield Mastery, Persuasive Speaking"

    elif job.lower() == "ranger":
        if type == 0:
            return "1 additional point in dexterity and constitution"
        elif type == 1:
            return "Ranged Weapon Mastery, Trap Handling, Persuasive Speaking"

    elif job.lower() == "rogue":
        if type == 0:
            return "1 additional point in dexterity and luck"
        elif type == 1:
            return "One-handed Weapon Mastery, Two-handed Weapon Mastery, Trap Handling"

    elif job.lower() == "wizard":
        if type == 0:
            return "1 additional point in constitution and intelligence"
        elif type == 1:
            return "Magic Mastery, Persuasive Speaking"

    else:
        return "- this class doesn't exist? How did this happen?"
def rollStats():
    stats = []
    for i in range(0,5):
        tray = [int(diceRolls.d6()[-1]), int(diceRolls.d6()[-1]), int(diceRolls.d6()[-1]), int(diceRolls.d6()[-1])]
        tray.pop(tray.index(min(tray))) #Roll 4, choose highest 3 and sum
        stats.append(sum(tray))
    print(stats)
    return stats
def addBonus(stats, race, job):
    if race.lower() == "human":
        stats[0] += 1
        stats[1] += 1
        stats[2] += 1
        stats[3] += 1
    elif race.lower() == "orc":
        stats[0] += 3
        stats[2] += 1
    elif race.lower() == "elf":
        stats[3] += 3
        stats[4] += 1
    elif race.lower() == "dwarf":
        stats[0] += 1
        stats[3] += 1
        stats[2] += 2
    else:
        pass
    if job.lower() == "fighter":
        stats[0] += 1
        stats[1] += 1
    elif job.lower() == "cleric":
        stats[2] += 1
        stats[3] += 1
    elif job.lower() == "ranger":
        stats[1] += 1
        stats[2] += 1
    elif job.lower() == "rogue":
        stats[1] += 1
        stats[4] += 1
    elif job.lower() == "wizard":
        stats[2] += 1
        stats[3] += 1
    else:
        pass


#Stupid shit
@client.command()
async def annoy(ctx, message, repeat_num):
    message = str(message)
    repeat_num = int(repeat_num)
    await ctx.send((message + " ") * repeat_num, tts=True)

#Testing some theories
@client.command(aliases = ["CAW"])
async def callAndWait(ctx):
    await ctx.send("Thanks for calling me!")
    num = await sayHi(ctx)
    if num == None:
        await ctx.send("No number was spoken!")
    else:
        await ctx.send(ctx.message.author.mention + " said number " + str(num))


async def sayHi(ctx):
    await asyncio.sleep(1)
    await ctx.send("Please say hi!")
    try:
        msg = await client.wait_for("message", timeout=10)
        await ctx.send(str(msg.author) + " has said " + msg.content + "\nPlease enter a number!")
        msg = await client.wait_for("message")
        return msg.content
    except asyncio.TimeoutError:
        await ctx.send("Time out!")
        return None



client.run('NTU4NDY1NTU0MDIxNzQ0NjQw.Xqu7Rg.LDDTUYl4tznCZwgH-L0aTwYJ-yY')
