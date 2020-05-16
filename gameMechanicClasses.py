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
        printStatement = "> "+ self.user + "'s " + self.name + + "\n" + \
                         "> Lv." + self.level + " " + self.race + " " + self.job + "\n" + \
                         "> Strength: " + self.stats[0] + "\n" + \
                         "> Dexterity: " + self.stats[1] + "\n" + \
                         "> Constitution: " + self.stats[2] + "\n" + \
                         "> Intelligence: " + self.stats[3] + "\n" + \
                         "> Luck: " + self.stats[4] + "\n\n" + \
                         "> HP: " + self.hitPoints + "/" + self.maxHitPoints

        return printStatement

    #TODO: ADD GENERAL SKILLS EVERY PLAYER CAN DO (Fleeing, Examining, Persuasion, etc. etc.)


class Spell:

    def __init__(self, name, desc, level, castTime, necessity, damage):
        self.name = name
        self.desc = desc
        self.level = level
        self.castTime = castTime
        self.necessity = necessity
        self.damage = damage


class Items:

    def __init__(self, name, itemType, stats):
        self.name = name
        self.type = itemType
        self.stats = stats


