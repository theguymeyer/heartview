@ECHO OFF
:: Create windows distribution of HeartView

:LocalVars
set filename=HeartView

:EraseDirs
RMDIR /S /Q .\build\ .\dist\

:PyInstaller
START /WAIT pyinstaller.exe --noconfirm --onefile --window heartview_win.spec

:CopyImages
MKDIR .\dist\res\
COPY ..\res\McSCert_Logo.png .\dist\res\
COPY ..\res\mac_fireball.jpg .\dist\res\