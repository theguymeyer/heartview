import sys, threading

from PyQt5 import QtCore, QtWidgets, QtGui  # Qt basics

# Plotting packages
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import numpy as np  # math package
try:
    import qtawesome as qta # fontawesome
except:
    print("unable to upload QtAwesome Library")


# import a custom modules
from lib.slider import *
from lib.plotter import *
from lib.serial_interface import *
from lib.toggle_switch import *
from lib.printer import *
from lib.tutorial import *
# from lib.helper_functions import *

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        MainWindow.setObjectName(self, "MainWindow")
        MainWindow.resize(self, 1662, 512)
        
        print("Booting HeartView (macOS)...")

        # Create central widget
        self.centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralWidget) 
        self.centralWidget.setObjectName("centralWidget")
        self.setWindowTitle("HeartView - Heart Simulator")

        # setup main layout
        self.mainLayout = QtGui.QHBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Tutorial Window
        self.tr = TutorialWindow(self)

        # Printer Window
        self.pr = PrinterWindow(self)

        ##  --------- START -- Icons and Images  ---------  

        # Create McSCert Logo
        self.logoMcSCertLabel = QtWidgets.QLabel(self)
        pixmap1 = QtGui.QPixmap(QtCore.QCoreApplication.applicationDirPath() + '/res/McSCert_Logo.png')
        pixmap1 = pixmap1.scaledToHeight(70)
        self.logoMcSCertLabel.setPixmap(pixmap1)
        
        # Create Mac Eng Logo
        self.logoMacEngLabel = QtWidgets.QLabel(self)
        pixmap2 = QtGui.QPixmap(QtCore.QCoreApplication.applicationDirPath() + '/res/mac_fireball.jpg')
        pixmap2 = pixmap2.scaledToHeight(70)
        self.logoMacEngLabel.setPixmap(pixmap2)

        ##  --------- END -- Icons and Images  ---------  

        ##  --------- START -- Control Panel Widgets  ---------  

        # Generic Setup
        headerFont = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        headerFont.setUnderline(True)
        labelFont = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        buttonFont = QtGui.QFont("Arial", 16, QtGui.QFont.Bold)
        smallLabelFont = QtGui.QFont("Arial", 16)

        self.hcLabel = QtWidgets.QLabel("Natural Heart Characteristics")
        self.hcLabel.setFont(headerFont)

        # Atrium
        self.atrLabel = QtWidgets.QLabel("Natural Atrium")
        self.atrLabel.setFont(labelFont)
        self.atrSliderLabel = QtWidgets.QLabel("Pulse Width (ms):")
        self.atrSliderLabel.setFont(smallLabelFont)
        self.atrPushButton = ToggleSwitch(self)

        self.atrSlider = Slider(tickPosition=QtGui.QSlider.TicksBelow,
            orientation=QtCore.Qt.Horizontal, tickInterval=1)
        self.atrSliderMinLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignLeft)
        self.atrSliderMaxLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignRight)
        self.atrSliderValue = QtGui.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.atrSlider.attachLabels(self.atrSliderMinLabel, self.atrSliderMaxLabel, self.atrSliderValue)
        self.atrSlider.setMinimum(1)
        self.atrSlider.setMaximum(20)


        # Ventricle
        self.ventLabel = QtWidgets.QLabel("Natural Ventricle")
        self.ventLabel.setFont(labelFont)
        self.ventSliderLabel = QtWidgets.QLabel("Pulse Width (ms):")
        self.ventSliderLabel.setFont(smallLabelFont)
        self.ventPushButton = ToggleSwitch(self)

        self.ventSlider = Slider(tickPosition=QtGui.QSlider.TicksBelow,
            orientation=QtCore.Qt.Horizontal, tickInterval=1)
        self.ventSliderMinLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignLeft)
        self.ventSliderMaxLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignRight)
        self.ventSliderValue = QtGui.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.ventSlider.attachLabels(self.ventSliderMinLabel, self.ventSliderMaxLabel, self.ventSliderValue)
        self.ventSlider.setMinimum(1)
        self.ventSlider.setMaximum(20)


        # Rate
        self.rateLabel = QtWidgets.QLabel("Natural Heart Rate")
        self.rateLabel.setFont(labelFont)
        self.rateSliderLabel = QtWidgets.QLabel("Beats Per Minute:")
        self.rateSliderLabel.setFont(smallLabelFont)

        self.rateSlider = Slider(tickPosition=QtGui.QSlider.TicksBelow,
            orientation=QtCore.Qt.Horizontal, tickInterval=1)
        self.rateSliderMinLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignLeft)
        self.rateSliderMaxLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignRight)
        self.rateSliderValue = QtGui.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.rateSlider.attachLabels(self.rateSliderMinLabel, self.rateSliderMaxLabel, self.rateSliderValue)
        self.rateSlider.setMinimum(30)
        self.rateSlider.setMaximum(180)


        # AV Delay
        self.avDelayLabel = QtWidgets.QLabel("Natural AV Delay")
        self.avDelayLabel.setFont(labelFont)
        self.avSliderLabel = QtWidgets.QLabel("Duration (ms):")
        self.avSliderLabel.setFont(smallLabelFont)
        
        self.avDelaySlider = Slider(tickPosition=QtGui.QSlider.TicksBelow,
            orientation=QtCore.Qt.Horizontal, tickInterval=10)
        self.avDelaySliderMinLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignLeft)
        self.avDelaySliderMaxLabel = QtGui.QLabel(alignment=QtCore.Qt.AlignRight)
        self.avDelaySliderValue = QtGui.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.avDelaySlider.attachLabels(self.avDelaySliderMinLabel, self.avDelaySliderMaxLabel, self.avDelaySliderValue)
        self.avDelaySlider.setMinimum(30)
        self.avDelaySlider.setMaximum(250)


        # Dispatch Commands
        self.send = QtWidgets.QPushButton("DISPATCH TEST")
        self.send.setFont(buttonFont)
        self.send.setStyleSheet("background-color: rgb(3,252,107); \
            padding: 1em 5em; border-style: outset; border-width: 2px; \
                border-radius: 10px; color: black;")

        # State Output - ensures that the user knows which test is currently running
        self.activeTestRoutineLabel = QtWidgets.QLabel("Active Test Routine")
        self.activeTestRoutineLabel.setFont(labelFont)
        self.activeTestRoutine = QtWidgets.QLabel("N/A")
        self.activeTestRoutine.setFont(smallLabelFont)

        ##  ---------  END -- Control Panel Widgets  ---------  


        ##  ---------  START -- Real Time Plot Widgets  ---------  

        pg.setConfigOption('leftButtonPan', False)  # no panning (only allow zooming) - fixes graph misalignment issue
        pg.setConfigOption('background', 'w')   # sets background to white
        pg.setConfigOptions(useOpenGL=True)     # allows for line widths other than 1

        ## init graphics window
        self.atrPlot = Plotter(title="Atrium Signals", frameSize=int(1e4), enableMenu=False)
        self.atrPlot.setVoltRange()

        self.ventPlot = Plotter(title="Ventricle Signals", frameSize=int(1e4))
        self.ventPlot.setVoltRange()

        self.autoRangePlots()

        ## cross link views
        self.atrPlot.setXLink(self.ventPlot)
        self.ventPlot.setXLink(self.atrPlot)

        ## timer settings
        self.timestep = 400 # ms
        self.timerPlotter = QtCore.QTimer()

        self.refreshCounter = 0

        # Timer Commands
        qta_stop = qta.icon('fa5.hand-paper', color='red')
        self.stop = QtWidgets.QPushButton(qta_stop,"")
        self.stop.setEnabled(True)
        self.stop.setFixedSize(50,50)

        qta_start = qta.icon('fa.play', color='green')
        self.start = QtWidgets.QPushButton(qta_start, "")
        self.start.setEnabled(True)
        self.start.setFixedSize(50,50)

        # Reset Plots
        qta_redo = qta.icon('fa5s.redo', color='blue')
        self.rst = QtWidgets.QPushButton(qta_redo, "")
        self.rst.setEnabled(True)
        self.rst.setFixedSize(50,50)

        # Generate Report
        qta_print = qta.icon('fa.print')
        self.prnt = QtWidgets.QPushButton(qta_print, "")
        self.prnt.setEnabled(True)
        self.prnt.setFixedSize(50,50)
        self.reportSubmitLabel = QtWidgets.QLabel("")
        self.reportSubmitLabel.setFont(smallLabelFont)

        ##  ---------  END -- Real Time Plot Widgets  --------- 

        ##  ---------  START -- Serial Interface  ---------  

        ## init serial object
        self.ser = SerialWidget()

        # print('Main Thread:\t', threading.get_ident())
        ## serial thread
        self.serThread = QtCore.QThread()
        self.serThread.start()
        self.ser.moveToThread(self.serThread)

        ## serial control widgets
        self.serialControlsLabel = QtWidgets.QLabel("Choose a Serial device...")
        self.serialComboBox = QtWidgets.QComboBox(self)
        self.updateSerialComboBox()
        self.serialPushButton = QtWidgets.QPushButton("Connect")
        self.serialStatusLabel = QtWidgets.QLabel("Disconnected")

        ## refresh button to update serial
        self.refreshSerial = QtWidgets.QPushButton(qta_redo, "")
        
        ##  ---------  END -- Serial Interface  --------- 


        ##  ---------  START -- PyQt UI Setup  ---------  

        ## Help Button
        qta_help = qta.icon('mdi.help')
        self.help = QtWidgets.QPushButton(qta_help, "")
        self.help.setEnabled(True)
        self.help.setFixedSize(50,50)

        ## setup layout
        self.__setupLayout()

        ## make SIGNAL-SLOT connections
        self.__connectionsList()

        ##  ---------  END -- PyQt UI Setup  --------- 


    # update the serial device options
    def updateSerialComboBox(self):
        self.serialComboBox.clear()
        self.serialComboBox.addItems(self.ser.getSerialPorts())

    ## -- Setup Methods --

    def __setupLayout(self):

        ## Control Panel
        controlPanel = QtWidgets.QVBoxLayout()
        self.__setupControlPanel(controlPanel)
        self.mainLayout.addLayout(controlPanel)

        ## Real Time Plots
        realTimeLayout = QtWidgets.QVBoxLayout()
        self.__setupRealTimePlots(realTimeLayout)
        self.mainLayout.addLayout(realTimeLayout)

    ## Called on init to setup control panel layout
    ## ASSUMPTION: parent is vertical layout
    def __setupControlPanel(self, Vparent):

        # add icons
        icons = QtWidgets.QHBoxLayout()

        icons.addWidget(self.logoMcSCertLabel, alignment=QtCore.Qt.AlignLeft)
        icons.addWidget(self.logoMacEngLabel, alignment=QtCore.Qt.AlignRight)

        Vparent.addLayout(icons)

        # add serial butons
        serial = QtWidgets.QHBoxLayout()

        serial.addWidget(self.refreshSerial)
        serial.addWidget(self.serialComboBox)
        serial.addWidget(self.serialPushButton)

        Vparent.addLayout(serial)

        # add heart controls characteristics
        wrapper = QtWidgets.QWidget()
        heartControls = QtWidgets.QGridLayout()

        self.__setupHeartCharacteristic(heartControls)

        wrapper.setLayout(heartControls)

        # surround heart controls with border + label
        wrapper.setStyleSheet("background-color: rgb(207, 209, 205);")
        Vparent.addWidget(wrapper)

        # add test routine buttons
        Vparent.addWidget(self.activeTestRoutineLabel)
        Vparent.addWidget(self.activeTestRoutine)


    ## Called to init heart characteristic controls
    ## ASSUMPTION: parent is grid layout
    def __setupHeartCharacteristic(self, Gparent):

        Gparent.addWidget(self.hcLabel, 0, 0, 1, 3, alignment=QtCore.Qt.AlignCenter)

        # atrium widgets
        Gparent.addWidget(self.atrLabel, 1, 0, 1, 2)
        Gparent.addWidget(self.atrPushButton, 1, 2, alignment=QtCore.Qt.AlignRight)
        Gparent.addWidget(self.atrSliderLabel, 2, 0, 1, 1, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))
        self.atrSlider.addSliderToLayout(Gparent, 2, 1, 1, 2, self.atrSliderMinLabel, self.atrSliderMaxLabel, self.atrSliderValue)

        # ventricle widgets
        Gparent.addWidget(self.ventLabel, 3, 0, 1, 2)
        Gparent.addWidget(self.ventPushButton, 3, 2, alignment=QtCore.Qt.AlignRight)
        Gparent.addWidget(self.ventSliderLabel, 4, 0, 1, 1, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))
        self.ventSlider.addSliderToLayout(Gparent, 4, 1, 1, 2, self.ventSliderMinLabel, self.ventSliderMaxLabel, self.ventSliderValue)

        # rate widgets
        Gparent.addWidget(self.rateLabel, 5, 0, 1, 2)
        Gparent.addWidget(self.rateSliderLabel, 6, 0, 1, 1, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))
        self.rateSlider.addSliderToLayout(Gparent, 6, 1, 1, 2, self.rateSliderMinLabel, self.rateSliderMaxLabel, self.rateSliderValue)

        # av delay widgets
        Gparent.addWidget(self.avDelayLabel, 7, 0, 1, 2)
        Gparent.addWidget(self.avSliderLabel, 8, 0, 1, 1, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))
        self.avDelaySlider.addSliderToLayout(Gparent, 8, 1, 1, 2, self.avDelaySliderMinLabel, self.avDelaySliderMaxLabel, self.avDelaySliderValue)

        # send TR
        Gparent.addWidget(self.send, 9, 0, 1, 3, alignment=QtCore.Qt.AlignCenter)

    ## Called on init to setup real time plots layout
    ## ASSUMPTION: parent is vertical layout
    def __setupRealTimePlots(self, Vparent):

        # add plot controls
        plotButtons = QtGui.QHBoxLayout()
        plotButtons.addWidget(self.help)
        plotButtons.addWidget(self.prnt)
        plotButtons.addWidget(self.stop)
        plotButtons.addWidget(self.start)
        plotButtons.addWidget(self.rst)
        plotButtons.setAlignment(QtCore.Qt.AlignRight)

        Vparent.addLayout(plotButtons)

        Vparent.addWidget(self.atrPlot)
        Vparent.addWidget(self.ventPlot)

        Vparent.addWidget(self.reportSubmitLabel)


    ## connect SIGNALS -> SLOTS
    def __connectionsList(self):
        
        # timer signals
        self.timerPlotter.timeout.connect(self.autoRangePlots)
        self.timerPlotter.timeout.connect(self.ser.startSerialRead)
        self.timerPlotter.timeout.connect(self.atrPlot.update)
        self.timerPlotter.timeout.connect(self.ventPlot.update)
        self.timerPlotter.start(self.timestep)

        # Connect Serial Controls
        self.serialPushButton.clicked.connect(lambda: self.ser.openSerial(self.serialComboBox.currentText()))
        self.serialPushButton.clicked.connect(self.autoRangePlots)  # prep plots

        # Connect Serial data signals
        self.ser.atrNat.connect(self.atrPlot.addNaturalDataPoint)
        self.ser.atrPace.connect(self.atrPlot.addPacemakerDataPoint)
        self.ser.ventNat.connect(self.ventPlot.addNaturalDataPoint)
        self.ser.ventPace.connect(self.ventPlot.addPacemakerDataPoint)

        # Serial status msgs
        self.ser.statusMsg.connect(self.updateStatusBar)

        # update serial device options
        self.refreshSerial.clicked.connect(self.updateSerialComboBox)

        # button clicks
        self.stop.clicked.connect(self.timerPlotter.stop)
        
        self.start.clicked.connect(self.startPlotting)
        
        self.rst.clicked.connect(self.autoRangePlots)
        
        self.send.clicked.connect(self.__sendTestRoutine)

        self.prnt.clicked.connect(self.__generateReport)

        self.help.clicked.connect(self.__showTutorial)


    def resizeEvent(self, event):
        # print("resize")
        # QtGui.QMainWindow.resizeEvent(self, event)

        self.atrPlot.updateFrameSize()
        self.ventPlot.updateFrameSize()

        self.autoRangePlots()

    ### SLOT FUNCTIONS ###

    # Public method to update the MainWindow StatusBar
    @QtCore.pyqtSlot()
    def startPlotting(self):
        self.autoRangePlots()
        self.timerPlotter.start(self.timestep)

    # Public method to update the MainWindow StatusBar
    @QtCore.pyqtSlot(str)
    def updateStatusBar(self, msg):
        self.statusBar().showMessage(msg)

    @QtCore.pyqtSlot()
    def __setActiveTestRoutine(self, tr):
        display = "Atrium PW: " + str(tr[0]/10) + " ms" + "\nVentricular PW: " + \
            str(tr[1]/10) + " ms" + "\nHeart Rate: " + str(tr[2]) + " BPM" + \
                "\nAV Delay: " + str(tr[3]) + " ms"

        self.activeTestRoutine.setText(str(display))

    @QtCore.pyqtSlot()
    def __generateReport(self):
        self.pr.show()

    @QtCore.pyqtSlot()
    def __showTutorial(self):
        self.tr.show()
        self.activateWindow()

    @QtCore.pyqtSlot()
    def __sendTestRoutine(self):

        '''
        According to Requirements doc:
            ATR_PW -> a multiple of 100us
            VENT_PW -> a multiple of 100us
            RATE -> an unsigned char describing the frequency of the pacing pattern (beats per minute)
            AV_DELAY -> an unsigned char describing the millisecond timespan between the end of ATR pulse and beginning of the VENT pulse
        '''

        atr_val = (self.atrSlider.value() * 10) if (self.atrPushButton.isChecked()) else 0
        vent_val = (self.ventSlider.value() * 10) if (self.ventPushButton.isChecked()) else 0

        message = [atr_val, vent_val, self.rateSlider.value(), self.avDelaySlider.value()]

        in_bytes = []
        for m in message:
            in_bytes.append(bytes([m]))

        # display active test routine if sent successfully
        if (self.ser.sendPacingInfo(in_bytes) == 1):
            self.__setActiveTestRoutine(message)
        else:
            self.updateStatusBar("Unable to update Test Routine")
        
        # realign plots
        self.autoRangePlots()

    @QtCore.pyqtSlot()
    def autoRangePlots(self):
        self.atrPlot.enableAutoRange()
        self.ventPlot.enableAutoRange()
        self.atrPlot.setVoltRange()
        self.ventPlot.setVoltRange()


app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(QtCore.QCoreApplication.applicationDirPath() + 'res/heartbeat.ico'))
ui = MainWindow()

ui.show()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()





