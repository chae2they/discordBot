import character_manager
import gameMechanicClasses


testPlayer = gameMechanicClasses.Player('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p')
character_manager.SavePlayerData(testPlayer)

testPlayer = character_manager.LoadPlayerData("a")
print(testPlayer)

testPlayer.inventory = [0, 0]
testPlayer.user = "a1"
character_manager.SavePlayerData(testPlayer)

#character_manager.DeletePlayerData(testPlayer.user)


