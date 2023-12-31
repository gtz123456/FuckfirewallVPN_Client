# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

block_cipher = None

import sys
PLATFORM = sys.platform
if PLATFORM.startswith('win'):
    resources = 'resources_windows'
    ico = 'images/images/icon_blue.ico'
elif PLATFORM == 'darwin':
    resources = 'resources_macos'
    ico = 'images/images/icon_blue.icns'
else:
    resources = 'resources_linux'
    ico = 'images/images/icon_blue.ico'

a = Analysis(
    ['client.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='client',
)
