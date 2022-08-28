import globals
import utils

def start():
    print(f"\n------------------------------\n--- YOUR ADVENTURE AWAITS! ---\n------------------------------")
    print(f"[\"{globals.exitGameCommand}\" to exit game]")
    print(f"[\"{globals.listCommand}\" to list actions]")
    print()
    nextCheckpoint = "1.1"
    while(nextCheckpoint != "-1"):
        nextCheckpoint = utils.loadCheckpoint(nextCheckpoint)
    

start()