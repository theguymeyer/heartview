# 1. Install Drivers & Tools
## Windows
    - ST-Link Driver: https://www.st.com/en/development-tools/stsw-link009.html 
## Linux
    - udev rules for stm32 board
## Windows, Linux, macOS
    - JLink Software Pack https://www.segger.com/downloads/jlink#J-LinkSoftwareAndDocumentationPack

# 2. Replace the bootloader on the K64F
    - Download JLink firmware for k64f https://www.segger.com/downloads/jlink/OpenSDA_FRDM-K64F
    - Hold the reset button while connecting the board to you computer
    - A bootloader drive/volume should show up
    - Copy the .bin file to the bootloader drive

# 3. Install Python dependencies (Python 3)
```sh
    pip3 install pipenv
    pipenv install
    pipenv run pyocd pack -i stm32f446re
```

# 4. Run the tests
```sh
    pipenv run python ./main.py
```