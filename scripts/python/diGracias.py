import webbrowser
#import hou
import os
from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui

# Calling UI File & Some Modification / Create The Widget Class

aPath = hou.getenv("AnDCGI")
uPath = "scripts/UI"
iPath = "/icons"
UIPath = os.path.join(aPath, uPath)

class donationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=QtCore.Qt.Window):
        super(donationWidget, self).__init__(parent, flags)
        ui_file = UIPath + "/DonationUI.ui"
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setWindowTitle("Requesting For Donation")
        self.setWindowIcon(QtGui.QIcon(
             aPath + iPath + "/icons8-donate-64.png"))

# Connecting Buttons
        self.ui.visitGit.clicked.connect(self.visitGitClicked)
        self.ui.buyCoffee.clicked.connect(self.buyCoffeeClicked)

# Setup "Me On GitHub" Button
    def visitGitClicked(self):
        webbrowser.open("https://github.com/andcgi", new=0, autoraise=True)
        self.close()
# Setup "Buy Me A Coffee" Button

    def buyCoffeeClicked(self):
        webbrowser.open("https://www.paypal.com/paypalme/DJDhrub",
                        new=0, autoraise=True)
        self.close()


winDon = donationWidget()
winDon.show()
