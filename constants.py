from enum import Enum
import json

class Screen(Enum):
    NONE, MAIN_MENU, SELECT_PROFILE, NEW_PROFILE, PAUSE_MENU, GAME, INVENTORY, EXIT = range(8)

class ScreenDetails:
    screenType = Screen.NONE
    prevScreenDetails = Screen.NONE
    nextScreenDetails = Screen.NONE
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
        self.items = self.convertItemsListToDict(itemsList)

    def convertItemsListToDict(self, itemsList):
        itemsDict = {}
        for item in itemsList:
            itemName = item["itemName"]
            if itemName in itemsDict:
                itemsDict[itemName].append(item)
            else:
                itemsDict[itemName] = [item]

        return itemsDict

    def useItem(self, itemName):
        if (itemName not in self.items) or (len(self.items[itemName]) == 0):
            return False
        else:
            itemFound = self.items[itemName][0]
            itemFound.useItem()
            return True
        

class Item:
    itemName = ""
    itemHealth = 0
    itemDescription = ""

    def __init__(self, itName, itDesc, itHealth=-1):
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

commandsGeneric = [commandExitGame, commandList, commandTest]
#, commandOpenInventory, commandCloseInventory, commandNewGame, commandLoadGame]