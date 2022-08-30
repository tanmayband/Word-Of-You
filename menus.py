import globals
import utils

def showStartMenu():
    print(f"> Type an option")
    print(f"- {globals.commandLoadGame}")
    print(f"- {globals.commandNewGame}")
    print(f"- {globals.commandExitGame}")

    utils.processInput()