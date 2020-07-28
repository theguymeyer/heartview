#!/bin/bash

FILENAME="HeartView"
CWD=$(pwd)

printf "Compiling App\n" > build.txt

while getopts c:t:s: flag
do
    case "${flag}" in
        c) clearDirs=1;;
        t) packageType=${OPTARG};;
        s) code=${OPTARG};;
    esac
done

if [[ $clearDirs -eq 1 ]]
then
    printf "\nClearing build and dist folders\n" >> build.txt
    rm -rf ./build/ ./dist/
fi

if [[ $packageType -eq 1 ]]
then
    printf "\nGenerating macOS Distribution from HeartView.spec as single file.\nEnsure that pyenv is running with pyqt-venv-py3.7.7\n\n" >> build.txt
    sleep 2
    
    python3 -m PyInstaller --onefile --console --noconfirm HeartView.spec 2> build.txt
elif [[ $packageType -eq 0 ]]
then
    printf "\nGenerating macOS Distribution from HeartView.spec as single directory.\nEnsure that pyenv is running with pyqt-venv-py3.7.7\n\n" >> build.txt
    sleep 2

    python3 -m PyInstaller --onedir --console --noconfirm HeartView.spec 2> build.txt
fi

if [[ -n $code ]]  
then
    printf "\n\nCode Signing App..." >> build.txt
    codesign -f -s "Apple Development: Guy Meyer ($code)" dist/HeartView.app --deep
fi

printf "\n\nFind Distro in \`dist\` folder\n" >> build.txt
