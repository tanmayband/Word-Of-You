import traceback
from typing import List
import json
import re

import globals

def printDescription(descTexts):
    for descText in descTexts:
        print(f"# {descText}\n")

def printPrompt(promptText):
    if(len(promptText) > 0):
        print(f"> {promptText}")

def printOptions(optionsList):
    for optionText in optionsList:
        print(f"- {optionText}")

def addOptionsToCheckpoint(newOptionsList, oldOptionsList):
    oldOptionTexts = [option["optionText"] for option in oldOptionsList]
    for newOption in newOptionsList:
        if(newOption["optionType"] != "persist" and newOption["optionText"] not in oldOptionTexts):
            oldOptionsList.append(newOption)
    return oldOptionsList

def addOptionsToScreen(newOptionsList):
    for addOption in newOptionsList:
        if(addOption["optionType"] == "persist"):
            globals.currentScreenDetails.addScreenCommand(addOption["optionText"])

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
                globals.currentChapterData[checkpointData["addOptionsTo"]]["options"] = addOptionsToCheckpoint(checkpointData["addOptions"], globals.currentChapterData[checkpointData["addOptionsTo"]]["options"])

                # add to screen details too (if any "persist" type options)
                addOptionsToScreen(checkpointData["addOptions"])


            # add to inventory (if any)
            if("addToInventory" in checkpointData):
                addToInventory(checkpointData["addToInventory"])

            # moving back to an earlier checkpoint (if any)
            if("goToCheckpoint" in checkpointData):
                globals.currentChapterCheckpointId = checkpointData["goToCheckpoint"]
                checkpointData = globals.currentChapterData[globals.currentChapterCheckpointId]
            
            # show action options
            if("options" in checkpointData):
                globals.currentChapterCheckpointOptions = [option["optionText"] for option in checkpointData["options"]]
                printOptions(globals.currentChapterCheckpointOptions)

    except:
        traceback.print_exc()
        traceback.print_stack()

def loadFile(filename):
    file = open(filename)
    jsonData = json.load(file)
    file.close()
    return jsonData

def validateInput(inputText):
    pattern = r"^[a-zA-Z0-9\s]+$"     # only alphanumeric with spaces allowed
    return re.match(pattern, inputText) != None

def sanitizeInput(inputText):
    inputText = inputText.replace(" ", "_")
    return inputText

def processInput():
    moveAhead = False
    inputResponse = ""
    # while(not moveAhead):
    action = input("> ").strip().lower()
    if(validateInput(action)):
        inputResponse = action
        genericResponse = processGenericInput(action)
        if(genericResponse):
            # moveAhead = True
            inputResponse = genericResponse
    else:
        print("Only alphanumeric input please")
            
    return inputResponse

def processGenericInput(action):
    genericResponse = None
    if(action in globals.commandsGeneric):
        if(action == globals.commandExitGame):
            genericResponse = action
            print(f"\nYou do that.\n")
        elif(action == globals.commandList):
            genericResponse = action
            print()
            if(len(globals.currentScreenDetails.screenTempCommands)):
                print("--------")
                printOptions(globals.currentScreenDetails.screenTempCommands)
            print("--------")
            printOptions(globals.currentScreenDetails.screenCommands)
            print("--------")

    return genericResponse