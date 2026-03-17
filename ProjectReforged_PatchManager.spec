# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for Project Reforged Patch Manager
# Produces a single .exe with no console window.
#
# Build with:  pyinstaller ProjectReforged_PatchManager.spec

block_cipher = None

a = Analysis(
    ['ProjectReforged_PatchManager.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'urllib.request',
        'urllib.error',
        'queue',
        'threading',
        'json',
        'pathlib',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'PIL', 'pandas',
        'scipy', 'setuptools',
        'xml', 'pydoc', 'doctest', 'unittest',
    ],
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
    name='ProjectReforged_PatchManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,           # compress with UPX if available (smaller exe)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # no black console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # uncomment and add an .ico file if you have one
)
