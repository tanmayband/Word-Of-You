import globals
import utils
import menus

def start():
    print(f"\n------------------------------\n--- YOUR ADVENTURE AWAITS! ---\n------------------------------")
    print(f"[\"{globals.commandExitGame}\" to exit game]")
    print(f"[\"{globals.commandList}\" to list actions]")
    print()
    inputResponse = "1.1"
    while(inputResponse != globals.commandExitGame):
        if(inputResponse not in globals.commandsGeneric):
            utils.loadCheckpoint(inputResponse)
        inputResponse = utils.processInput()
    
start()
# menus.showStartMenu()