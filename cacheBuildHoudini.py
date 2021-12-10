# import glob
# import os
# import time
# from datetime import date
# from pathlib import Path
# import getpass
# import hou

# start_time = time.time()

# # Setting The Global Path
# creationDate = date.today()
# globalPath = "W:/01prj/AAJ/prod/shotpub/"
# epiNum = "EP" + "725" + "/"
# seqNum = "SQ" + "050" + "/"
# shoNum = "SH" + "030" + "/"
# obj = hou.node("/obj")

# # Creating The Directory Variables
# filesDirectory = globalPath + epiNum + seqNum + shoNum + "data/cache/"
# camDirectory = globalPath + epiNum + seqNum + shoNum + "data/cam/"
# fileType = "/*.abc"
# bABC = "\\abc\\"
# aCache = "\\cache\\"

# # Getting The Paths Of The ABC File
# folders = Path(filesDirectory)
# for filePaths in folders.iterdir():
#     filePaths = glob.glob(str(filePaths) + "**" + "/abc" + fileType, recursive=True)
#     latestFilePaths = max(filePaths, key=os.path.getctime)

# # Getting The Names Of The Files
#     fileNames = latestFilePaths.partition(bABC)[0]
#     fileNames = fileNames.partition(aCache)[2]
#     geoNodeNames = latestFilePaths.partition(bABC)[2]
#     geoNodeNames = geoNodeNames[:-4]
#     latestFilePaths = latestFilePaths.replace("\\", "/")

# # Creating The Nodes On GEO Level    
#     geoNode = obj.createNode("geo",fileNames)
#     geoNode.setColor(hou.Color((0.15,0.20,0.25)))
#     geoNode.setUserData('nodeshape', "tabbed_right")

# # Creating The Nodes On SOP Level   
#     nullNode = geoNode.createNode("null", "OUT")
#     alembicNode = geoNode.createNode("alembic", geoNodeNames)
#     updateFilePath = alembicNode.parm("fileName")
#     updateFilePath.set(latestFilePaths)
#     nullNode.setInput(0,alembicNode,0)
#     nullNode.setColor(hou.Color((0.125,0.125,0.25)))
#     geoNode.layoutChildren()

# # Getting The Path Of The Camera
# folders = Path(camDirectory)
# for shotCamera in folders.iterdir():
#     shotCamera = glob.glob(str(shotCamera) + "**" + "/abc" + fileType, recursive=True)
#     latestCameraPath = max(shotCamera, key=os.path.getctime)

# # Getting The Name Of The Camera
#     cameraName = latestCameraPath.partition(bABC)[2]
#     cameraName = cameraName[:-4]
#     latestCameraPath = latestCameraPath.replace("\\", "/")

# #Creating The Camera Node In Houdini
# cameraNode = obj.createNode("alembicarchive",cameraName)
# updateCameraPath = cameraNode.parm("fileName").set(latestCameraPath)
# refreshHierarchy = cameraNode.parm("buildHierarchy").pressButton()

# # Some Variable For Networkbox Comments
# userName = getpass.getuser()
# userName = userName.upper()
# userName = userName[0:1] + userName[-1:]
# buildDate = creationDate.strftime("%d %b %Y ")
# nbCom = cameraName[4:-17] + " FX Scene ◆ Build " + buildDate + "◆ " + userName

# # Layot Obj Level Nodes
# obj.layoutChildren()

# # Selecting All OBJ Level Nodes
# for i in obj.children():
#     i.setSelected("on")

# # Putting The Selection In Var
# sel = hou.selectedNodes()[0]
# all = hou.selectedNodes()

# # Position Of Network Box From Selection
# pos = sel.position()
# parent = sel.parent()

# # Creating Network Box
# box = parent.createNetworkBox()
# box.setPosition(sel.position())

# # Adding All Nodes
# for node in all:
#     box.addItem(node)

# # Box Parms
# box.setColor(hou.Color(0.095, 0.35, 0.25))
# box.setComment(nbCom)

# # Fit Box
# box.fitAroundContents()
# box.resize(hou.Vector2(5,0.5))


# timeTaken = ("%s Seconds!" % (time.time() - start_time))
# # Some Message
# hou.ui.displayMessage("Zoop! Now That's Some Flash In Action \nCache Building Done In Just " + timeTaken + "\nPlease Save The File Using Script.")








# # stick Note Part
# thetext = """Please Read This The ABC Shot Builder Tool Import All Latest Cache For Proper Directory
# & Creates The Files Also Assinging A Null Node To Each File. Since The Update Tool Isn't
# Ready Yet, Its A Suggestion To Use Object Merge Everywhere. So If There Is Any Cache Update You Can manually Delete The Caches 
# And Recreate Then Using ABC Shot Builder Again."""
# note = obj.createStickyNote()
# #customize a sticky note
# note.setName('note_name')
# note.setSize([2, 3])
# note.setPosition([-5, -2])
# note.setText(thetext)
# note.setTextSize(0.15)
# note.setColor(hou.Color(0.635, 0.8, 0.215))
# note.setTextColor(hou.Color(0, 0, 0))