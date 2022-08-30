from enum import Enum

class Screen(Enum):
    NONE, MAIN_MENU, SELECT_PROFILE, PAUSE_MENU, GAME, INVENTORY, EXIT = range(7)

class ScreenDetails:
    screenType = Screen.NONE
    prevScreenType = Screen.NONE
    nextScreenType = Screen.NONE
    screenCommands = []
    inputProcessor = None

    def __init__(self, scrType, scrCmds, scrInputPrc, prvScrType=None, nxtScrType=None):
        self.screenType = scrType
        self.screenCommands = scrCmds
        self.inputProcessor = scrInputPrc

        if prvScrType is not None:
            self.prevScreenType = prvScrType
        if nxtScrType is not None:
            self.nextScreenType = nxtScrType

currentScreenDetails = ScreenDetails(Screen.GAME, [], None)

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

commandsGeneric = [commandExitGame, commandList, commandOpenInventory, commandCloseInventory, commandNewGame, commandLoadGame]