# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import sys
PLATFORM = sys.platform
if PLATFORM.startswith('win'):
    resources = 'resources_windows'
elif PLATFORM == 'darwin':
    resources = 'resources_macos'
else:
    resources = 'resources_linux'

a = Analysis(
    ['client.py'],
    pathex=[],
    binaries=[],
    datas=[(resources, resources)],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='client.app',
    icon='ico.icns',
    bundle_identifier=None,
)
