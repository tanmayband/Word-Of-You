from enum import Enum

class Screen(Enum):
    NONE, MAIN_MENU, SELECT_PROFILE, PAUSE_MENU, GAME, INVENTORY, EXIT = range(7)

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

    def updateTempCommands(self, newCommands):
        self.screenTempCommands = newCommands

currentScreenDetails = ScreenDetails(Screen.GAME, [], None)
exitScreenDetails = ScreenDetails(Screen.EXIT, [], None)

currentChapter = "-1"
currentChapterData = {}
currentChapterCheckpointId = "-1.0"
currentChapterCheckpointOptions = []
isInventoryOpen = False

commandExitGame = "exit game"
commandList = "list"
commandOpenInventory = "open inventory"
commandCloseInventory = "close inventory"
commandNewGame = "start game"
commandLoadGame = "load game"

commandsGeneric = [commandExitGame, commandList]
#, commandOpenInventory, commandCloseInventory, commandNewGame, commandLoadGame]