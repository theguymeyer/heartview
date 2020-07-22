# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mainwindow.py'],
             pathex=['/Users/guy/Documents/heartview/course_dev/ui-HeartView'],
             binaries=[],
             datas=[
                ('/Users/guy/Documents/heartview/course_dev/ui-HeartView/README.md', '.'), 
                ('/Users/guy/Documents/heartview/course_dev/ui-HeartView/res/mac_fireball.jpg', 'res'), 
                ('/Users/guy/Documents/heartview/course_dev/ui-HeartView/res/McSCert_Logo.png', 'res'), 
                ('/Users/guy/Documents/heartview/course_dev/ui-HeartView/res/pixel-heart.icns', 'res')],
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
          [],
          exclude_binaries=True,
          name='mainwindow',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True,
          icon='/Users/guy/Documents/heartview/course_dev/ui-HeartView/res/pixel-heart.icns' )
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
            icon='res/pixel-heart.icns',
            bundle_identifier='com.guymeyer.HeartView.ui',
            info_plist={
                'NSPrincipalClass': 'NSApplication', 
                'NSHighResolutionCapable': 'True',
                'NSAppleScriptEnabled': False, 
                'LSBackgroundOnly': False,
                'CFBundleDocumentTypes': [{
                    'CFBundleTypeName': 'py', 
                    'CFBundleTypeIconFile': 'res/pixel-heart.icns', 
                    'LSItemContentTypes': ['com.guymeyer.HeartView.ui'], 
                    'LSHandlerRank': 'Owner'
                }] 
            })