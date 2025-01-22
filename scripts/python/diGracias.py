import webbrowser
import os
from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui

# Calling UI File
aPath = hou.getenv("AnDLib")
uPath = "scripts/UI"
iPath = "/icons"
UIPath = os.path.join(aPath, uPath)

# Create The Widget Class
class donationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=QtCore.Qt.Window):
        super(donationWidget, self).__init__(parent, flags)
        ui_file = UIPath + "/DonationUI.ui"
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setWindowTitle("Requesting For Donation")
        self.setWindowIcon(QtGui.QIcon(aPath + iPath + "/icons8-donate-64.png"))

        # Connecting Buttons
        self.ui.buyCoffee.clicked.connect(self.buyCoffeeClicked)
        self.ui.buyCoffee.setIcon(
            QtGui.QIcon((aPath + iPath + "/icons8-donate-64.png"))
        )
        self.ui.linkTree.clicked.connect(self.linkTreeClicked)
        self.ui.linkTree.setIcon(
            QtGui.QIcon((aPath + iPath + "/linktree_brandfetch.svg"))
        )

    # Setup "Link in Bio" Button
    def linkTreeClicked(self):
        webbrowser.open("https://linktr.ee/andcgi", new=0, autoraise=True)
        self.close()

    # Setup "Cup of Coffee" Button
    def buyCoffeeClicked(self):
        webbrowser.open(
            "https://www.paypal.com/paypalme/DJDhrub", new=0, autoraise=True
        )
        self.close()

winDon = donationWidget()
winDon.show()
