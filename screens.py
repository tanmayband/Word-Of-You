from glob import glob
from globals import Screen, ScreenDetails
import globals
import utils

def showMainMenu():
    def mainMenuInput(inputResponse):
        # utils.loadCheckpoint(inputResponse)
        print(inputResponse)

    screenDetails = ScreenDetails(Screen.MAIN_MENU, [globals.commandLoadGame, globals.commandNewGame, globals.commandExitGame, globals.commandList], mainMenuInput)
    globals.currentScreenDetails = screenDetails
    print(f"> Type an option")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    return screenDetails

def showGameScreen():
    def gameScreenInput(inputResponse):
        if(inputResponse and len(inputResponse) > 0):
            utils.loadCheckpoint(inputResponse)

    globals.currentScreenDetails = Screen.GAME
    print(f"\n------------------------------\n--- YOUR ADVENTURE AWAITS! ---\n------------------------------")
    # print(f"[\"{globals.commandExitGame}\" to exit game]")
    # print(f"[\"{globals.commandList}\" to list actions]")
    print()

    screenDetails = ScreenDetails(Screen.GAME, [globals.commandExitGame, globals.commandList], gameScreenInput)
    globals.currentScreenDetails = screenDetails
    print(f"# General Commands:")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    gameScreenInput("1.1")
    return screenDetails

    # inputResponse = "1.1"
    # while(inputResponse != globals.commandExitGame):
    #     if(inputResponse not in globals.commandsGeneric):
    #         utils.loadCheckpoint(inputResponse)
    #     inputResponse = utils.processInput()