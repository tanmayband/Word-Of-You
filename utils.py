import traceback
from typing import List
import json
import re
import os
import shutil

import globals
import constants

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
            globals.currentGlobalConfig.currentScreenDetails.addScreenCommand(addOption["optionText"])

def addToInventory(itemsList):
    print("ADDED TO INVENTORY:")
    for itemName in itemsList:
        print(f"* {itemName}")
    print("")

def loadChapter(chapterNum):
    chapterData = loadFile(f"Data/chapter{chapterNum}.json")
    globals.currentGlobalConfig.currentChapterData = chapterData
    globals.currentGlobalConfig.currentChapter = chapterNum

def loadCheckpoint(checkpointId):
    try:
        nextCheckpoint = ""
        if(checkpointId[0] != globals.currentGlobalConfig.currentChapter):
            # different chapter
            loadChapter(checkpointId[0])
        
        globals.currentGlobalConfig.currentChapterCheckpointId = checkpointId
        checkpointData = globals.currentGlobalConfig.currentChapterData[checkpointId]
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
                globals.currentGlobalConfig.currentChapterData[checkpointData["addOptionsTo"]]["options"] = addOptionsToCheckpoint(checkpointData["addOptions"], globals.currentGlobalConfig.currentChapterData[checkpointData["addOptionsTo"]]["options"])

                # add to screen details too (if any "persist" type options)
                addOptionsToScreen(checkpointData["addOptions"])


            # add to inventory (if any)
            if("addToInventory" in checkpointData):
                addToInventory(checkpointData["addToInventory"])

            # moving back to an earlier checkpoint (if any)
            if("goToCheckpoint" in checkpointData):
                globals.currentGlobalConfig.currentChapterCheckpointId = checkpointData["goToCheckpoint"]
                checkpointData = globals.currentGlobalConfig.currentChapterData[globals.currentGlobalConfig.currentChapterCheckpointId]
            
            # show action options
            if("options" in checkpointData):
                globals.currentGlobalConfig.currentChapterCheckpointOptions = [option["optionText"] for option in checkpointData["options"]]
                printOptions(globals.currentGlobalConfig.currentChapterCheckpointOptions)

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
    inputResponse = ""
    action = input("> ").strip().lower()
    if(validateInput(action)):
        inputResponse = action
        genericResponse = processGenericInput(action)
        if(genericResponse):
            inputResponse = genericResponse
    else:
        print("Only alphanumeric input please")
            
    return inputResponse

def processGenericInput(action):
    genericResponse = None
    if(action in constants.commandsGeneric):
        if(action == constants.commandExitGame):
            genericResponse = action
            print(f"\nYou do that.\n")
        elif(action == constants.commandList):
            genericResponse = action
            print()
            if(len(globals.currentGlobalConfig.currentScreenDetails.screenTempCommands)):
                print("--------")
                printOptions(globals.currentGlobalConfig.currentScreenDetails.screenTempCommands)
            print("--------")
            printOptions(globals.currentGlobalConfig.currentScreenDetails.screenCommands)
            print("--------")

    return genericResponse

def createNewProfile(profileName):
    profilesRoot = "Profiles"
    profileDirName = os.path.join(profilesRoot, f"profile_{profileName}")
    if not os.path.exists(profileDirName):
        os.makedirs(profileDirName)
        profileGlobalsName = os.path.join(profileDirName,"globals.json")
        f = open(profileGlobalsName,'x')
        f.close()

# def save

