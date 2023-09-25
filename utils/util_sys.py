import os
import sys
import subprocess

def source_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
 
BASE_DIR = os.path.join(source_path(''), 'resources')
XRAY_PATH = os.path.join(BASE_DIR, 'xray', 'xray')

PLATFORM = sys.platform
if PLATFORM.startswith('win'):
    PLATFORM = 'windows'
    BASE_DIR = os.path.join(source_path(''), 'resources_windows')
    import winreg
elif PLATFORM == 'darwin':
    PLATFORM = 'macos'
    BASE_DIR = os.path.join(source_path(''), 'resources_macos')
else:
    PLATFORM = 'linux'
    BASE_DIR = os.path.join(source_path(''), 'resources_linux')

def proxySwitchWindows(open=True):
    proxy = "socks=127.0.0.1:1081"
    root = winreg.HKEY_CURRENT_USER
    proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    kv_Enable = [
        (proxy_path, "ProxyEnable", 1, winreg.REG_DWORD),
        (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]

    kv_Disable = [
        (proxy_path, "ProxyEnable", 0, winreg.REG_DWORD),
        # (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]
    if open:
        kv = kv_Enable
    else:
        kv = kv_Disable
    for keypath, value_name, value, value_type in kv:
        hKey = winreg.CreateKey(root, keypath)
        winreg.SetValueEx(hKey, value_name, 0, value_type, value)

def proxyOn():
    if PLATFORM == 'windows':
        proxySwitchWindows()
    elif PLATFORM == 'macos':
        setSocks = 'networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 1081'
        os.system(setSocks)

        proxyOn = 'networksetup -setsocksfirewallproxystate Wi-Fi on'
        os.system(proxyOn)
    else:
        pass #TODO


def proxyOff():
    if PLATFORM == 'windows':
        proxySwitchWindows(False)
    elif PLATFORM == 'macos':
        proxyOff = 'networksetup -setsocksfirewallproxystate Wi-Fi off'
        os.system(proxyOff)
    else:
        pass #TODO

def xrayOn():
    xrayProcess = subprocess.Popen([os.path.join(BASE_DIR, 'xray', 'xray')], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    return xrayProcess#.pid

def xrayOff(pid):
    if PLATFORM == 'windows':
        os.system('taskkill /f /t /im xray.exe')
    else:
        os.popen('kill ' + str(pid))

def xrayRestart(pid):
    xrayOff(pid)
    return xrayOn()