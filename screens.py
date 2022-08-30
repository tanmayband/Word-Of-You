from glob import glob
from globals import Screen, ScreenDetails
import globals
import utils

def showMainMenu():
    def mainMenuInput(inputResponse):
        if(inputResponse == globals.commandNewGame):
            globals.currentScreenDetails = showNewGameScreen(screenDetails)

    screenDetails = ScreenDetails(Screen.MAIN_MENU, [globals.commandLoadGame, globals.commandNewGame, globals.commandExitGame, globals.commandList], mainMenuInput)
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
            # make folder and relevant files
            # start game
            showGameScreen()

    screenDetails = ScreenDetails(Screen.NEW_PROFILE, [globals.commandMenuBack, globals.commandExitGame, globals.commandList], MakeProfileInput, prevScrDet)
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

                if(actionType == "once"):
                    checkpointData["options"].pop(optionIndex)
                    globals.currentScreenDetails.screenTempCommands = [option["optionText"] for option in checkpointData["options"]]
        else:
            if(inputResponse == globals.commandOpenInventory):
                globals.isInventoryOpen = True
                print("the inventory is not here yet. they said one-day delivery, absolute duffers. you'll see it when we see it. END OF DEMO")
        
        if(inputResponse[0].isnumeric()):
            utils.loadCheckpoint(inputResponse)
            screenDetails.updateTempCommands(globals.currentChapterCheckpointOptions)


    globals.currentScreenDetails = Screen.GAME
    print(f"\n------------------------------\n--- YOUR ADVENTURE AWAITS! ---\n------------------------------")
    # print(f"[\"{globals.commandExitGame}\" to exit game]")
    # print(f"[\"{globals.commandList}\" to list actions]")
    print()

    screenDetails = ScreenDetails(Screen.GAME, [globals.commandExitGame, globals.commandList], gameScreenInput, prevScrDet)
    globals.currentScreenDetails = screenDetails
    print(f"# General Commands:")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    gameScreenInput(globals.currentChapterCheckpointId)
    return screenDetails

    # inputResponse = "1.1"
    # while(inputResponse != globals.commandExitGame):
    #     if(inputResponse not in globals.commandsGeneric):
    #         utils.loadCheckpoint(inputResponse)
    #     inputResponse = utils.processInput()