@ECHO OFF
:: Create windows distribution of HeartView

:LocalVars
set filename=HeartView

:EraseDirs
RMDIR /S /Q .\build\ .\dist\

:PyInstaller
pyinstaller.exe ^
    --noconfirm ^
    --onefile ^
    --console ^
    --add-data="README.md;." ^
    --add-data="res\mac_fireball.jpg;res" ^
    --add-data="res\McSCert_Logo.png;res" ^
    --add-data="res\pixel-heart.ico;res" ^
    --log-level=DEBUG ^
    --name=%filename% ^
    --icon=.\res\pixel-heart.ico ^
    heartview_win.spec 1> build.txt