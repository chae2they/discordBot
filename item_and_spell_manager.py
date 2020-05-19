import json
import os
import gameMechanicClasses

def AddSpell(spell:gameMechanicClasses.Spell):
    save = {}
    save["name"] = spell.name
    save["desc"] = spell.desc
    save["level"] = spell.level
    save["castTime"] = spell.castTime
    save["necessity"] = spell.necessity
    save["damage"] = spell.damage
    save["stats"] = spell.stats

    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Spell Compendium\\" + spell.name + ".json"
    fp = open(filename, "w")
    json.dump(save, fp, indent=4)
    fp.close()

def LoadSpell(spellName:str):
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Spell Compendium\\" + spellName + ".json"
    fp = open(filename, "r")
    loaded = json.load(fp)
    spell = gameMechanicClasses.Spell(loaded["name"], loaded["desc"], loaded["level"], loaded["castTime"],
                                      loaded["necessity"], loaded["damage"], loaded["stats"])
    return spell

def LoadAllSpells() -> dict:
    path = os.getcwd() + "\\Spell Compendium"
    dir_list = os.listdir(path)
    fullSpellBook = {}
    for fp in dir_list:
        fp = path + "\\" + fp
        filename = open(fp, "r")
        loaded = json.load(filename)
        spell = gameMechanicClasses.Spell(loaded["name"], loaded["desc"], loaded["level"], loaded["castTime"],
                                          loaded["necessity"], loaded["damage"], loaded["stats"])
        fullSpellBook[spell.name] = spell
        filename.close()

    return fullSpellBook


def AddItem(item: gameMechanicClasses.Items):
    save = {}
    save["name"] = item.name
    save["desc"] = item.desc
    save["itemType"] = item.itemType
    save["stats"] = item.stats

    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Item Compendium\\" + item.name + ".json"
    fp = open(filename, "w")
    json.dump(save, fp, indent=4)
    fp.close()

def LoadItem(itemName:str):
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Item Compendium\\" + itemName + ".json"
    fp = open(filename, "r")
    loaded = json.load(fp)
    item = gameMechanicClasses.Items(loaded["name"], loaded["desc"], loaded["itemType"], loaded["stats"])
    return item

def LoadAllItems() -> dict:
    path = os.getcwd() + "\\Item Compendium"
    dir_list = os.listdir(path)
    fullItemBook = {}
    for fp in dir_list:
        fp = path + "\\" + fp
        print(fp)
        filename = open(fp, "r")
        loaded = json.load(filename)
        item = gameMechanicClasses.Items(loaded["name"], loaded["desc"], loaded["itemType"], loaded["stats"])
        fullItemBook[item.name] = item
        filename.close()

    return fullItemBook