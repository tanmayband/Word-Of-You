from constants import ScreenDetails, Screen, Inventory

class GlobalConfig:
    currentScreenDetails = None
    currentChapter = "-1"
    currentChapterData = {}
    currentChapterCheckpointId = "-1.1"
    currentChapterCheckpointOptions = []
    currentInventory = None

    def __init__(self, currScrDet, currChp, currChpDat, currChpChkId, currChpChkOpt, currInv):
        self.currentScreenDetails = currScrDet
        self.currentChapter = currChp
        self.currentChapterData = currChpDat
        self.currentChapterCheckpointId = currChpChkId
        self.currentChapterCheckpointOptions = currChpChkOpt
        self.currentInventory = currInv

currentGlobalConfig = GlobalConfig(
    ScreenDetails(Screen.MAIN_MENU, [], None),
    "-1",
    {},
    "1.1",
    [],
    Inventory([])
)
isInventoryOpen = False