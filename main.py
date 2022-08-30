from glob import glob
import globals
from constants import Screen, ScreenDetails
import constants
import utils
import screens

def mainLoop():
    globals.currentGlobalConfig.currentScreenDetails = screens.showMainMenu()
    while(globals.currentGlobalConfig.currentScreenDetails.screenType != constants.Screen.EXIT):
        # if(globals.currentGlobalConfig.currentScreenDetails.screenType == constants.Screen.MAIN_MENU):
        #     currentScreenDetails = screens.showMainMenu()
        # elif(globals.currentGlobalConfig.currentScreenDetails.screenType == constants.Screen.SELECT_PROFILE):
        #     currentScreenDetails = screens.showMainMenu()
        # if(globals.currentGlobalConfig.currentScreenDetails.screenType == constants.Screen.GAME):
        #     currentScreenDetails = screens.showGameScreen()

        # globals.currentGlobalConfig.currentScreenDetails = currentScreenDetails
        inputResponse = ""
        while(inputResponse != constants.commandExitGame):
            currentScreenDetails = globals.currentGlobalConfig.currentScreenDetails

            if(currentScreenDetails.inputProcessor):
                if(inputResponse and len(inputResponse) > 0):
                    print(f"non-empty inputProcessor with {currentScreenDetails.inputProcessor.__name__}")
                    currentScreenDetails.inputProcessor(inputResponse)
            inputResponse = utils.processInput()
            
            if(inputResponse == constants.commandList):
                inputResponse = ""

        if(inputResponse == constants.commandExitGame):
            globals.currentGlobalConfig.currentScreenDetails = constants.exitScreenDetails

# screens.showGameScreen()
# screens.showMainMenu()
mainLoop()