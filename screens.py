from glob import glob
from constants import Screen, ScreenDetails
import constants
import globals
import utils

def showMainMenu():
    def mainMenuInput(inputResponse):
        if(inputResponse == constants.commandNewGame):
            globals.currentScreenDetails = showNewGameScreen(screenDetails)

    screenDetails = ScreenDetails(Screen.MAIN_MENU, [constants.commandLoadGame, constants.commandNewGame, constants.commandExitGame, constants.commandList], mainMenuInput)
    globals.currentScreenDetails = screenDetails
    print(f"> Type an option")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    return screenDetails

def showNewGameScreen(prevScrDet):
    def MakeProfileInput(inputResponse):
        if(inputResponse not in globals.currentScreenDetails.getAllCommands()):
            inputResponse = utils.sanitizeInput(inputResponse)
            print(f"# Creating profile \"{inputResponse}\"...")
            globals.currentProfileName = inputResponse
            utils.createNewProfile(globals.currentProfileName)
            # start game
            showGameScreen()

    screenDetails = ScreenDetails(Screen.NEW_PROFILE, [constants.commandMenuBack, constants.commandExitGame, constants.commandList], MakeProfileInput, prevScrDet)
    globals.currentScreenDetails = screenDetails
    print(f"\n# Creating a new profile...")
    print(f"> Type a name:")
    print("(Only alphanumeric names allowed. Command names not allowed. \"list\" to find out.)")

    return screenDetails

def showGameScreen(prevScrDet=None):
    def gameScreenInput(inputResponse):
        if(inputResponse not in globals.currentScreenDetails.screenCommands):
            if(inputResponse not in globals.currentScreenDetails.screenTempCommands):
                print(f"You fail to do that. Try again.")
            else:
                print("")
                checkpointData = globals.currentChapterData[globals.currentChapterCheckpointId]
                optionIndex = globals.currentScreenDetails.screenTempCommands.index(inputResponse)
                actionFound = checkpointData["options"][optionIndex]
                actionResponse = actionFound["optionResponse"]
                actionType = actionFound["optionType"]
                
                if(type(actionResponse) == list):
                    utils.printDescription(actionResponse)
                else:
                    inputResponse = actionResponse
                    gameScreenUpdate(inputResponse)

                if(actionType == "once"):
                    checkpointData["options"].pop(optionIndex)
                    globals.currentScreenDetails.screenTempCommands = [option["optionText"] for option in checkpointData["options"]]
                
        else:
            if(inputResponse == constants.commandOpenInventory):
                globals.isInventoryOpen = True
                print("the inventory is not here yet. they said one-day delivery, absolute duffers. you'll see it when we see it. END OF DEMO")
            elif(inputResponse == constants.commandSaveGame):
                print(f"> Saving to {globals.currentProfileName}...")

        # CHEAT: comment in to enable jumpoing to checkpoints by inputting its id
        # gameScreenUpdate(inputResponse)

    def gameScreenUpdate(inputResponse):
        if(inputResponse[0].isnumeric()):
            utils.loadCheckpoint(inputResponse)
            screenDetails.updateTempCommands(globals.currentChapterCheckpointOptions)

    globals.currentScreenDetails = Screen.GAME
    print(f"\n------------------------------\n--- YOUR ADVENTURE AWAITS! ---\n------------------------------")
    print()

    screenDetails = ScreenDetails(Screen.GAME, [constants.commandSaveGame, constants.commandExitGame, constants.commandList], gameScreenInput, prevScrDet)
    globals.currentScreenDetails = screenDetails
    print(f"# General Commands:")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    gameScreenUpdate(globals.currentChapterCheckpointId)
    return screenDetails