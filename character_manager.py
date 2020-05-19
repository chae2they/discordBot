"""
THIS PYTHON FILE IS FOR CHARACTER MANAGEMENT.

THE SCOPE OF THE FILE IS LIMITED TO:
-LOADING AND READING THE .json FILES OF EACH PLAYER
-EDITING THE INFORMATION STORED IN THE .json FILES FOR EACH PLAYER
"""

import json
import gameMechanicClasses
import os


def LoadPlayerData(discordID : str) -> gameMechanicClasses.Player:
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Character Informations\\" + discordID + ".json"
    fp = open(filename, "r")
    character = json.load(fp)
    player = gameMechanicClasses.Player(character["user"], character["name"], character["race"], character["job"],
                                        character["level"], character["xp"], character["xpToLevel"], character["stats"],
                                        character["proficiencies"], character["money"], character["equipments"],
                                        character["inventory"], character["hitPoints"], character["maxHitPoints"],
                                        character["spells"])
    fp.close()
    return player


def SavePlayerData(player: gameMechanicClasses.Player):
    save = {}
    save["user"] = player.user
    save["name"] = player.name
    save["race"] = player.race
    save["job"] = player.job
    save["level"] = player.level
    save["xp"] = player.xp
    save["xpToLevel"] = player.xpToLevel
    save["stats"] = player.stats
    save["proficiencies"] = player.proficiencies
    save["money"] = player.money
    save["equipments"] = player.equipments
    save["inventory"] = player.inventory
    save["hitPoints"] = player.hitPoints
    save["maxHitPoints"] = player.maxHitPoints
    save["spells"] = player.spells

    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Character Informations\\" + player.user + ".json"
    fp = open(filename, "w")
    json.dump(save, fp, indent=4)
    fp.close()


def DeletePlayerData(discordID : str):
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Character Informations\\" + discordID + ".json"
    os.remove(filename)


def LoadEnemy(enemyName):
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Enemy Compendium\\" + enemyName + ".json"
    fp = open(filename , "r")
    loaded = json.load(fp)
    enemy = gameMechanicClasses.Enemy(loaded["name"], loaded["desc"], loaded["hp"], loaded["damage"], loaded["other"])
    fp.close()
    return enemy


def SaveEnemy(enemy : gameMechanicClasses.Enemy):
    save = {}
    save["name"] = enemy.name
    save["desc"] = enemy.desc
    save["hp"] = enemy.hp
    save["damage"] = enemy.damage
    save["other"] = enemy.other
    filename = "C:\\Users\\Chaeyoung\\Documents\\Chaeyoung\\Discord Bot\\Enemy Compendium\\" + enemy.name + ".json"
    fp = open(filename, "w")
    json.dump(save, fp, indent=4)
    fp.close()


def LoadAllEnemies():
    path = os.getcwd() + "\\Enemy Compendium"
    dir_list = os.listdir(path)
    fullEnemyBook = {}
    for fp in dir_list:
        fp = path + "\\" + fp
        filename = open(fp, "r")
        loaded = json.load(filename)
        enemy = gameMechanicClasses.Enemy(loaded["name"], loaded["desc"], loaded["hp"], loaded["damage"],
                                          loaded["other"])
        fullEnemyBook[enemy.name] = enemy
        filename.close()

    return fullEnemyBook

