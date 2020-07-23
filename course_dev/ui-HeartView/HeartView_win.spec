# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import os
import ntpath
import PyQt5


a = Analysis(["mainwindow.py"],
             pathex=["C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView", os.path.join(ntpath.dirname(PyQt5.__file__), 'Qt', 'bin')],
             binaries=[],
             datas=[
                ("C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView\\README.md", "."), 
                ("C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView\\res\\mac_fireball.jpg", "res"), 
                ("C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView\\res\\McSCert_Logo.png", "res"), 
                ("C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView\\res\\pixel-heart.ico", "res")],
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
          [],
          exclude_binaries=True,
          name='mainwindow',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True,
          icon="C:\\Users\\Guy\\Documents\\pacemaker\\heartview\\course_dev\\ui-HeartView\\res\\pixel-heart.ico" )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name="HeartView_win")