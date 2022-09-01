from glob import glob
from constants import Screen, ScreenDetails
import constants
import globals
import utils

def showMainMenu():
    def mainMenuInput(inputResponse):
        if(inputResponse == constants.commandNewGame):
            globals.currentGlobalConfig.currentScreenDetails = showNewGameScreen(screenDetails)
        elif(inputResponse == constants.commandLoadGame):
            globals.currentGlobalConfig.currentScreenDetails = showLoadGameScreen(screenDetails)

    screenDetails = ScreenDetails(Screen.MAIN_MENU, [constants.commandLoadGame, constants.commandNewGame, constants.commandExitGame, constants.commandList], mainMenuInput)
    globals.currentGlobalConfig.currentScreenDetails = screenDetails
    print(f"> Type an option")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    return screenDetails

def showNewGameScreen(prevScrDet):
    def MakeProfileInput(inputResponse):
        if(inputResponse not in globals.currentGlobalConfig.currentScreenDetails.getAllCommands()):
            inputResponse = utils.sanitizeInput(inputResponse)
            if(inputResponse in allProfiles):
                print(f"Sorry! {inputResponse} is already taken. Try a different name.")
            else:
                print(f"# Creating profile \"{inputResponse}\"...")
                utils.createNewProfile(inputResponse)
                # start game
                showGameScreen()
            

    screenDetails = ScreenDetails(Screen.NEW_PROFILE, [constants.commandMenuBack, constants.commandExitGame, constants.commandList], MakeProfileInput, prevScrDet)
    globals.currentGlobalConfig.currentScreenDetails = screenDetails
    print(f"\n# Creating a new profile...")
    print(f"> Type a name:")
    print("(Only alphanumeric names allowed. Command names not allowed. \"list\" to find out.)")
    allProfiles = utils.getAllProfiles()

    return screenDetails

def showLoadGameScreen(prevScrDet):
    def LoadProfileInput(inputResponse):
        if(inputResponse not in globals.currentGlobalConfig.currentScreenDetails.getAllCommands() and inputResponse in availableProfiles):
            inputResponse = utils.sanitizeInput(inputResponse)
            print(f"# Loading profile \"{inputResponse}\"...")
            utils.loadGame(inputResponse)
            # start game
            showGameScreen()

    screenDetails = ScreenDetails(Screen.SELECT_PROFILE, [constants.commandMenuBack, constants.commandExitGame, constants.commandList], LoadProfileInput, prevScrDet)
    globals.currentGlobalConfig.currentScreenDetails = screenDetails
    availableProfiles = utils.getAllProfiles()
    if(len(availableProfiles)):
        print(f"\n# Available profiles:")
        utils.printOptions(availableProfiles)
        print(f"\n> Select a name:")
    else:
        print("No profiles made yet!")

    return screenDetails

def showGameScreen(prevScrDet=None):
    def gameScreenInput(inputResponse):
        if(inputResponse not in globals.currentGlobalConfig.currentScreenDetails.screenCommands):
            if(inputResponse not in globals.currentGlobalConfig.currentScreenDetails.screenTempCommands):
                print(f"You fail to do that. Try again.")
            else:
                print("")
                checkpointData = globals.currentGlobalConfig.currentChapterData[globals.currentGlobalConfig.currentChapterCheckpointId]
                optionIndex = globals.currentGlobalConfig.currentScreenDetails.screenTempCommands.index(inputResponse)
                actionFound = checkpointData["options"][optionIndex]
                actionResponse = actionFound["optionResponse"]
                actionType = actionFound["optionType"]
                
                if(type(actionResponse) == list):
                    utils.printDescription(actionResponse)
                else:
                    inputResponse = actionResponse

                if(actionType == "once"):
                    checkpointData["options"].pop(optionIndex)
                    globals.currentGlobalConfig.currentScreenDetails.screenTempCommands = [option["optionText"] for option in checkpointData["options"]]
      
                gameScreenUpdate(inputResponse)
                
        else:
            if(inputResponse == constants.commandOpenInventory):
                # globals.isInventoryOpen = True
                globals.currentGlobalConfig.currentInventory.printInventory()
                
            elif(inputResponse == constants.commandSaveGame):
                print(f"> Saving to {globals.currentGlobalConfig.currentProfileName}...")
                utils.saveGame()
                print(f"> Save to {globals.currentGlobalConfig.currentProfileName} successful")

        # CHEAT: comment in to enable jumpoing to checkpoints by inputting its id
        # gameScreenUpdate(inputResponse)

    def gameScreenUpdate(inputResponse):
        if(inputResponse[0].isnumeric()):
            utils.loadCheckpoint(inputResponse)
            globals.currentGlobalConfig.currentScreenDetails.updateTempCommands(globals.currentGlobalConfig.currentChapterCheckpointOptions)

    print(f"\n------------------------------\n--- YOUR ADVENTURE AWAITS! ---\n------------------------------")
    print()

    screenDetails = None
    if(globals.currentGlobalConfig.currentScreenDetails.screenType != Screen.GAME):
        screenDetails = ScreenDetails(Screen.GAME, [constants.commandSaveGame, constants.commandExitGame, constants.commandList, constants.commandPrintConfig], gameScreenInput, prevScrDet)
        globals.currentGlobalConfig.currentScreenDetails = screenDetails
    else:
        screenDetails = globals.currentGlobalConfig.currentScreenDetails
    print(f"# General Commands:")
    for option in screenDetails.screenCommands:
        print(f"- {option}")

    gameScreenUpdate(globals.currentGlobalConfig.currentChapterCheckpointId)
    return screenDetails