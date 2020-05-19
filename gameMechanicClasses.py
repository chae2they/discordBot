class Player:

    def __init__(self, user, name, race, job, level, xp, xpToLevel, stats, proficiencies,
                 money, equipments, inventory, hitPoints, maxHitPoints, spells):
        #As of now, I have all these attributes manually handled because
        #This would help when later, creating and loading the .json files

        #This is for using with discord
        self.user = user

        #The basics. This will also influence/determine rest of the stats
        self.name = name
        self.race = race
        self.job = job

        self.level = level
        self.xp = xp
        self.xpToLevel = xpToLevel
        self.stats = stats
        self.proficiencies = proficiencies

        self.money = money
        self.equipments = equipments
        self.inventory = inventory

        self.hitPoints = hitPoints
        self.maxHitPoints = maxHitPoints
        self.spells = spells

    def __str__(self):
        #hp = str("> HP: " + str(self.hitPoints) + "/" + str(self.maxHitPoints))
        printStatement = "> " + self.user + "'s " + self.name + "\n" + \
                         "> Lv." + str(self.level) + " " + self.race + " " + self.job + "\n" + \
                         "> Strength: " + str(self.stats[0]) + "\n" + \
                         "> Dexterity: " + str(self.stats[1]) + "\n" + \
                         "> Constitution: " + str(self.stats[2]) + "\n" + \
                         "> Intelligence: " + str(self.stats[3]) + "\n" + \
                         "> Luck: " + str(self.stats[4]) + "\n\n" #+ hp
                         #"> HP: " + str(self.hitPoints) + "/" + str(self.maxHitPoints)

        return printStatement

    #TODO: ADD GENERAL SKILLS EVERY PLAYER CAN DO (Fleeing, Examining, Persuasion, etc. etc.)


class Spell:

    #TODO: CONSIDER EXPANDING THIS CLASS - INHERIT THEM TO SEVERAL SUBCLASSES OF SPELLS

    def __init__(self, name, desc, level, castTime, necessity, damage, stats):
        self.name = name
        self.desc = desc
        self.level = level
        self.castTime = castTime
        self.necessity = necessity
        self.damage = damage
        self.stats = stats


class Items:

    def __init__(self, name, desc, itemType, stats):
        self.name = name
        self.desc = desc
        self.itemType = itemType
        self.stats = stats

    def __str__(self):
        return "Item: " + self.name + "\nDescription: " + self.desc


class Enemy:

    def __init__(self, name, desc, hp, damage, other):
        self.name = name
        self.desc = desc
        self.hp = hp
        self.damage = damage #Might replace with "attack" in the future and use it as a list or dictionary"
        self.other = other #Other stats that might affect combat

