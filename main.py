import sys
import os
import threading
import platform
from datetime import datetime

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu

from utils.util_json import getUser, saveUser, initRealityClientConfig
from utils.util_request import login, register
from utils.util_sys import xrayOn, xrayOff, xrayRestart, proxyOn, proxyOff
from utils.util_static import serverIP

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        UIFunctions.uiDefinitions(self)

        #Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "Fuckfirewall VPN"
        description = "Fuckfirewall VPN - A ease-to-use VPN client"
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True)) # TOGGLE MENU

        self.pages = {"btn_home": widgets.home, "btn_user": widgets.loginPage, "btn_settings": widgets.settingsPage}

        widgets.btn_home.clicked.connect(self.leftBarButtonClick)
        widgets.btn_user.clicked.connect(self.leftBarButtonClick)
        widgets.btn_settings.clicked.connect(self.leftBarButtonClick)

        widgets.minimizeAppBtn.clicked.disconnect()
        widgets.minimizeAppBtn.clicked.connect(self.showSwitch)

        self.initLoginPage()
        self.initSettingsPage()
        self.initFunctionPage()

        widgets.label_website.linkActivated.connect(lambda: QDesktopServices.openUrl(QUrl("http://www.la.fuckfirewall.top")))

        self.show()
        self.initTray()

        widgets.stackedWidget.setCurrentWidget(widgets.loginPage)
        widgets.btn_user.setStyleSheet(UIFunctions.selectMenu(widgets.btn_user.styleSheet()))

    def initTray(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        self.trayMenu = QMenu(self)

        self.showAction = QAction("Hide", self)
        self.proxySwitchAction = QAction("Proxy on", self)
        self.quitAction = QAction("Quit", self)

        self.proxySwitchAction.setEnabled(False)

        self.hideStatus = False
        self.trayMenu.addAction(self.showAction)
        self.trayMenu.addAction(self.proxySwitchAction)
        self.trayMenu.addAction(self.quitAction)

        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

        self.showAction.triggered.connect(self.showSwitch)
        self.proxySwitchAction.triggered.connect(self.proxySwitch)
        self.quitAction.triggered.connect(self.quit)

    def showSwitch(self):
        if self.hideStatus:
            self.showNormal()
            self.showAction.setText('Hide')
        else:
            #self.setWindowFlags(self.windowFlags() | Qt.Tool)
            self.hide()
            self.showAction.setText('Show')
        self.hideStatus = not self.hideStatus

    def initLoginPage(self):
        self.email, self.password = getUser()
        self.proxyIsOn = False
        self.xrayProcess = None

        if self.email:
            widgets.emailInput.setText(self.email)
        else:
            widgets.emailInput.focusInEvent = self.clearEmail

        if self.password:
            widgets.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            widgets.passwordInput.setText(self.password)
        else:
            widgets.passwordInput.focusInEvent = self.clearPasswoard
        
        widgets.btn_login.clicked.connect(self.login)
        widgets.btn_register.clicked.connect(self.register)
        
    def clearEmail(self, event):
        if widgets.emailInput.text() == 'Email':
            widgets.emailInput.clear()
        widgets.emailInput.focusInEvent = None

    def clearPasswoard(self, event):
        if widgets.passwordInput.text() == 'Password':
            widgets.passwordInput.clear()
            widgets.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        widgets.passwordInput.focusInEvent = None

    def leftBarButtonClick(self):
        btn = self.sender()
        btnName = btn.objectName()
        if btnName in self.pages:
            widgets.stackedWidget.setCurrentWidget(self.pages[btnName])
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def closeEvent(self, event):
        self.quit()
    
    def quit(self):
        proxyOff()
        if self.xrayProcess:
            xrayOff(self.xrayProcess.pid)
        self.xrayLogOn = False
        QApplication.quit()

    # -----------------------------------
    # below are methods for functionality
    # -----------------------------------
    @QtCore.Slot()
    def register(self):
        email, password = widgets.emailInput.text(), widgets.passwordInput.text()
        result = register(email, password, 0, serverIP)
        if result == 'Register success.':
            self.login()
        else:
            QtWidgets.QMessageBox.information(self, 'Message', result)

    @QtCore.Slot()
    def login(self) -> None:
        email, password = widgets.emailInput.text(), widgets.passwordInput.text()
        user = login(email, password, serverIP)
        print(user)
        if not user:
            QtWidgets.QMessageBox.information(self, 'Message', 'Login failed.')
            return
        port, uuid, pubkey, shortid, balance, expireOn, referralCode = user['port'], user['uuid'], user['pubkey'], user['shortid'], user['balance'], user['expireOn'], user['referralCode']
        print(port, uuid, pubkey, shortid, balance, expireOn, referralCode)
        saveUser(email, password)
        initRealityClientConfig(serverIP, port, uuid, pubkey, shortid) # TODO
        self.xrayProcess = xrayOn()
        self.xrayLogOn = True

        self.xrayLogUpdateThread = threading.Thread(target=self.xrayLogUpdater)
        self.xrayLogUpdateThread.start()
        self.proxySwitch()

        self.refreshAccountStatus(email, balance, expireOn, referralCode)
        self.proxySwitchAction.setEnabled(True)
        self.userPageSwitch()

    # select function page
    def userPageSwitch(self):
        if self.pages["btn_user"] == widgets.loginPage:
            self.proxySwitchAction.setEnabled(True)
            self.pages["btn_user"] = widgets.functionPage
        else:
            self.proxySwitchAction.setEnabled(False)
            xrayOff(self.xrayProcess.pid)
            self.pages["btn_user"] = widgets.loginPage
        widgets.stackedWidget.setCurrentWidget(self.pages["btn_user"])

    # ---------------------------
    # below are for function page
    # ---------------------------
    def initFunctionPage(self):
        widgets.btn_proxySwitch.clicked.connect(self.proxySwitch)
        widgets.btn_logout.clicked.connect(self.logout)

        current_row = widgets.table_servers.rowCount()

        # 在末尾插入一行
        widgets.table_servers.insertRow(current_row)
        row_data = ["209.141.49.64", "0 ms", "0 mbps"]
        # 设置每个单元格的数据
        for column, data in enumerate(row_data):
            item = QTableWidgetItem(data)
            widgets.table_servers.setItem(current_row, column, item)

        widgets.table_servers.itemClicked.connect(lambda item: widgets.table_servers.selectRow(item.row()))

    def refreshAccountStatus(self, email, balance, expireOn, referralCode):
        widgets.label_currentUser.setText(f'Current user: {email}')
        widgets.label_balance.setText(f'Balance: {balance}')

        expireOn = datetime.now() - datetime.utcnow() + datetime.strptime(expireOn, '%Y-%m-%d %H:%M')
        widgets.label_expireOn.setText(f'Expire on: {expireOn.strftime("%Y-%m-%d %H:%M")}')
        widgets.label_referralCode.setText(f'Referral code: {referralCode}')

    def logout(self):
        self.proxySwitch()
        self.userPageSwitch()

    def proxySwitch(self):
        if self.proxyIsOn:
            widgets.btn_proxySwitch.setText('Proxy On')
            self.proxySwitchAction.setText('Proxy On')
            proxyOff()
        else:
            widgets.btn_proxySwitch.setText('Proxy Off')
            self.proxySwitchAction.setText('Proxy Off')
            proxyOn()
        self.proxyIsOn = not self.proxyIsOn

    # ---------------------------
    # below are for settings page
    # ---------------------------
    def initSettingsPage(self):
        widgets.checkBox_theme.stateChanged.connect(self.switchTheme)

    def switchTheme(self, state):
        themeFile = "themes/py_dracula_light.qss" if state == 0 else "themes/py_dracula_dark.qss"
        UIFunctions.theme(self, themeFile, True)
        AppFunctions.setThemeHack(self)

    def xrayLogUpdater(self):
        while self.xrayLogOn:
            for line in iter(self.xrayProcess.stdout.readline, b''):
                output = line.decode('utf-8')
                widgets.textEdit_xrayLog.append(output.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
