import os
import sys
import subprocess

def source_path(relative_path):
    # 是否Bundle Resource
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
elif PLATFORM == 'darwin':
    PLATFORM = 'macos'
else:
    PLATFORM = 'linux'

def proxyOn():
    if PLATFORM == 'windows':
        sethttp = 'netsh winhttp set proxy 127.0.0.1 1080'
        os.system(sethttp)
    elif PLATFORM == 'macos':
        setSocks = 'networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 1081'
        os.system(setSocks)

        proxyOn = 'networksetup -setsocksfirewallproxystate Wi-Fi on'
        os.system(proxyOn)
    else:
        pass #TODO


def proxyOff():
    if PLATFORM == 'windows':
        proxyOff = 'netsh winhttp reset proxy'
        os.system(proxyOff)
    elif PLATFORM == 'macos':
        proxyOff = 'networksetup -setsocksfirewallproxystate Wi-Fi off'
        os.system(proxyOff)
    else:
        pass #TODO

def xrayOn():
    xrayProcess = subprocess.Popen([os.path.join(BASE_DIR, 'xray', 'xray')], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return xrayProcess#.pid

def xrayOff(pid):
    os.popen('kill ' + str(pid))

def xrayRestart(pid):
    xrayOff(pid)
    return xrayOn()