import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[
       # ('/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0', '_internal/libpython3.12.so.1.0'),
    ],
    datas=[
        ('src/code_compiler/config/config.yaml', 'src/code_compiler/config'),
        ('src/code_compiler/config/instructions.yaml', 'src/code_compiler/config'),

        ('src/stack_machine/config/config.yaml', 'src/stack_machine/config'),
        ('src/stack_machine/config/instructions.yaml', 'src/stack_machine/config'),
        ('src/stack_machine/config/mc.yaml', 'src/stack_machine/config'),
        ('src/stack_machine/bin_mem', 'src/stack_machine/bin_mem'),
    ],
    hiddenimports=collect_submodules('yaml'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='stack-machine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='stack-machine'
)
