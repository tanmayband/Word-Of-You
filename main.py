from glob import glob
import globals
import utils
import screens

def mainLoop():
    globals.currentScreenDetails = screens.showMainMenu()
    while(globals.currentScreenDetails.screenType != globals.Screen.EXIT):
        # if(globals.currentScreenDetails.screenType == globals.Screen.MAIN_MENU):
        #     currentScreenDetails = screens.showMainMenu()
        # elif(globals.currentScreenDetails.screenType == globals.Screen.SELECT_PROFILE):
        #     currentScreenDetails = screens.showMainMenu()
        # if(globals.currentScreenDetails.screenType == globals.Screen.GAME):
        #     currentScreenDetails = screens.showGameScreen()

        # globals.currentScreenDetails = currentScreenDetails
        inputResponse = ""
        while(inputResponse != globals.commandExitGame):
            currentScreenDetails = globals.currentScreenDetails

            if(currentScreenDetails.inputProcessor):
                currentScreenDetails.inputProcessor(inputResponse)
            inputResponse = utils.processInput()
            
            if(inputResponse == globals.commandList):
                inputResponse = ""

        if(inputResponse == globals.commandExitGame):
            globals.currentScreenDetails = globals.exitScreenDetails

# screens.showGameScreen()
# screens.showMainMenu()
mainLoop()