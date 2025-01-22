# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import platform
import tkinterdnd2
from pathlib import Path

# Get tkdnd path directly from the package
TKDND_BASE = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd')

# Determine the correct platform folder
if platform.system() == 'Windows':
    if platform.machine().endswith('64'):
        TKDND_PLATFORM = 'win-x64'
    else:
        TKDND_PLATFORM = 'win-x86'

# Full path to platform-specific tkdnd files
TKDND_PATH = os.path.join(TKDND_BASE, TKDND_PLATFORM)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # FFmpeg
        ('src/ffmpeg.exe', '.'),
        # TkDnD - platform specific files to root
        (TKDND_PATH, '.'),
    ],
    hiddenimports=[
        'tkinterdnd2',
        'tkinter',
        'tkinter.ttk',
        'pydub',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='M4AConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Changed to False for final version
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/basic-icon.ico']
)