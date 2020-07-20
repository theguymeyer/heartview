# PyQt5 Testing Interface UI - HeartView

This UI is main interface of the remote testing station. Users can build test routines using the **Control Panel** and see the pacing information in using the **Real Time Plots**

## Components

### Control Panel

The user can uses this UI component to build test routines. The user can set pacing information with the available buttons and dispatch the test routine to the testing controller (MCU: nucleo-f446RE in this implementation). The data is transmitted to the testing controller via serial and is updated in real-time.

### Real Time Plots

The user can use this UI component to see the resulting waveforms they generated using their pacemaker, along with the testing routine currently running on the Testing Controller. The objective is to allow the user to compare waveforms and ensure that their operation is correct. As a result, timing is strict and must match the actual MCU operation with high accuracy. 

## Error Handling

No device connected upon serial start - upon boot the system will try to connect to the testing controller via serial. If the device is not found on the given port then the status bar will be updated

No serial device connected upon send - if the user tries to send a test routine when no device is connected then the serial.Exception is caught and the status bar is updated.

## Supporting Libraries

The following are a set of Python3 Libraries that enable the functionality in this application.

1. [PyQt5 5.15.0](https://pypi.org/project/PyQt5/)
... Frameworks for all UI elements, and serial communication
... ``pip3 install PyQt5``
2. [pyqtgraph](https://pyqtgraph.readthedocs.io/en/latest/index.html)
... Used to generate responsive real-time plots
... ``pip3 install pyqtgraph`` (source [here](https://pypi.org/project/pyqtgraph/))
3. [QtAwesome](https://pypi.org/project/QtAwesome/)
... Used for button and label icons
... ``pip3 install QtAwesome``
4. [fpdf](https://pypi.org/project/fpdf/)
... Used to generate printer-friendly PDF report
... ``pip3 install fpdf``
5. [numpy](https://pypi.org/project/numpy/)
... Mathematical computation
... ``pip3 install numpy``
6. Standard Python3 Libraries: sys, os


## Distribution

Yet to be registered, this app is intended to be licensed under the GPL. As such it is possible to distribute HeartView due to its dependencies on PyQt5 and [fbs](https://build-system.fman.io/) (build system).

Currently in development, the distribution bundler is PyInstaller.

According to the PyInstaller documentation the end users "do not need to have Python installed at all"[\[docs\]](https://readthedocs.org/projects/pyinstaller/downloads/pdf/latest/). Good to note! In addition the docs note that in order to generate executables for a different OS, a different version of Python, or a 32-bit/64-bit machine then PyInstaller must be run on that platform. The first distribution is for macOS Catalina 15.5.0

### Icons

Application icon (heartbeat.ico) found [here](https://www.iconarchive.com/show/medical-health-icons-by-graphicloads/heart-beat-icon.html)