from glob import glob
import globals
import constants
import utils
import screens

def mainLoop():
    globals.currentScreenDetails = screens.showMainMenu()
    while(globals.currentScreenDetails.screenType != constants.Screen.EXIT):
        # if(globals.currentScreenDetails.screenType == constants.Screen.MAIN_MENU):
        #     currentScreenDetails = screens.showMainMenu()
        # elif(globals.currentScreenDetails.screenType == constants.Screen.SELECT_PROFILE):
        #     currentScreenDetails = screens.showMainMenu()
        # if(globals.currentScreenDetails.screenType == constants.Screen.GAME):
        #     currentScreenDetails = screens.showGameScreen()

        # globals.currentScreenDetails = currentScreenDetails
        inputResponse = ""
        while(inputResponse != constants.commandExitGame):
            currentScreenDetails = globals.currentScreenDetails

            if(currentScreenDetails.inputProcessor):
                if(inputResponse and len(inputResponse) > 0):
                    currentScreenDetails.inputProcessor(inputResponse)
            inputResponse = utils.processInput()
            
            if(inputResponse == constants.commandList):
                inputResponse = ""

        if(inputResponse == constants.commandExitGame):
            globals.currentScreenDetails = constants.exitScreenDetails

# screens.showGameScreen()
# screens.showMainMenu()
mainLoop()