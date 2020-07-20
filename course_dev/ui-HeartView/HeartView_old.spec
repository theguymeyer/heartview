# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

a = Analysis(['mainwindow.py'],
             pathex=['/Users/guy/Documents/pacemaker/course_dev/ui-HeartView'],
             binaries=[],
             datas=[('README.md', '.'), ('res/mac_fireball.jpg', 'res'), ('res/McSCert_Logo.png', 'res')],
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
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='res/heartbeat.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='HeartView')
app = BUNDLE(exe,
             name='HeartView.app',
             icon='res/heartbeat.ico',
             bundle_identifier='com.guymeyer.heartview.ui',
             info_plist={
                'NSPrincipalClass': 'NSApplication', 
                'NSAppleScriptEnabled': False, 
                'CFBundleDocumentTypes': [{
                    'CFBundleTypeName': 'py', 
                    'CFBundleTypeIconFile': 'res/heartbeat.ico', 
                    'LSItemContentTypes': ['com.guymeyer.heartview.ui'], 
                    'LSHandlerRank': 'Owner'
                }] 
            })
