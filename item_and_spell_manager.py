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

    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Spell Compendium\\" + spell.name + ".json"
    fp = open(filename, "w")
    json.dump(save, fp, indent=4)
    fp.close()

def LoadSpell(spellName:str):
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Spell Compendium\\" + spellName + ".json"
    fp = open(filename, "r")
    loaded = json.load(fp)
    spell = gameMechanicClasses.Spell(loaded["name"], loaded["desc"], loaded["level"], loaded["castTime"],
                                      loaded["necessity"], loaded["damage"])
    return spell

def LoadAllSpells():
    path = os.getcwd() + "\\Spell Compendium"
    dir_list = os.listdir()