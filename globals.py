from constants import ScreenDetails, Screen

class GlobalConfig:
    currentScreenDetails = None
    currentChapter = "-1"
    currentChapterData = {}
    currentChapterCheckpointId = "-1.1"
    currentChapterCheckpointOptions = []

    def __init__(self, currScrDet, currChp, currChpDat, currChpChkId, currChpChkOpt):
        self.currentScreenDetails = currScrDet
        self.currentChapter = currChp
        self.currentChapterData = currChpDat
        self.currentChapterCheckpointId = currChpChkId
        self.currentChapterCheckpointOptions = currChpChkOpt

currentGlobalConfig = GlobalConfig(
    ScreenDetails(Screen.MAIN_MENU, [], None),
    "=1",
    {},
    "1.1",
    []
)


isInventoryOpen = False