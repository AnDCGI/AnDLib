import sys
import os
import glob
import time
from datetime import date
from pathlib import Path
import getpass
import hou
from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui

# Setting The Global Path
creationDate = date.today()
aPath = hou.getenv("AnDCGI")
rPath = "scripts/UI"
iPath = "/icons"
UIPath = os.path.join(aPath, rPath)
gPath = "W:/01prj/AAJ/prod/shotpub/"
obj = hou.node("/obj")
version = "1.0.1"


#Creating The Widget
class ShotBuilder(QtWidgets.QWidget):
    def __init__(self):
        super(ShotBuilder, self).__init__()
        ui_file = UIPath + "/CacheBuild.ui"
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        self.setWindowTitle("Alembic Shot Builder "
                            + version + " - Python 3")
        self.setWindowIcon(QtGui.QIcon(
            aPath + iPath + "/icons8-board-64.png"))
        self.collect()

# Connecting All Three Buttons
        self.ui.buildBtn.clicked.connect(self.buildBtnPush)
#        self.ui.updateBtn.clicked.connect(self.updateBtnPush)
        self.ui.doneBtn.clicked.connect(self.doneButtonPush)

# Connecting Spin Box Values
        self.ui.spbxEP.valueChanged.connect(self.collect)
        self.ui.spbxSQ.valueChanged.connect(self.collect)
        self.ui.spbxSH.valueChanged.connect(self.collect)

# Manipulating Spin Box Values
    def collect(self):
        self.epiNum = "EP" + str(self.ui.spbxEP.value()).zfill(3) + "/"
        self.seqNum = "SQ" + str(self.ui.spbxSQ.value()).zfill(3) + "/"
        self.shoNum = "SH" + str(self.ui.spbxSH.value()).zfill(3) + "/"
# Creating The Directory Variables
        self.filesDirectory = (gPath + self.epiNum
                               + self.seqNum + self.shoNum + "data/cache/")
        self.camDirectory = (gPath + self.epiNum
                             + self.seqNum + self.shoNum + "data/cam/")
        self.fileType = "/*.abc"
        self.bABC = "\\abc\\"
        self.aCache = "\\cache\\"

# The Shot Building Function
    def buildBtnPush(self):
        # Start The Clock
        start_time = time.time()
# Creating Scene Scale Null
        nullObj = obj.createNode("null", "sceneScale")
# Hiding Extra Parameters & Setting Some
        nullObj.setParms({"picking": 0, "dcolorr": 1, "dcolorg": 0.175,
                          "dcolorb": 0, "displayicon": 2, "controltype": 6})
        nullObjTG = nullObj.parmTemplateGroup()
        nullObjTG.hideFolder("Render", True)
        nullObjTG.hideFolder("Misc", True)
        nullObjTG.hide((nullObjTG.find("xOrd")), True)
        nullObjTG.hide((nullObjTG.find("rOrd")), True)
        nullObjTG.hide((nullObjTG.find("t")), True)
        nullObjTG.hide((nullObjTG.find("r")), True)
        nullObjTG.hide((nullObjTG.find("s")), True)
        nullObjTG.hide((nullObjTG.find("p")), True)
        nullObjTG.hide((nullObjTG.find("pr")), True)
        nullObjTG.hide((nullObjTG.find("pre_xform")), True)
        nullObjTG.hide((nullObjTG.find("keeppos")), True)
        nullObjTG.hide((nullObjTG.find("childcomp")), True)
        nullObjTG.hide((nullObjTG.find("constraints_on")), True)
        nullObj.setParmTemplateGroup(nullObjTG)
# Getting The Paths Of The ABC File
        folders = Path(self.filesDirectory)
        for filePaths in folders.iterdir():
            filePaths = glob.glob(str(filePaths) + "**"
                                  + "/abc" + self.fileType, recursive=True)
            latestFilePaths = max(filePaths, key=os.path.getctime)
# Getting The Names Of The Files
            fileNames = latestFilePaths.partition(self.bABC)[0]
            fileNames = fileNames.partition(self.aCache)[2]
            geoNodeNames = latestFilePaths.partition(self.bABC)[2]
            geoNodeNames = geoNodeNames[:-4]
            latestFilePaths = latestFilePaths.replace("\\", "/")
# Creating The Nodes On GEO Level
            geoNode = obj.createNode("geo", fileNames)
            geoNode.setColor(hou.Color((0.15, 0.20, 0.25)))
            geoNode.setUserData('nodeshape', "tabbed_right")
            geoNode.setInput(0, nullObj, 0)
# Creating The Nodes On SOP Level
            nullNode = geoNode.createNode("null", "OUT")
            alembicNode = geoNode.createNode("alembic", geoNodeNames)
            updateFilePath = alembicNode.parm("fileName")
            updateFilePath.set(latestFilePaths)
            nullNode.setInput(0, alembicNode, 0)
            nullNode.setColor(hou.Color((0.125, 0.125, 0.25)))
            geoNode.layoutChildren()
# Getting The Path Of The Camera
        folders = Path(self.camDirectory)
        for shotCamera in folders.iterdir():
            shotCamera = glob.glob(
                str(shotCamera) + "**" + "/abc" + self.fileType, recursive=True)
            latestCameraPath = max(shotCamera, key=os.path.getctime)
# Getting The Name Of The Camera
            cameraName = latestCameraPath.partition(self.bABC)[2]
            cameraName = cameraName[:-4]
            latestCameraPath = latestCameraPath.replace("\\", "/")
# Creating The Camera Node In Houdini
        cameraNode = obj.createNode("alembicarchive", cameraName)
        updateCameraPath = cameraNode.parm("fileName").set(latestCameraPath)
        refreshHierarchy = cameraNode.parm("buildHierarchy").pressButton()
        cameraNode.setInput(0, nullObj, 0)
# Some Variable For Networkbox Comments
        userName = getpass.getuser()
        userName = userName.upper()
        userName = userName[0:1] + userName[-1:]
        buildDate = creationDate.strftime("%d %b %Y ")
        nbCom = cameraName[4:-17] + " FX Scene ◆ Build " + \
            buildDate + "◆ " + userName
# Layot Obj Level Nodes
        obj.layoutChildren()
# Selecting All OBJ Level Nodes
        for i in obj.children():
            i.setSelected("on")
# Putting The Selection In Var
        sel = hou.selectedNodes()[0]
        all = hou.selectedNodes()
# Position Of Network Box From Selection
        pos = sel.position()
        parent = sel.parent()
# Creating Network Box
        box = parent.createNetworkBox()
        box.setPosition(sel.position())
# Adding All Nodes
        for node in all:
            box.addItem(node)
# Box Parms
        box.setColor(hou.Color(0.095, 0.35, 0.25))
        box.setComment(nbCom)
# Fit Box
        box.fitAroundContents()
        box.resize(hou.Vector2(5, 0.5))
# Time taken To Run The Scirpt
        timeTaken = ("%s Seconds!" % (time.time() - start_time))
# Some Message
        hou.ui.displayMessage("Zoop! Now That's Some Flash In Action \nCache Building Done In Just "
                              + timeTaken + "\nPlease Save The File Using Script.")
# Close The UI When Pressing Done

    def doneButtonPush(self):
        self.close()
        globals().clear()


alembicShotBuilder = ShotBuilder()
alembicShotBuilder.show()
