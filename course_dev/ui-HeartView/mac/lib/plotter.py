'''
Generate a Report Window
Author: Guy Meyer
Date of Creation: June 18 2020

An inheritance of the pyqtgraph PlotWidget that defines the plot widgets on
the main window. The main drivers of this class are Slots that are updated 
with every timer tick.
'''


import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore

# Plotter - class definition for the plots used to graph the real-time signals
class Plotter(pg.PlotWidget):

    def __init__(self, frameSize, *args, **kwargs):
        super(Plotter, self).__init__(*args, **kwargs)

        # init data
        self.stepSize = round(1.0/2.3116,8)    # plotting rate
        self.frameSize = frameSize    # number of data points shown at once
        self.timesteps = np.arange(0, self.frameSize * self.stepSize, self.stepSize)
        self.dataNatural = np.transpose([self.timesteps, np.random.rand(self.frameSize)])
        self.dataPacemaker = np.transpose([self.timesteps, np.random.rand(self.frameSize)])

        # color scheme - TODO add line weights
        self.natPen = pg.mkPen(color=(255, 0, 0), width=3)
        self.pacePen = pg.mkPen(color=(0, 0, 255), width=3)

        # get Plot Item
        self.natPlot = self.plotItem.plot(pen=self.natPen)
        self.pacePlot = self.plotItem.plot(pen=self.pacePen)

        # axis labels
        self.setLabel("left", "Voltage (mV)")
        self.setLabel("bottom", "Time (ms)")

        

    ### SLOT FUNCTIONS ###

    '''
    - The following slot functions are used to continuously update the plot with new data.
    - This is accomplished by connecting signals generated in the serial_interface 
        to the slots which are updated when new data is read and calculated.
    - The 'update' function is connected to the timeout of a timer in the parent that executes
        once every given timer period. The timer's timeout is also connected to the serial
        read function so that serial is read, calculated and displayed every tick.
    '''

    @QtCore.pyqtSlot(int)
    def addNaturalDataPoint(self, nat_dp):
        nextStep = self.dataNatural[len(self.dataNatural)-1][0] + self.stepSize # next time value
        self.dataNatural = np.vstack((self.dataNatural[1:len(self.dataNatural)], [nextStep, nat_dp]))

    @QtCore.pyqtSlot(int)
    def addPacemakerDataPoint(self, pace_dp):
        nextStep = self.dataPacemaker[len(self.dataPacemaker)-1][0] + self.stepSize # next time value
        self.dataPacemaker = np.vstack((self.dataPacemaker[1:len(self.dataPacemaker)], [nextStep, pace_dp]))

    @QtCore.pyqtSlot()
    def update(self):
        self.__updateNaturalData()
        self.__updatePacemakerData()

        # fix height to 5Volts
        self.setYRange(0,5000)


    ### PRIVATE METHODS ###

    def __updateNaturalData(self):
        self.natPlot.setData(self.dataNatural)

    def __updatePacemakerData(self):
        self.pacePlot.setData(self.dataPacemaker)
