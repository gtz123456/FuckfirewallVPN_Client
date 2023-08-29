import sys
import os

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtCore import Qt
from utils.util_json import getUser, saveUser, initRealityClientConfig
from utils.util_request import login
from utils.util_sys import xrayOn, xrayOff, proxyOn, proxyOff

class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Fuckfirewall VPN")
        self.resize(245, 170)
        self.email, self.password = getUser()
        self.proxyIsOn = False
        self.xrayProcess = None
        self.setup_ui()

    def setup_ui(self) -> None:

        self.emailInput = QtWidgets.QLineEdit(self)
        self.emailInput.move(60, 40)
        if self.email:
            self.emailInput.setText(self.email)
        else:
            self.emailInput.setText("Email")
        self.emailInput.selectionChanged.connect(self.clearEmail)

        self.passwordInput = QtWidgets.QLineEdit(self)
        self.passwordInput.move(60, 70)
        if self.password:
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.passwordInput.setText(self.password)
        else:
            self.passwordInput.setText("Password")
        self.passwordInput.selectionChanged.connect(self.clearPasswoard)
        
        icon = QtGui.QIcon("../../../Resources/Icons/Python_128px.png")
        
        self.button = QtWidgets.QPushButton(icon, "Login", self)
        self.button.resize(80, 30)
        self.button.move(86, 95)
        self.button.clicked.connect(self.login)  # type: ignore

    @QtCore.Slot()
    def proxySwitch(self):
        if self.proxyIsOn:
            self.button.setText('Proxy On')
            proxyOff()
            self.proxyIsOn = False
        else:
            self.button.setText('Proxy Off')
            proxyOn()
            self.proxyIsOn = True

    @QtCore.Slot()
    def login(self) -> None:
        email, password = self.emailInput.text(), self.passwordInput.text()
        user = login(email, password, 'http://lv.fuckfirewall.top')
        if not user:
            QtWidgets.QMessageBox.information(self, 'Message', 'Login failed.')
            return
        address, port, uuid, pubkey, shortid = user

        self.button.clicked.disconnect()
        self.button.clicked.connect(self.proxySwitch)
        saveUser(email, password)
        initRealityClientConfig('209.141.49.64', port, uuid, pubkey, shortid)
        self.xrayProcess = xrayOn()
        self.proxySwitch()
        
    def clearEmail(self):
        if self.emailInput.text() == 'Email':
            self.emailInput.clear()
        self.emailInput.selectionChanged.disconnect(self.clearEmail)

    def clearPasswoard(self):
        if self.passwordInput.text() == 'Password':
            self.passwordInput.clear()
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordInput.selectionChanged.connect(self.clearPasswoard)

    def closeEvent(self, event):
        proxyOff()
        if self.xrayProcess:
            xrayOff(self.xrayProcess.pid)
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())