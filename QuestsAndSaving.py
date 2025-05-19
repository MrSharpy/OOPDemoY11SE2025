import os

def clearScreen():
    os.system('cls')

class Quest:
    def __init__(self, name, reward, description, status='Inactive'):
        self.name = name
        self.goldReward = reward
        self.description = description
        self.status = status

    def getStatus(self):
        return self.status

    def setStatus(self, currentStatus):
        if currentStatus in ['Completed', 'In Progress', 'Inactive']:
            self.status = currentStatus

class Player:
    def __init__(self, name, health, attack, position, gold):
        self.name = name
        self.health = health
        self.attack = attack
        self.position = position 
        self.gold = gold
        self.quests = [
            Quest('Main Quest', 5, 'Basic starter quest'),
            Quest('I need the frog toes', 10, "Babies first fetch quest"),
            Quest('Quest demo 3', 10, "Babies first fetch quest"),
            Quest('Quest demo 4', 10, "Babies second fetch quest"),
            Quest('Quest demo 5', 10, "Babies third fetch quest"),
            Quest('Quest demo 6', 10, "Babies fourth fetch quest"),
            Quest('Quest demo 7', 10, "Babies fifth fetch quest"),
            Quest('Quest demo 8', 10, "Babies sixth fetch quest"),
            Quest('Quest demo 9', 10, "Babies seventh fetch quest"),
            Quest('Quest demo 10', 10, "Babies eighth fetch quest")
        ]

    def move(self, direction, gameMap):
        if direction == 'up' and self.position[0] > 0:
            self.position[0] -= 1
        elif direction == 'down' and self.position[0] < len(gameMap) - 1:
            self.position[0] += 1
        elif direction == 'left' and self.position[1] > 0:
            self.position[1] -= 1
        elif direction == 'right' and self.position[1] < len(gameMap[0]) - 1:
            self.position[1] += 1
        else:
            print("You can't move in that direction.")
            return False
        return True

    def isAlive(self):
        return self.health > 0

    def getStats(self):
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")

    def getQuests(self):
        for quest in self.quests:
            if quest.getStatus() != 'Inactive':
                print(f"Quest: {quest.name}")
                print(f"Status: {quest.getStatus()}")
                print(f"Reward: {quest.goldReward} gold")
                print(f"Description: {quest.description}")
                print("-" * 20)

    def setLoadFileQuests(self, index, status):
        self.quests[index].setStatus(status)

    def saveInfo(self):
        with open('playerSave.txt', 'w') as f:
            questsData = ','.join([f"{q.status}" for q in self.quests])
            f.write(f"{self.name},{self.health},{self.attack},{self.position[0]},{self.position[1]},{self.gold},{questsData}\n")
        print("Player information saved to 'playerSave.txt' file.")

class Game:
    def __init__(self, player):
        self.player = player
        self.gameMap = self.createMap()

    def createMap(self):
        return [
            ['T', 'x', 'x', 'C', 'x'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'C', 'x', 'T', 'x'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x']
        ]

    def displayMap(self):
        for i, row in enumerate(self.gameMap):
            for j, cell in enumerate(row):
                if [i, j] == self.player.position:
                    print('P', end=' ')
                else:
                    print(cell, end=' ')
            print()

    def enterTown(self):
        print("Welcome to the town! What would you like to do?")
        while True:
            choice = input("Enter 'shop' to visit the shop, 'leave' to leave the town, or 'info' to view player info: ").lower()
            if choice == 'shop':
                print("You visit the shop and browse the items.")
                break
            elif choice == 'leave':
                print("You leave the town and continue your journey.")
                break
            elif choice == 'info':
                self.checkPlayerInfo()
            else:
                print("Invalid choice. Please enter 'shop', 'leave', or 'info'.")

    def checkPlayerInfo(self):
        while True:
            clearScreen()
            print("Player Information Menu:")
            print("1. View Stats")
            print("2. View Quests")
            print("3. Save Info to File")
            print("4. Return to Game")
            choice = input("Choose an option (1/2/3/4): ")
            if choice == '1':
                self.player.getStats()
                input("Press Enter to return to the menu...")
            elif choice == '2':
                self.player.getQuests()
                input("Press Enter to return to the menu...")
            elif choice == '3':
                self.player.saveInfo()
                input("Press Enter to return to the menu...")
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    def play(self):
        while self.player.isAlive():
            clearScreen()
            self.displayMap()
            move = input("Enter move (up/down/left/right): ").lower()
            if self.player.move(move, self.gameMap):
                if self.gameMap[self.player.position[0]][self.player.position[1]] == 'T':
                    clearScreen()
                    self.enterTown()
            else:
                print("Invalid move. Try again.")

        print("Game Over. You have been defeated.")

def mainMenu():
    while True:
        clearScreen()
        print("Main Menu:")
        print("1. Start New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")
        if choice == '1':
            playerName = input("Enter your character's name: ")
            player = Player(playerName, 100, 10, [0,0])
            game = Game(player)
            game.play()
            break
        elif choice == '2':
            player = loadInfo()
            if player:
                game = Game(player)
                game.play()
                break
            else:
                playerName = input("Enter your character's name: ")
                player = Player(playerName, 100, 10, [0,0])
                game = Game(player)
                game.play()
                break
        elif choice == '3':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to try again...")

def loadInfo():
    if os.path.exists('playerSave.txt'):
        with open('playerSave.txt', 'r') as file:
            data = file.read().split(',')
            name = data[0]
            health = int(data[1])
            attack = int(data[2])
            position = [int(data[3]), int(data[4])]
            gold = int(data[5])
            player = Player(name, health, attack, position, gold)
            for i in range(10):
                player.setLoadFileQuests(i, data[i+6])
            return player
    else:
        print("No saved game found. Starting a new game.")
        return None


if __name__ == "__main__":
    mainMenu()