from discord.ext import commands
import diceRolls
import character_manager
import item_and_spell_manager
import gameMechanicClasses
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
loaded_enemies = {}
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
        msg = await client.wait_for("message", check=check, timeout=300)
        name = str(msg.content)
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
            msg = await client.wait_for("message", check=check, timeout=300)
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
            msg = await client.wait_for("message", check=check, timeout=300)
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


        player = gameMechanicClasses.Player(user, name, race, job, level, xp, xpToLevel, stats, proficiencies, money,
                                            equipments, inventory, hitpoints, maxhitpoints, spells)
        loaded_characters[player.name] = player
        character_manager.SavePlayerData(player)
        await ctx.send("Your characther, " + player.name + " has been created and ready for adventure!")

        #MONEY, EQUIPMENTS, AND ITEMS
        money = 50
        equipments = {"helmet":None, "armor":None, "shoes":None, "rightHand":None, "leftHand":None, "rings":None}

        player = gameMechanicClasses.Player(user, name, race, job, level, xp, xpToLevel, stats, proficiencies, money,
                                            equipments, inventory, hitpoints, maxhitpoints, spells)
        loaded_characters[player.name] = player

    except asyncio.TimeoutError:
        await ctx.send("Timeout: Character creation canceled!")
        del(loaded_characters[ctx.message.author])

    except IndexError:
        await ctx.send("Yeah, you messed up your message spacing. Try again?")

@client.command()
async def testChar(ctx, heroName=None):
    await ctx.send(loaded_characters)
    if heroName is not None:
        await ctx.send(loaded_characters[heroName])


@client.command()
async def loadItem(ctx, itemName):
    item = item_and_spell_manager.LoadItem(itemName)
    loaded_items[item.name] = item


@client.command()
async def loadAll(ctx):
    allItems = item_and_spell_manager.LoadAllItems()
    for item in allItems.keys():
        loaded_items[item] = allItems[item]

    allSpells = item_and_spell_manager.LoadAllSpells()
    for spell in allSpells.keys():
        loaded_items[spell] = allSpells[spell]

    allMonsters = character_manager.LoadAllEnemies()
    for monster in allMonsters.keys():
        loaded_enemies[monster] = allMonsters[monster]

    await ctx.send("All your items, spells, and monsters have been added.")



#ALL THE SPELLS AND ITEMS REGISTRATION
@client.command(aliases=["rg"])
async def register(ctx):
    await ctx.send("What are you registering? Spells, Items, or Monsters?")
    def check(m):
        return m.author == ctx.message.author
    try:
        msg = await client.wait_for("message", check=check, timeout=30)
        if msg.content == "item":
            await regItem(ctx)
        elif msg.content == "spell":
            await regSpell(ctx)
            #TODO MAKE SPELL ADDER
        elif msg.content == "monster":
            await regMonster(ctx)
            #TODO MAKE MONSTER ADDER
        elif msg.content == "cancel":
            return
        else:
            pass #TODO FOR FUTURE EXPANSION


    except asyncio.TimeoutError:
        ctx.send("Timeout: Please try again!\nWe recommend you have one written down before you start registration!")

async def regItem(ctx):
    def check(m):
        return m.author == ctx.message.author
    name = None
    desc = None
    itemType = None
    stats = None
    try:
        await ctx.send("Please enter your item name")
        msg = await client.wait_for("message", check=check, timeout=30)
        name = str(msg.content)
        await ctx.send("Item name: " + name + "\nPlease enter your item type. Your choices are:"
                                              "\nWeapon-Bladed"
                                              "\nWeapon-Blunt"
                                              "\nWeapon-Needle"
                                              "\nWeapon-Projectile"
                                              "\nWeapon-Magic"
                                              "\nWeapon-Fists"
                                              "\nConsumable"
                                              "\nArmor-Helmet"
                                              "\nArmor-Body"
                                              "\nArmor-Shoes")

        isTyping = True
        while isTyping:
            msg = await client.wait_for("message", check=check, timeout=30)
            if msg.content in ["Weapon-Bladed", "Weapon-Blunt", "Weapon-Needle", "Weapon-Projectile", "Weapon-Magic",
                               "Weapon-Fists", "Consumable", "Armor-Helmet", "Armor-Body", "Armor-Shoes"]:
                isTyping = False
                itemType = msg.content
                await ctx.send("Item Type: " + itemType)
            else:
                await ctx.send("Please choose a proper item type.")

        await ctx.send("Give a description of your item. This can be anything from its appearance to its function. (Single message, 3 minutes)")
        msg = await client.wait_for("message", check=check, timeout=180)
        desc = msg.content

        await ctx.send("Give your item some attributes."
                       "\nThe format is: [3 lowercase letter code][#d# format dice roll]"
                       "\n(example: dft2d6 is 'Damage From Throw, sum two d6 rolls')"
                       "\nUse space when registering several different attributes to divide them."
                       "\n(example: dft2d6 dfs1d8 is 'Damage From Throw 2d6, Damage From Swing 1d8')"
                       "\nDo this in a single message. See various attribute codes in help.")
        isTyping = True
        while isTyping:
            isTyping = False
            msg = await client.wait_for("message", check=check, timeout=60)
            atr = msg.content.split()
            stats = atr
            for i in atr:
                if len(i)==6 and i[0:2].isalpha() and i[3].isnumeric() and i[4].isalpha() and i[5].isnumeric():
                    pass
                else:
                    isTyping = True
                    await ctx.send("Please try again. Your code format is inappropriate")
                    break

        item = gameMechanicClasses.Items(name, desc, itemType, stats)
        loaded_items[item.name] = item
        item_and_spell_manager.AddItem(item)
        await ctx.send("Your item, " + loaded_items[item.name].name + " has been registered.")

    except asyncio.TimeoutError:
        await ctx.send("Timed out! Please try again!"
                       "\nWe recommend you have one written down before you start registration!")
    def check(m):
        return m.author == ctx.message.author


async def regSpell(ctx):
    def check(m):
        return m.author == ctx.message.author
    name = None
    desc = None
    level = None
    castTime = None
    necessity = None
    damage = None
    stats = None
    try:
        await ctx.send("Please enter your spell name")
        msg = await client.wait_for('message', check=check, timeout=180)
        name = msg.content
        await ctx.send("Please describe the spell")
        msg = await client.wait_for('message', check=check, timeout=300)
        desc = msg.content
        await ctx.send("Please enter your level")
        msg = await client.wait_for('message', check=check, timeout=300)
        level = int(msg.content)
        await ctx.send("Please enter the cast time (number in turns)")
        msg = await client.wait_for('message', check=check, timeout=180)
        castTime = int(msg.content)
        await ctx.send("Choose which components are necessary for your spell: "
                       "\nIndicate in three 0s and 1s:"
                       "\nConcentration (No interruption during cast)"
                       "\nSalt (Think of this as your MP)"
                       "\nStaff, Tome, etc. (This is your required tool)"
                       "\nFor example, if you are registering a spell that takes salt "
                       "and requires concentration during cast, say 110")
        msg = await client.wait_for('message', check=check, timeout=180)
        necessity = [int(i) for i in msg.content]
        await ctx.send("Provide your main damage. Your main damage calculation will be ndx, "
                       "where n is the level and x is chosen here.")
        msg = await client.wait_for('message', check=check, timeout=180)
        damage = int(msg.content)
        await ctx.send("Give your spells attributes/stats."
                       "\nFormat is 3 alphabets, then ndm (to display dice roll)"
                       "\nSee help for item codes.")
        isTyping = True
        while isTyping:
            isTyping = False
            msg = await client.wait_for("message", check=check, timeout=60)
            atr = msg.content.split()
            stats = atr
            for i in atr:
                if len(i)==6 and i[0:2].isalpha() and i[3].isnumeric() and i[4].isalpha() and i[5].isnumeric():
                    pass
                else:
                    isTyping = True
                    await ctx.send("Please try again. Your code format is inappropriate")
                    break

        spell = gameMechanicClasses.Spell(name, desc, level, castTime, necessity, damage, stats)
        loaded_spells[spell.name] = spell
        item_and_spell_manager.AddSpell(spell)
        await ctx.send("Your spell, " + loaded_spells[spell.name].name + " has been registered.")

    except asyncio.TimeoutError:
        await ctx.send("You ran out of time! Try again.")


async def regMonster(ctx):
    def check(m):
        return m.author == ctx.message.author
    name = None
    desc = None
    hp = None
    damage = None
    other = None
    try:
        await ctx.send("Please name your monster")
        msg = await client.wait_for('message', check=check, timeout=180)
        name = msg.content
        await ctx.send("Please give your monster a description")
        msg = await client.wait_for('message', check=check, timeout=300)
        desc = msg.content
        await ctx.send("Set your monster's hit points")
        msg = await client.wait_for('message', check=check, timeout=180)
        hp = int(msg.content)
        await ctx.send("Set your monster's attack (in dice roll style)")
        msg = await client.wait_for('message', check=check, timeout=180)
        damage = msg.content
        await ctx.send("Set your monster's miscellaneous feats"
                       "\nYou should be following the item and spell's stats format (See help)")
        isTyping = True
        while isTyping:
            isTyping = False
            msg = await client.wait_for("message", check=check, timeout=60)
            atr = msg.content.split()
            other = atr
            for i in atr:
                if len(i)==6 and i[0:2].isalpha() and i[3].isnumeric() and i[4].isalpha() and i[5].isnumeric():
                    pass
                else:
                    isTyping = True
                    await ctx.send("Please try again. Your code format is inappropriate")
                    break

        enemy = gameMechanicClasses.Enemy(name, desc, hp, damage, other)
        loaded_enemies[enemy.name] = enemy
        character_manager.SaveEnemy(enemy)
        await ctx.send("Your monster, " + enemy.name + " has been registered")


    except asyncio.TimeoutError:
        await ctx.send("Time out! Please start again")


@client.command()
async def testItem(ctx, itemName=None):
    await ctx.send(loaded_items)
    if itemName is not None:
        await ctx.send(loaded_characters[itemName])



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



client.run('')

