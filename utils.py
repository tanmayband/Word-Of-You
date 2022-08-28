from multiprocessing.dummy import Array
import traceback
from typing import List
import globals
import json

def printDescription(descTexts):
    for descText in descTexts:
        print(f"# {descText}\n")

def printPrompt(promptText):
    if(len(promptText) > 0):
        print(f"> {promptText}")

def printOptions(optionsList):
    for optionObj in optionsList:
        print(f"- {optionObj['optionText']}")

def addOptions(newOptionsList, oldOptionsList):
    oldOptionTexts = [option["optionText"] for option in oldOptionsList]
    for newOption in newOptionsList:
        if(newOption["optionText"] not in oldOptionTexts):
            oldOptionsList.append(newOption)
    return oldOptionsList

def addToInventory(itemsList):
    print("ADDED TO INVENTORY:")
    for itemName in itemsList:
        print(f"* {itemName}")
    print("")

def loadChapter(chapterNum):
    chapterData = loadFile(f"chapter{chapterNum}.json")
    globals.currentChapterData = chapterData
    globals.currentChapter = chapterNum

def loadCheckpoint(checkpointId):
    try:
        nextCheckpoint = ""
        if(checkpointId[0] != globals.currentChapter):
            # different chapter
            loadChapter(checkpointId[0])
            
        checkpointData = globals.currentChapterData[checkpointId]
        printDescription(checkpointData["description"])

        if("nextChapterCheckpoint" in checkpointData):
            print(f"\nTo be continued...\n")
            nextCheckpoint = checkpointData["nextChapterCheckpoint"]
        else:
            # show prompt (if any)
            if("prompt" in checkpointData):
                printPrompt(checkpointData["prompt"])

            # check for new options unlocked
            if("addOptions" in checkpointData):
                globals.currentChapterData[checkpointData["addOptionsTo"]]["options"] = addOptions(checkpointData["addOptions"], globals.currentChapterData[checkpointData["addOptionsTo"]]["options"])

            # add to inventory (if any)
            if("addToInventory" in checkpointData):
                addToInventory(checkpointData["addToInventory"])

            # moving back to an earlier checkpoint (if any)
            if("goToCheckpoint" in checkpointData):
                checkpointData = globals.currentChapterData[checkpointData["goToCheckpoint"]]
            
            # show action options
            allActions = []
            if("options" in checkpointData):
                printOptions(checkpointData["options"])
                allActions = [option["optionText"] for option in checkpointData["options"]]
            
            # await/process input
            moveAhead = False
            while(not moveAhead):
                action = input("> ").strip().lower()
                if(action in globals.genericCommands):
                    if(action == globals.exitGameCommand):
                        print(f"\nYou do that.\n")
                        nextCheckpoint = "-1"
                        moveAhead = True
                    elif(action == globals.listCommand):
                        printOptions(checkpointData["options"])
                    elif(action == globals.openInventoryCommand):
                        globals.isInventoryOpen = True
                        print("the inventory is not here yet. they said one-day delivery, absolute noobs. you'll see it when we see it. END OF DEMO")
                else:
                    if(action not in allActions):
                        print(f"You fail to do that. Try again.")
                    else:
                        print("")
                        optionIndex = allActions.index(action)
                        actionFound = checkpointData["options"][optionIndex]
                        actionResponse = actionFound["optionResponse"]
                        actionType = actionFound["optionType"]
                        
                        if(type(actionResponse) == list):
                            printDescription(actionResponse)
                        else:
                            nextCheckpoint = actionResponse
                            moveAhead = True

                        if(actionType == "once"):
                            checkpointData["options"].pop(optionIndex)
                            allActions = [option["optionText"] for option in checkpointData["options"]]
                
        return nextCheckpoint
    except:
        return "-1"

def loadFile(filename):
    file = open(filename)
    jsonData = json.load(file)
    file.close()
    return jsonData