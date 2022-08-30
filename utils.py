import traceback
from typing import List
import json

import globals

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
    chapterData = loadFile(f"Data/chapter{chapterNum}.json")
    globals.currentChapterData = chapterData
    globals.currentChapter = chapterNum

def loadCheckpoint(checkpointId):
    try:
        nextCheckpoint = ""
        if(checkpointId[0] != globals.currentChapter):
            # different chapter
            loadChapter(checkpointId[0])
        
        globals.currentChapterCheckpointId = checkpointId
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
                globals.currentChapterCheckpointId = checkpointData["goToCheckpoint"]
                checkpointData = globals.currentChapterData[globals.currentChapterCheckpointId]
            
            # show action options
            if("options" in checkpointData):
                printOptions(checkpointData["options"])
                globals.currentChapterCheckpointOptions = [option["optionText"] for option in checkpointData["options"]]

    except:
        traceback.print_exc()
        traceback.print_stack()

def loadFile(filename):
    file = open(filename)
    jsonData = json.load(file)
    file.close()
    return jsonData

def processInput():
    moveAhead = False
    inputResponse = ""
    while(not moveAhead):
        action = input("> ").strip().lower()
        genericResponse = processGenericInput(action)
        if(genericResponse):
            moveAhead = True
            inputResponse = genericResponse
        else:
            if(action not in globals.currentChapterCheckpointOptions):
                print(f"You fail to do that. Try again.")
            else:
                print("")
                checkpointData = globals.currentChapterData[globals.currentChapterCheckpointId]
                optionIndex = globals.currentChapterCheckpointOptions.index(action)
                actionFound = checkpointData["options"][optionIndex]
                actionResponse = actionFound["optionResponse"]
                actionType = actionFound["optionType"]
                
                if(type(actionResponse) == list):
                    printDescription(actionResponse)
                else:
                    inputResponse = actionResponse
                    moveAhead = True

                if(actionType == "once"):
                    checkpointData["options"].pop(optionIndex)
                    globals.currentChapterCheckpointOptions = [option["optionText"] for option in checkpointData["options"]]

    return inputResponse

def processGenericInput(action):
    genericResponse = None
    if(action in globals.commandsGeneric):
        if(action == globals.commandExitGame):
            genericResponse = action
            print(f"\nYou do that.\n")
        elif(action == globals.commandList):
            genericResponse = action
            printOptions(globals.currentChapterData[globals.currentChapterCheckpointId]["options"])
        elif(action == globals.commandOpenInventory):
            if(globals.currentScreenDetails == globals.Screen.GAME):
                genericResponse = action
                globals.isInventoryOpen = True
                print("the inventory is not here yet. they said one-day delivery, absolute noobs. you'll see it when we see it. END OF DEMO")

    return genericResponse