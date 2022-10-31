# Imports Libraries
import hou
import os
from functools import partial

# Declares Varibale
vNum = str(1)
globalPath = "W:/01prj/AAJ/prod/shotpub"

# Getting All Nodes From /obj Context
obj = hou.node('/obj')
allGeometry = obj.children()

# Getting The Fist Found Object Only
getObjOne, *getObjRest = allGeometry

# Getting All Nodes That Are Type Of Alembic
allAlembics = hou.sopNodeTypeCategory().nodeType("alembic").instances()

# Getting The Fist Found Alembic Only
getAbcOne, *getAbcRest = allAlembics

# Doing Some Typical String Concatenation To Create The Full Path
pathToAlembic = ("/obj/" + str(getObjOne) + '/' + str(getAbcOne))

# Pointer For Node From Which ABC Range Data Will Be Extracted
workNode = hou.node(pathToAlembic)
# ABC Data
tree = workNode.infoTree()
branches = tree.branches()

# Hoops In Loops
info = "Alembic SOP Info"
if info in branches:
    rows = branches[info].rows()
    start = ""
    end = ""
    for row in rows:
        if row[0] == "Start Frame":
            start = row[1]
        if row[0] == "End Frame":
            end = row[1]
# Just Assigning The Variables Which Is Extracted The Above Loop
    if start != "" and end != "":
        start = int(start)          # Making Sure Not To Get Float Frame Number
        end = int(end)              # Making Sure Not To Get Float Frame Number
else:
    print("No Frame Range Data!")

# Actual Command That Sets The Frame Range & Playback Range
hou.playbar.setFrameRange(start, end)
hou.playbar.setPlaybackRange(start, end)

# Finding Cameras
nodeType = hou.nodeType('Object/cam').instances()
camName = str(nodeType[0])
camName = camName[3:21]
camPath = camName.replace("_", "/")

# Having Root Directory
saveDir = globalPath + camPath

# Creating Bunch Of Folders
dirs = ("fx_scene/caches", "fx_scene/previews", "fx_renderlayers/v000")
concatRootPath = partial(os.path.join, saveDir)
makeDirectory = partial(os.makedirs, exist_ok=True)
for pathItems in map(concatRootPath, dirs):
    makeDirectory(pathItems)

# Creating The Total Path
saveDir = globalPath + camPath + "/" + "fx_scene/"
fileName = saveDir.replace("/", "_")
fileName = "aaj" + fileName[-28:] + "source" + "_v" + vNum.zfill(3) + ".hip"

# The Final File Path For New File
mergeSDFN = saveDir + fileName

# Version Up If File Already There
if os.path.isfile(mergeSDFN):
    getFileName = str(hou.hipFile.basename())
    getVName = int(getFileName[-5:-4])
    newVNum = getVName + 1
    newVNum = str(newVNum)
    newFName = getFileName[:-7] + newVNum.zfill(3) + ".hip"
    newMergeSDFN = saveDir + newFName
    hou.hipFile.save(file_name=newMergeSDFN)
    hou.ui.displayMessage(
        "File Saved As New Version! \nThe New File Is "
        + newFName
        + "\nReconnect All Caches If $HIPNAME Varibale Was Used \nDang It!")
# Save For New Scene
else:
    hou.hipFile.save(file_name=mergeSDFN)
    hou.ui.displayMessage(
        "Version 001 File Has Been Saved! \nAll Varibales Have Been Updated "
        "With Current \nFrame Range Has Been Set \nOof! So Much Work")