import globals
import utils
import screens

def mainLoop():
    currentScreenDetails = globals.currentScreenDetails
    while(globals.currentScreenDetails.screenType != globals.Screen.EXIT):
        if(globals.currentScreenDetails.screenType == globals.Screen.MAIN_MENU):
            currentScreenDetails = screens.showMainMenu()
        elif(globals.currentScreenDetails.screenType == globals.Screen.SELECT_PROFILE):
            currentScreenDetails = screens.showMainMenu()
        if(globals.currentScreenDetails.screenType == globals.Screen.GAME):
            currentScreenDetails = screens.showGameScreen()

        globals.currentScreenDetails = currentScreenDetails
        inputResponse = ""
        while(inputResponse != globals.commandExitGame):
            if(inputResponse not in globals.commandsGeneric):
                if(currentScreenDetails.inputProcessor):
                    currentScreenDetails.inputProcessor(inputResponse)
            inputResponse = utils.processInput()

# screens.showGameScreen()
# screens.showMainMenu()
mainLoop()