'''
Author: Guy Meyer
Date of Creation: June 2nd 2020
Objective: To provide an interface for serial comm with the Nucleo-F446RE
    INPUT: ADC readings for the pacemaker ATR and VENT pulses
    OUTPUT: Pacing information for natural ATR and VENT pulses
'''
import sys, threading

from PyQt5 import QtCore, QtWidgets, QtSerialPort
from PyQt5.QtCore import pyqtSignal


# import a custom classes
from lib.helper_functions import Helpers

class SerialWidget(QtCore.QObject):

    parentWidget = None

    # Class signals
    atrNat = QtCore.pyqtSignal(int)
    atrPace = QtCore.pyqtSignal(int)
    ventNat = QtCore.pyqtSignal(int)
    ventPace = QtCore.pyqtSignal(int)

    statusMsg = QtCore.pyqtSignal(str)

    errorOccurred = QtCore.pyqtSignal()

    # helper class
    helpers = Helpers()

    def __init__(self):
        super(SerialWidget, self).__init__()

        # self.parentWidget = parent
        
        self.ser = QtSerialPort.QSerialPort(
            baudRate=QtSerialPort.QSerialPort.Baud115200
        )

        # manage errors with error handler method
        self.__connectionsList()


    def getSerialPorts(self):
        ports = QtSerialPort.QSerialPortInfo.availablePorts()
        for p in range(len(ports)):
            ports[p] = ports[p].portName()
        return ports

    def closeSerial(self):
        if self.ser.isOpen():
            self.ser.close()
            self.statusMsg.emit("Port Was Successfully Closed")
        else:
            self.statusMsg.emit("Port Already Closed")
            None

    def clearSerial(self):
        self.ser.clear(QtSerialPort.QSerialPort.AllDirections)

    def isSerialOpen(self):
        if (self.ser.isOpen()):
            return True
        else:
            self.__errorHandler(13)
            return False
    
    def bytesAvailable(self):
        return self.ser.bytesAvailable()

    def __connectionsList(self):
        self.errorOccurred.connect(self.__errorHandler)



    ### SLOT FUNCTIONS ###


    # get ADC stream
    # Incoming serial stream protocol:
    #   <uint8_t> {SOM, ATR_PACE, VENT_PACE, ATR_NAT, VENT_NAT}
    @QtCore.pyqtSlot()
    def startSerialRead(self):

        print('Serial Thread:\t', threading.get_ident())

        # ensure that serial is open
        if(not self.isSerialOpen()):
            return None

        try:
            raw = []

            if (self.ser.bytesAvailable() > 8500):
                ## I hate this hack! 
                # What's essentially happening is that too much data results in this malloc error...
                #   Python(2254,0x111685dc0) malloc: *** error for object 0x7f83287b2000: pointer being freed was not allocated
                #   Python(2254,0x111685dc0) malloc: *** set a breakpoint in malloc_error_break to debug
                # I think that a viable solution of simply dumping the data would be to plot at higher speeds but that might require a 
                # substantial refactoring of the code. As a result I will stick with this hack since it seems to produce the 
                # desired result for this time-sensitive project
                #
                #   TODO: FIX THIS!!!!!
                ## 
                self.clearSerial()
                return None
            elif (self.ser.bytesAvailable() > 0):
                # get all the available data
                raw = self.ser.readAll()

            # split list of bytes
            data = list(raw)

            # do while data is left to analyze
            while(len(data) > 0):
                
                # Start of Message
                SOM = data.pop(0)

                if (SOM == b'\xff'):
                    try:
                        # if data is large enough
                        if (len(data) >= 4):

                            # if ADC data available convert it
                            convertedData = []
                            for i in range(4):  # take 4 values
                                convertedData.append(self.helpers.adc2volts(data.pop(0), (i < 2)))

                            # emit the signals 
                            # REMINDER - Incoming serial stream protocol:
                            #   <uint8_t> {SOM, ATR_PACE, VENT_PACE, ATR_NAT, VENT_NAT}

                            self.atrNat.emit(convertedData[2])
                            self.atrPace.emit(convertedData[0])
                            self.ventNat.emit(convertedData[3])
                            self.ventPace.emit(convertedData[1])

                    
                    except Exception as e:
                        print("Internal Exception, \t", e)
                        break


                else:
                    # not at start of message
                    # Forseeable issue losing data points since they are not SOMs
                    None

        except Exception as e:
            # TODO handle error: QIODevice::read (QSerialPort): device not open
            
            pass

    # send new pacing information
    # INPUT: pacingData - an array of bytes respresenting pacing info
    # OUTPUT: sends serial info to testing controller
    # RETURN VALUE: return 1 upon successful send, else returns 0
    @QtCore.pyqtSlot()
    def sendPacingInfo(self, pacingData):
        print("Attemting:\t",pacingData)

        if(not self.isSerialOpen()):
            return 0

        try:
            if (self.ser.error() == 0):
                for d in pacingData:
                    self.ser.write(d)
                    
                self.statusMsg.emit("Sent Successfully")
                return 1

        except Exception as e:
            pass    # Serial Error signal will direct error to __errorHandler
            
        return 0

    @QtCore.pyqtSlot()
    def openSerial(self, portText):
        currentConnected = portText #self.parentWidget.serialComboBox.currentText()

        if (self.isSerialOpen and self.ser.portName() == currentConnected.split('/')[-1]):
            self.statusMsg.emit("Serial Port: " + str(currentConnected) + " - Already Open")

        # trying to connect a new device
        elif (self.ser.portName != currentConnected):

            # close the old port
            self.closeSerial()

            # define port
            self.ser.setPortName(currentConnected)

            # open the serial port
            status = self.ser.open(QtCore.QIODevice.ReadWrite)
            if (status):
                self.statusMsg.emit("Serial Enabled - Connected to " + str(currentConnected))
                self.__connectionsList()    # establish connections
                self.clearSerial()
            else:
                self.__errorHandler()



    @QtCore.pyqtSlot()
    def __errorHandler(self, *args):
        

        if (self.ser.error() != 0): 
            self.statusMsg.emit("Serial Error:\t" + self.ser.errorString())
            if ('ser' in locals()):
                self.ser.close()

        # catch non-signal error
        elif(len(args) != 0):
            if (args[0] == 13):
                self.statusMsg.emit("Serial Error:\t" + "Device Not Open")
                
            elif (args[0] == 2):
                self.statusMsg.emit("Serial Error:\t" + "Permission Error")

            elif (args[0] == 7):
                self.statusMsg.emit("Serial Error:\t" + "Write Error")

            elif (args[0] == 8):
                self.statusMsg.emit("Serial Error:\t" + "Read Error")

            if ('ser' in locals()):
                    self.ser.close()

        # clear flag
        self.ser.clearError()
