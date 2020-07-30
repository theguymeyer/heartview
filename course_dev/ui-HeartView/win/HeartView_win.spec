# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mainwindow_win.py'],
             pathex=['C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView'],
             binaries=[],
             datas=[('README.md', '.'), ('..\\res\\mac_fireball.jpg', 'res'), ('..\\res\\McSCert_Logo.png', 'res'), ('..\\res\\pixel-heart.ico', 'res')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='HeartView',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='..\\res\\pixel-heart.ico')
