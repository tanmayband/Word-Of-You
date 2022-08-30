from enum import Enum

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

exitScreenDetails = ScreenDetails(Screen.EXIT, [], None)

commandExitGame = "exit game"
commandList = "list"
commandOpenInventory = "open inventory"
commandCloseInventory = "close inventory"
commandNewGame = "start game"
commandLoadGame = "load game"
commandSaveGame = "save game"
commandMenuBack = "back"

commandsGeneric = [commandExitGame, commandList]
#, commandOpenInventory, commandCloseInventory, commandNewGame, commandLoadGame]