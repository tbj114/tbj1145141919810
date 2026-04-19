import os
import sys
from pathlib import Path

try:
    import PyInstaller
    from PyInstaller.__main__ import run
except ImportError:
    print("PyInstaller not found. Please install it first: pip install pyinstaller")
    sys.exit(1)

project_root = Path(__file__).parent
spec_path = project_root / "AxaltyX.spec"

spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app/locale', 'app/locale'),
        ('app/gui/styles', 'app/gui/styles'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AxaltyX',
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
    icon=None,
)
'''

with open(spec_path, 'w', encoding='utf-8') as f:
    f.write(spec_content)

print("Spec file created successfully.")
print("Now building AxaltyX...")

run([
    '--clean',
    '--noconfirm',
    str(spec_path)
])

print("Build completed!")
