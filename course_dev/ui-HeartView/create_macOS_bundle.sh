#!/bin/bash

FILENAME="HeartView"
CWD=$(pwd)

while getopts c:s: flag
do
    case "${flag}" in
        c) clearDirs=${OPTARG};;
        s) clearSpec=${OPTARG};;
    esac
done

if [[ $clearDirs -eq 1 ]]
then
    rm -rf ./build ./dist
fi

if [[ $clearSpec -eq 1 ]]
then
    rm "$FILENAME.spec"
fi

printf "\nGenerating macOS Distribution from HeartView.spec\nEnsure that pyenv is running with pyqt-venv-py3.7.7\n\n"
sleep 2

python3 -m PyInstaller \
    --noconfirm \
    --onedir \
    --console \
    --add-data="$CWD/README.md:." \
    --add-data="$CWD/res/mac_fireball.jpg:res" \
    --add-data="$CWD/res/McSCert_Logo.png:res" \
    --add-data="$CWD/res/heartbeat.ico:res" \
    --log-level=DEBUG \
    --osx-bundle-identifier="Apple Development: Guy Meyer (VVJQ6Y9Y2X)" \
    --name="$FILENAME" \
    --icon="$CWD/res/heartbeat.ico" \
    mainwindow.py 2> build.txt
    
printf "\n\nCode Signing App..."

codesign -f -s "Apple Development: Guy Meyer (VVJQ6Y9Y2X)" dist/HeartView --deep

printf "\n\nFind Distro in \`dist\` folder\n"
