#!/bin/bash

FILENAME="HeartView"
CWD=$(pwd)

printf "Compiling App\n" > build.txt

while getopts c:t:s: flag
do
    case "${flag}" in
        c) CLEAR=1;;
        t) PACKAGETYPE=${OPTARG};;
        s) CERTIFICATE=${OPTARG};;
    esac
done

if [[ $CLEAR -eq 1 ]]
then
    printf "\nClearing build and dist folders\n"
    rm -rf ./build/ ./dist/
fi

if [[ $PACKAGETYPE -eq 1 ]]
then
    printf "\nGenerating macOS Distribution from HeartView.spec as single file.\nEnsure that pyenv is running with py3.7.7\n"
    sleep 2
    
    python3 -m PyInstaller --onefile --noconfirm --clean HeartView.spec 2> build.txt
elif [[ $PACKAGETYPE -eq 0 ]]
then
    printf "\nGenerating macOS Distribution from HeartView.spec as single directory.\nEnsure that pyenv is running with py3.7.7\n"
    sleep 2

    python3 -m PyInstaller --onedir --noconfirm --clean HeartView.spec 2> build.txt
fi

if [[ -n $code ]]  
then
    printf "\nCode Signing App...\n"
    codesign -s "$CERTIFICATE" -v dist/HeartView.app --deep
fi

printf "\nFind Distro in \`dist\` folder\n"
