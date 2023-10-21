#Lootbox Simulator
import random
import math
import os

os.system("cls")

# Vars
game = True
fastMode = True
playerItems = {
    "Watcher's Key Teeth": 0,
    "Watcher's Key Frames": 0,
    "Coins": 0
}

itemText = {
    "Watcher's Key Teeth": "~! Tooth !~",
    "Watcher's Key Frames": "-=!! Frame !!=-",
}
itemCost = {"Watcher's Key Teeth": 100, "Watcher's Key Frames": 400}
itemLetter = {"Watcher's Key Teeth": "t", "Watcher's Key Frames": "f"}


class Chest:
    def __init__(self, chestType, value, slots, difficulty, cost):
        self.difficulty = difficulty
        self.type = chestType
        self.slots = slots
        self.cost = cost
        self.toothChance = math.ceil((3 * value) / difficulty)
        self.frameChance = math.ceil((2 * value) / difficulty)
        self.manyCoins = math.ceil((10 * value) / difficulty)
        self.someCoins = 15
        self.lowCoins = 20
        self.table = []
        self.rewardContents = []
        self.customItems = []
        firstLetterOfChests.append(chestType[0].lower())

    def fill(self):
        self.table = []
        for i in range(self.toothChance):
            self.table.append("Watcher's Key Teeth")
        for i in range(self.frameChance):
            self.table.append("Watcher's Key Frames")
        for i in range(self.manyCoins):
            self.table.append("many")
        for i in range(self.someCoins):
            self.table.append("some")
        for i in range(self.lowCoins):
            self.table.append("low")
        for i in self.customItems:
            self.table.append(i)

    def getTable(self):
        return self.table

    def getRewardContents(self):
        return self.rewardContents

    def getName(self):
        return self.type

    def getSlots(self):
        return self.slots

    def getCost(self):
        return self.cost

    def addCustomItem(self, item, rarity, text, sellPrice, definingLetter):
        if item not in playerItems:
            playerItems[item] = 0
            itemText[item] = text
            itemCost[item] = sellPrice
            itemLetter[item] = definingLetter
        for i in range(math.floor(rarity / self.difficulty)):
            self.customItems.append(item)

    def createRewards(self):
        self.rewardContents = []
        for i in range(self.slots):
            self.rewardContents.append(
                self.table[random.randint(0, len(self.table) - 1)]
            )

    def canOpen(self):
        if playerItems["Coins"] > self.cost - 1:
            return True
        else:
            return False


class Recipe:
    def __init__(self, name, ingredients, onCraftText, sellPrice, definingLetter):
        self.ingredients = ingredients
        self.name = name
        self.onCraftText = onCraftText
        self.sellPrice = sellPrice
        firstLetterOfRecipies.append(name[0].lower())
        playerItems[name] = 0
        itemCost[name] = sellPrice
        itemLetter[name] = definingLetter

    def getName(self):
        return self.name

    def getIngredients(self):
        return self.ingredients

    def getCraftText(self):
        return self.onCraftText

    def getSellPrice(self):
        return self.sellPrice

    def craft(self):
        for i in self.ingredients:
            playerItems[i] -= self.ingredients[i]
        playerItems[self.name] += 1

    def canCraft(self):
        canCraft = True
        for i in self.ingredients:
            if playerItems[i] < self.ingredients[i]:
                canCraft = False
        return canCraft


def forceValidResponse(
    response, possibilities, whatToAsk, shouldPrintChests=False
):
    if shouldPrintChests:
        printChests()
    response = str(response).lower()
    for i in range(len(possibilities)):
        if response == str(possibilities[i]):
            return str(possibilities[i])
    response = input(whatToAsk)
    return forceValidResponse(response, possibilities, whatToAsk, shouldPrintChests)


def handleResponse(response):
    os.system("cls")
    if response == "o":
        print("")
        printChests()
        chestToOpen = input(
            "\nWhat Chest do you Wish to open? You have {0} coins\n".format(
                playerItems["Coins"]
            )
        )
        chestToOpen = forceValidResponse(
            chestToOpen,
            firstLetterOfChests,
            "\nThats not a chest! What Chest do you Wish to open? You have {0} coins\n".format(
                playerItems["Coins"]
            ),
            True,
        )
        os.system("cls")
        if chestToOpen == "b":
            return False
        else:
            openChest(chestToOpen)
    elif response == "v":
        os.system("cls")
        print("Your Items:\n---------------------------")
        for i in playerItems:
            print("{0}: {1}".format(i, playerItems[i]))
        print("---------------------------")
        input("[Enter] to continue")
        os.system("cls")
    elif response == "r":
        os.system("cls")
        confirm = input("Are you sure you wish to restart? [y]es or [n]o")
        if str(confirm).lower() == "y":
            for i in playerItems:
                playerItems[i] = 0
            print("\n\n\nGame Reset")
        else:
            print("Restart aborted")
    elif response == "c":
        os.system("cls")
        startCrafting()
    elif response == "s":
        os.system("cls")
        startSelling()
    elif response == "t":
        os.system("cls")
        global fastMode
        fastMode = not fastMode
        if fastMode:
            print("Fast Chest Opening: Enabled")
        else:
            print("Fast Chest Opening: Disabled")


def startSelling():
    hasItems = False
    for i in playerItems:
        if playerItems[i] != 0 and i != "Coins":
            hasItems = True
    if not hasItems:
        input("Come back when you have something to sell me! [Enter] to Continue")
        return
    print("\nHey! I'm the merchant around these parts? What you you have to offer?\n")
    # Handle responses with same starting letter
    print(
        "Watcher's Key [T]eeth - Sell for {0} Coins - You have {1}".format(
            itemCost["Watcher's Key Teeth"], playerItems["Watcher's Key Teeth"]
        )
    )
    print(
        "Watcher's Key [F]rames - Sell for {0} Coins - You have {1}".format(
            itemCost["Watcher's Key Frames"], playerItems["Watcher's Key Frames"]
        )
    )
    for i in playerItems:
        if playerItems[i] != 0 and i not in [
            "Coins",
            "Watcher's Key Teeth",
            "Watcher's Key Frames",
        ]:
            print(
                "[{0}]{1} - Sell for {2} Coins - You have {3}".format(
                    i[0], i[1:], itemCost[i], playerItems[i]
                )
            )
    print("[B]ack")
    item = input("")
    if item == "b":
        return False
    item = forceValidResponse(
        item,
        definingLetterList,
        "That doesn't even exist! Give me something real or leave!\n",
    )
    item = itemLetterToItem(item)
    if playerItems[item] > 0:
        playerItems[item] -= 1
        playerItems["Coins"] += itemCost[item]
    else:
        print(
            "You don't have any {0}! Come back when you have something worth my time!".format(
                item
            )
        )
        return False
    input(
        "\nYou Sold 1 of your {0} for {1} coins. You now have {2} coins [Enter] to continue".format(
            item, itemCost[item], playerItems["Coins"]
        )
    )
    doContinue = input(
        "\nThank you very much! This will go great with my collection. You just gonna stand there or are you going to\n[S]ell More Items\n[L]eave\n"
    )
    doContinue = forceValidResponse(
        doContinue,
        ["s", "l"],
        "What? I only gave you two options to either\n[S]ell More Items\n[L]eave\n",
    )
    if doContinue == "s":
        handleResponse("s")


def itemLetterToItem(letter):
    for key, value in itemLetter.items():
        if letter == value:
            return key


def startCrafting():
    print("Welcome to the Workbench! You've Got:\n")
    items = 0
    for i in playerItems:
        if playerItems[i] > 0 and i != "Coins":
            print("{0} {1}".format(playerItems[i], i))
            items += 1
    if items == 0:
        input("Absoultely Nothing! Get to Opening Those Chests! [Enter] to Continue")
        return
    else:
        print("\nWhat do you want to Craft?\n")
        for i in recipies:
            print(createRecipeString(i))
        print("[B]ack")
        item = input("")
        item = forceValidResponse(
            item,
            firstLetterOfRecipies,
            "That Recipe Doesn't Exist! What do you want to Craft?\n",
        )
        if item == "b":
            os.system('cls')
            return
        else:
            craftItem(item)


def craftItem(item):
    os.system("cls")
    for i in recipies:
        if i.getName()[0].lower() == item:
            recipeToCraft = i
    if recipeToCraft.canCraft():
        recipeToCraft.craft()
        print(
            "{0}\nCongrats! You crafted {1}".format(
                recipeToCraft.getCraftText(), recipeToCraft.getName()
            )
        )
    else:
        input("\nSorry! You don't have the ingredients to craft this! [Enter] to Continue")
        handleResponse("c")


def createRecipeString(recipe):
    string = "[{0}]{1}:".format(recipe.getName()[0], recipe.getName()[1:])
    for i in recipe.getIngredients():
        string += " - {0} {1}".format(recipe.getIngredients()[i], i)
    return string


def openChest(chest):
    for i in chests:
        if i.getName()[0].lower() == chest:
            chestToOpen = i
    if not chestToOpen:
        print("Sorry! That chest doesn't exist!")
        handleResponse("o")
    if chestToOpen.canOpen():
        playerItems["Coins"] -= chestToOpen.getCost()
    else:
        input(
            "\nSorry! You need {0} coins to open that chest but only have {1}! [Enter] to continue".format(
                chestToOpen.getCost(), playerItems["Coins"]
            )
        )
        return handleResponse("o")

    chestToOpen.fill()
    chestToOpen.createRewards()
    print("\n{0} Chest Rewards:\n------------------".format(chestToOpen.getName()))
    for i in chestToOpen.getRewardContents():
        if i in playerItems:
            playerItems[i] += 1
            print(itemText[i])
        else:
            if i == "many":
                print("~/ Bunch o' Coins \~")
                playerItems["Coins"] += 50
            elif i == "some":
                print("~ Couple o' Coins ~")
                playerItems["Coins"] += 25
            elif i == "low":
                print("Some Coins")
                playerItems["Coins"] += 10
    print("------------------")
    if not fastMode:
        input("[Enter] to continue")


def printChests():
    for i in chests:
        chestName = i.getName()
        print("[{0}]{1} - {2} coins".format(chestName[0], chestName[1:], i.getCost()))
    print("[B]ack")


def checkForWin():
    global voiceNumber
    if playerItems["Keeper's Key"] != 0:
        input("\n\n\nThat's a nice looking key you got there...\n\n[Enter] to continue")
        input(
            "\nI've been trapped here for quite awhile you see... No hands, can't open the chests...\n\n[Enter] to continue"
        )
        #Splitting up the 'accept' input string so it easier to read in the written response
        string1 = "\nI need to escape this terrible place. But I won't be unfair. Here's the plan: Beat me at rock paper scissors, "
        string2 = "I let you go.\nDon't? Your key is mine anyways. Deal?\n[y or n]\n"
        accept = input(
            string1 + string2
        )
        accept = forceValidResponse(
            accept, ["y", "n"], "What are you saying? is it a [Y]es or a [N]o???\n"
        )
        if accept == "y":
            rockPaperScissors()
        else:
            playerItems["Keeper's Key"] = 0
            print(
                "\nWow, that was no fun. Good luck struggling down here im freeeeeee!!!"
            )
            voiceNumber += 1
            print(
                "\n\nHello, I am disembodied voice number {0}. I will be your guide on this adventure!".format(
                    voiceNumber
                )
            )


def rockPaperScissors():
    global voiceNumber
    choice = input(
        "\nWell then, what weapon do you chose?\n[R]ock\n[P]aper\n[S]cissors\n"
    )
    choice = forceValidResponse(
        choice,
        ["r", "p", "s"],
        "\nGah! No cheating, you can only chose\n[R]ock\n[P]aper\n[S]cissors\n",
    )
    matrix = (
        {  # 0 = Loss, 1 = Win, 2 = Tie - Uses letter of choice response + comp response
            "rpaper": 0,
            "rscissors": 1,
            "rrock": 2,
            "ppaper": 2,
            "pscissors": 0,
            "prock": 1,
            "spaper": 1,
            "sscissors": 2,
            "srock": 0,
        }
    )
    comp = random.choice(["rock", "paper", "scissors"])
    print("\nThe computer chose {0}".format(comp))
    if matrix[choice + comp] == 0:
        print(
            "\nHah! You LOSE! The key is MINE. I am free, finally. Good luck down here"
        )
        playerItems["Keeper's Key"] = 0
        voiceNumber += 1
        print(
            "\n\nHello, I am disembodied voice number {0}. I will be your guide on this adventure!".format(
                voiceNumber
            )
        )
    elif matrix[choice + comp] == 1:
        print(
            "\nNo! Not again! Well, I am a man of my word, so you may leave. I guess I'll be waiting here for a little while longer"
        )
        endGame()
    elif matrix[choice + comp] == 2:
        print(
            "\nUgh, a draw. That is my least favorite part about this game. Welp here we go again..."
        )
        rockPaperScissors()


def endGame():
    input(
        "\n\n\nYou walk up to the convenient door with a large keyhole and turn the key inside it... [Enter] to continue\n"
    )
    input(
        "\nClick! The door opens, and you suddenly appear in a Walmart. Walmart is scary. The end lol"
    )
    game = False


# Init difficulty
difficulty = int(
    input(
        "What difficulty would you like to play on?\nEasy [1]\nMedium [2]\nHard [3]\n"
    )
)
difficulty = forceValidResponse(
    difficulty,
    [1, 2, 3],
    "\nThat is not a difficulty, please select one of the three difficulties listed below:\nEasy [1]\nMedium [2]\nHard [3]\n",
)
difficulty = int(difficulty)

# Init chests - Chest('name', 'value (rare drop chances)', slots, difficulty, buy cost)
firstLetterOfChests = ["b"]
chests = []
chests.append(Chest("Wooden", 0, 3, difficulty, 0))  # 0
chests.append(Chest("Golden", 1, 3, difficulty, 50))  # 1
chests.append(Chest("Diamond", 3, 4, difficulty, 150))  # 2
chests.append(Chest("Emerald", 4, 5, difficulty, 450))  # 3
chests.append(Chest("Obsidian", 6, 7, difficulty, 1000))  # 4
chests[3].addCustomItem("Sledgehammers", 20, "》》A Sledgehammer《《", 2000, "s")
chests[4].addCustomItem("Weird Sticks", 5, "【『 A Stick? 』】", 5000, "w")

# Init recipies - Recipe('name', 'ingredients in dictionary', 'text to display on craft', 'sell price')
firstLetterOfRecipies = ["b"]
recipies = []
recipies.append(
    Recipe(
        "Very Sticky Glue",
        {"Weird Sticks": 1, "Sledgehammers": 2},
        "You hit the sticks with the sledgehammer and some really sticky glue suddenly appears!",
        10000,
        "v",
    )
)
recipies.append(
    Recipe(
        "Keeper's Key",
        {"Very Sticky Glue": 1, "Watcher's Key Teeth": 3, "Watcher's Key Frames": 1},
        "That looks like your key to getting out of here!",
        100000,
        "k",
    )
)

# Final Inits
definingLetterList = ["b"]
for i in itemLetter:
    definingLetterList.append(itemLetter[i])

# Start game
voiceNumber = 1
os.system("cls")
print(
    "Hello, I am disembodied voice number {0}. I will be your guide on this adventure!".format(
        voiceNumber
    )
)
while game:
    response = input(
        "\nWhat next? You have {0} coins\n[O]pen a Chest\n[V]iew Items\n[R]estart\n[C]raft\n[S]ell\n[T]oggle FastChest Mode\n".format(
            playerItems["Coins"]
        )
    )
    response = forceValidResponse(
        response,
        ["o", "v", "r", "c", "s", "t"],
        "That is not something you can do! You have {0} coins You can either:\n[O]pen a Chest\n[V]iew Items\n[R]estart\n[C]raft\n[S]ell\n[T]oggle FastChest Mode\n".format(
            playerItems["Coins"]
        ),
    )
    handleResponse(response)
    checkForWin()