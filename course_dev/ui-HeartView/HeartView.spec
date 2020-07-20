# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mainwindow.py'],
             pathex=[
                '/usr/local/lib/python3.7/site-packages/PyQt5/Qt/plugins/imageformats/',
                '/Users/guy/Documents/pacemaker/course_dev/ui-HeartView',
                '/Users/guy/Documents/pacemaker/course_dev/ui-HeartView/lib'],
             binaries=[],
             datas=[
                ('/Users/guy/Documents/pacemaker/course_dev/ui-HeartView/README.md', '.'), 
                ('/Users/guy/Documents/pacemaker/course_dev/ui-HeartView/res/mac_fireball.jpg', 'res'), 
                ('/Users/guy/Documents/pacemaker/course_dev/ui-HeartView/res/McSCert_Logo.png', 'res'), 
                ('/Users/guy/Documents/pacemaker/course_dev/ui-HeartView/res/heartbeat.ico', 'res')],
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
          name='HeartView',
          debug=1,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True , icon='/Users/guy/Documents/pacemaker/course_dev/ui-HeartView/res/heartbeat.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='HeartView')
app = BUNDLE(coll,
            name='HeartView.app',
            icon='res/heartbeat.ico',
            bundle_identifier='com.guymeyer.heartview.ui',
            info_plist={
                'NSPrincipalClass': 'NSApplication', 
                'NSHighResolutionCapable': 'True',
                'NSAppleScriptEnabled': False, 
                'CFBundleDocumentTypes': [{
                    'CFBundleTypeName': 'py', 
                    'CFBundleTypeIconFile': 'res/heartbeat.ico', 
                    'LSItemContentTypes': ['com.guymeyer.heartview.ui'], 
                    'LSHandlerRank': 'Owner'
                }] 
            })
