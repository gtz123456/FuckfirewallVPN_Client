import sys
import os
import platform

from PySide6 import QtGui, QtCore, QtWidgets
from utils.util_json import getUser, saveUser, initRealityClientConfig
from utils.util_request import getUserConfig
from utils.util_sys import xrayOn, xrayOff, proxyOn, proxyOff
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

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Fuckfirewall VPN"
        description = "Fuckfirewall VPN - A ease-to-use VPN client"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True)) # TOGGLE MENU

        UIFunctions.uiDefinitions(self)

        self.pages = {"btn_home": widgets.home, "btn_widgets": widgets.widgets, "btn_user": widgets.loginPage, "btn_settings": widgets.settingsPage}

        widgets.btn_home.clicked.connect(self.leftBarButtonClick)
        widgets.btn_user.clicked.connect(self.leftBarButtonClick)
        widgets.btn_settings.clicked.connect(self.leftBarButtonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        self.initLoginPage()
        self.initSettingsPage()
        self.initFunctionPage()

        widgets.label_website.linkActivated.connect(lambda: QDesktopServices.openUrl(QUrl("http://www.fuckfirewall.top")))

        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    def initLoginPage(self):
        self.email, self.password = getUser()
        self.proxyIsOn = False
        self.xrayProcess = None

        if self.email:
            widgets.emailInput.setText(self.email)
        widgets.emailInput.focusInEvent = self.clearEmail

        if self.password:
            widgets.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            widgets.passwordInput.setText(self.password)
        widgets.passwordInput.focusInEvent = self.clearPasswoard
        
        widgets.btn_login.clicked.connect(self.login)
        widgets.btn_register.clicked.connect(self.register)
        
    def clearEmail(self, event):
        if widgets.emailInput.text() == 'Email':
            widgets.emailInput.clear()
        widgets.emailInput.selectionChanged.disconnect()

    def clearPasswoard(self, event):
        if widgets.passwordInput.text() == 'Password':
            widgets.passwordInput.clear()
            widgets.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        widgets.passwordInput.selectionChanged.connect(self.clearPasswoard)

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
        proxyOff()
        if self.xrayProcess:
            xrayOff(self.xrayProcess.pid)
        event.accept()

    # -----------------------------------
    # below are methods for functionality
    # -----------------------------------
    @QtCore.Slot()
    def register(self):
        return

    @QtCore.Slot()
    def login(self) -> None:
        email, password = widgets.emailInput.text(), widgets.passwordInput.text()
        user = getUserConfig(email, password, serverIP)
        if not user:
            QtWidgets.QMessageBox.information(self, 'Message', 'Login failed.')
            return
        port, uuid, pubkey, shortid = user

        saveUser(email, password)
        initRealityClientConfig(serverIP, port, uuid, pubkey, shortid)
        self.xrayProcess = xrayOn()
        self.proxySwitch()
        self.userPageSwitch()

        # select function page
    def userPageSwitch(self):
        self.pages["btn_user"] = widgets.functionPage if self.pages["btn_user"] == widgets.loginPage else widgets.loginPage
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
        row_data = ["第三行数据-列1", "第三行数据-列2", "第三行数据-列3"]
        # 设置每个单元格的数据
        for column, data in enumerate(row_data):
            item = QTableWidgetItem(data)
            widgets.table_servers.setItem(current_row, column, item)

        widgets.table_servers.itemClicked.connect(lambda item: widgets.table_servers.selectRow(item.row()))

    def logout(self):
        self.userPageSwitch()

    def proxySwitch(self):
        if self.proxyIsOn:
            widgets.btn_proxySwitch.setText('Proxy On')
            proxyOff()
            self.proxyIsOn = False
        else:
            widgets.btn_proxySwitch.setText('Proxy Off')
            proxyOn()
            self.proxyIsOn = True

    # ---------------------------
    # below are for settings page
    # ---------------------------
    def initSettingsPage(self):
        widgets.checkBox_theme.stateChanged.connect(self.switchTheme)

    def switchTheme(self, state):
        themeFile = "themes/py_dracula_light.qss" if state == 0 else "themes/py_dracula_dark.qss"
        UIFunctions.theme(self, themeFile, True)
        AppFunctions.setThemeHack(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
