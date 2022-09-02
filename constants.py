from enum import Enum

class Screen(Enum):
    NONE, MAIN_MENU, SELECT_PROFILE, NEW_PROFILE, PAUSE_MENU, GAME, INVENTORY, EXIT = range(8)

class ScreenDetails:
    screenType = Screen.NONE
    prevScreenDetails = None
    nextScreenDetails = None
    screenCommands = []
    screenTempCommands = []
    inputProcessor = None

    def __init__(self, scrType, scrCmds, scrInputPrc, prvScrDet=None, nxtScrDet=None):
        self.screenType = scrType
        self.screenCommands = scrCmds
        self.inputProcessor = scrInputPrc

        if prvScrDet is not None:
            self.prevScreenDetails = prvScrDet
        if nxtScrDet is not None:
            self.nextScreenDetails = nxtScrDet

    def updateTempCommands(self, newTempCommands):
        self.screenTempCommands = newTempCommands

    def addScreenCommand(self, newCommand):
        if(newCommand not in self.screenCommands):
            self.screenCommands += [newCommand]

    def removeScreenCommand(self, oldCommand):
        if(oldCommand in self.screenCommands):
            self.screenCommands.pop(self.screenCommands.index(oldCommand))

    def getAllCommands(self):
        return self.screenCommands + self.screenTempCommands

class Inventory:
    items = {}

    def __init__(self, itemsList):
        self.items = {}
        self.addItems(itemsList)

    def addItems(self, itemsList):
        for item in itemsList:
            itemObj = Item(item)
            itemName = item["itemName"]
            if itemName in self.items:
                self.items[itemName].append(item)
            else:
                self.items[itemName] = [item]

    def useItem(self, itemName):
        if (itemName not in self.items) or (len(self.items[itemName]) == 0):
            return False
        else:
            itemFound = self.items[itemName][0]
            itemFound.useItem()
            return True

    def getAllItemNames(self):
        return list(self.items)

    def printInventory(self):
        allItemNames = self.getAllItemNames()
        allItemNames.sort()

        print("\n===== INVENTORY =====")
        for itemName in allItemNames:
            numItems = len(self.items[itemName])
            print(f"\n* {itemName.upper()} (x{numItems})")
            if(numItems):
                for item in self.items[itemName]:
                    print(f"--- Uses left: {item['itemHealth']}")
        print("\n=====================\n")


class Item:
    itemName = ""
    itemDescription = ""
    itemHealth = 0

    def __init__(self, itObj):
        if("itemHealth" not in itObj):
            itObj["itemHealth"] = -1
        self.makeItem(itObj["itemName"], itObj["itemDescription"])  

    def makeItem(self, itName, itDesc, itHealth=-1):
        self.itemName = itName
        self.itemDescription = itDesc
        self.itemHealth = itHealth

    def useItem(self):
        if(self.itemHealth > 0):
            self.itemHealth -= 1

exitScreenDetails = ScreenDetails(Screen.EXIT, [], None)

commandExitGame = "exit game"
commandList = "list"
commandOpenInventory = "open inventory"
commandCloseInventory = "close inventory"
commandNewGame = "start game"
commandLoadGame = "load game"
commandSaveGame = "save game"
commandMenuBack = "back"
commandTest = "test"
commandPrintConfig = "print all"

commandsGeneric = [commandExitGame, commandList, commandPrintConfig]
#, commandOpenInventory, commandCloseInventory, commandNewGame, commandLoadGame]