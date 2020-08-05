'''
Generate a Report Window
Author: Guy Meyer
Date of Creation: July 2 2020

Simple UI that allows the user to build a report which is generated as a PDF.
The user can select their desired sections and name the report
'''

import sys, os
from fpdf import FPDF
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtWidgets, QtCore
from datetime import datetime

import qtawesome as qta # fontawesome
import numpy as np  # numpy


## New window to display PDF Report options
class PrinterWindow(QtGui.QMainWindow):

    filePATH = str(os.path.dirname(os.path.realpath("mainwindow.py")))

    def __init__(self, parent):
        super(PrinterWindow, self).__init__(parent)
        self.setWindowTitle("Generate Report")

        # Create central widget
        self.centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralWidget) 

        # setup main layout
        self.mainLayout = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        ## UI Fonts
        self.family = "Times"
        labelFamily = "Arial"
        bigLabelFont = QtGui.QFont(labelFamily, 20)
        smallLabelFont = QtGui.QFont(labelFamily, 16)
        tinyLabelFont = QtGui.QFont(labelFamily, 12)
        errorFont = QtGui.QFont(labelFamily, 16, weight=QtGui.QFont.Bold)

        ## UI Widgets
        self.mainLabel = QtWidgets.QLabel("Build your report...")
        self.mainLabel.setFont(bigLabelFont)
        self.mainLabel.resize(100, 50)
        self.mainLabel.setStyleSheet("margin: 1em 0em;")

        # Main Title
        self.windowTitle = QtWidgets.QLabel("Report Title:")
        self.windowTitle.setFont(smallLabelFont)

        # Report Components checkbox list
        self.checkBoxLabel = QtWidgets.QLabel("Include these sections:")
        self.checkBoxLabel.setFont(smallLabelFont)
        self.activeRoutineCB = QtWidgets.QCheckBox("Active Test Routine")
        self.activeRoutineCB.setChecked(True)
        self.atrPlotCB = QtWidgets.QCheckBox("Atrium Plots")
        self.atrPlotCB.setChecked(True)
        self.ventPlotCB = QtWidgets.QCheckBox("Ventricle Plots")
        self.ventPlotCB.setChecked(True)

        # Report ID Text Input
        self.reportID = QtWidgets.QLineEdit(self)
        self.reportID.setText(str(np.random.randint(1,1E6)))
        self.reportID.setMaxLength(100)

        # Output File Location
        self.outputFolderLabel = QtWidgets.QLabel("Destination Folder:")
        self.outputFolderLabel.setFont(smallLabelFont)
        self.outputFolderPATH = QtWidgets.QLabel(self.filePATH)
        self.outputFolderPATH.setFont(tinyLabelFont)
        self.changeFolderButton = QtWidgets.QPushButton("Save to...")
        
        # Submit button
        qta_print = qta.icon('fa.print')
        self.submitButton = QtWidgets.QPushButton(qta_print, "Generate...")
        self.submitButton.setEnabled(True)

        # Error Messages
        self.checkboxErrorMsg = QtWidgets.QLabel("")
        self.checkboxErrorMsg.setFont(errorFont)
        self.checkboxErrorMsg.setStyleSheet("color: red;")
        self.idErrorMsg = QtWidgets.QLabel("")
        self.idErrorMsg.setFont(errorFont)
        self.idErrorMsg.setStyleSheet("color: red;")

        ## setup layout
        self.__setupLayout()

        ## make SIGNAL-SLOT connections
        self.__connectionsList()

    # extract 'widget' QPixmap, then adds it to 'pdf' with given *args
    def addWidgetToPDF(self, pdf, widget):
        p = widget.grab()
        w_name = str(np.random.randint(1, 1E8)) + ".jpg"
        p.save(w_name)
        pdf.image(w_name, w=180)
        os.remove(w_name)

        # clear memory
        del p
        del w_name

    ## Builds a PDF according to user input and generates report to desired location
    def generateReport(self):

        try:
            title = self.reportID.text()
            activeRoutine = self.parent().activeTestRoutine.text()
            atrPlot = self.parent().atrPlot
            ventPlot = self.parent().ventPlot
            spacer = 10

        except Exception as e:
            print("Printer Parent Error:", e)
            return 0

        try:
            date = datetime.now()
            filename = str(title) + "_" + date.strftime('%Y-%m-%d_%H-%M-%S.pdf')

            pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
            pdf.add_page()
            pdf.set_font(self.family, 'B', 16)

            # add title
            pdf.cell(40, 10, "Report ID:\t" + str(title))

            # Line break
            pdf.ln(spacer * 2)

            pdf.set_font(self.family, 'U', 12)

            # Active Test Routine
            if (self.activeRoutineCB.isChecked()):
                pdf.cell(w=20, h=8, txt="Active Test Routine", ln=1)

                pdf.set_font(self.family, '', 10)
                for param in activeRoutine.split('\n'):
                    pdf.cell(w=20, h=8, txt=param, ln=1)
                    pdf.ln(2)

                pdf.set_font(self.family, 'U', 12)

            # Atrium Plot
            if (self.atrPlotCB.isChecked()):
                pdf.cell(w=20, h=8, txt="Atrium Plot:", ln=1)
                self.addWidgetToPDF(pdf, atrPlot)
                pdf.ln(spacer)

            # Ventricle Plot
            if (self.ventPlotCB.isChecked()):
                pdf.cell(w=20, h=8, txt="Ventricle Plot:", ln=1)
                self.addWidgetToPDF(pdf, ventPlot)
                pdf.ln(spacer)

            pdf.output(self.filePATH + "/" + filename, 'F')

            # Submit Popup
            self.parent().reportSubmitLabel.setText(\
                "Report Generated! Saved to..." + self.filePATH + "/" + filename)


            # close window
            self.close()

        except Exception as e:
            print("PDF Error:", e)
        
    # checks if output file path is valid
    def __isValidPATH(self):
        # TODO add permissions restrictions
        return (len(self.filePATH) > 0)

    # checks if the ID is valid - must be greater than zero
    def __isValidID(self):
        return (len(self.reportID.text()) > 0 and not (" " in self.reportID.text()))

    # checks if UI components were selected - must be at least one
    def __isValidCheckboxes(self):
        return (self.activeRoutineCB.isChecked() or self.atrPlotCB.isChecked() or self.ventPlotCB.isChecked())

    def __setupLayout(self):

        verticalSpacer = QtWidgets.QSpacerItem(150, 10, QtWidgets.QSizePolicy.Expanding)

        # Window Title
        self.mainLayout.addWidget(self.mainLabel)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        # Section Checkboxes
        self.mainLayout.addWidget(self.checkBoxLabel)
        self.mainLayout.addWidget(self.activeRoutineCB)
        self.mainLayout.addWidget(self.atrPlotCB)
        self.mainLayout.addWidget(self.ventPlotCB)
        self.mainLayout.addWidget(self.checkboxErrorMsg)

        self.mainLayout.addItem(verticalSpacer)

        # Report ID Input
        titleLayout = QtGui.QHBoxLayout()
        titleLayout.addWidget(self.windowTitle)
        titleLayout.addWidget(self.reportID)
        self.mainLayout.addLayout(titleLayout)
        self.mainLayout.addWidget(self.idErrorMsg)

        # Destination PATH
        filePathLayout = QtGui.QHBoxLayout()
        filePathLayout.addWidget(self.outputFolderLabel)
        filePathLayout.addWidget(self.changeFolderButton)
        self.mainLayout.addLayout(filePathLayout)
        self.mainLayout.addWidget(self.outputFolderPATH)

        # Submit Button
        self.mainLayout.addWidget(self.submitButton)

    def __connectionsList(self):
        
        # Connect Checkboxes
        self.activeRoutineCB.clicked.connect(self.__isValidReport)
        self.atrPlotCB.clicked.connect(self.__isValidReport)
        self.ventPlotCB.clicked.connect(self.__isValidReport)

        # ID Altered
        self.reportID.textChanged.connect(self.__isValidReport)

        # Generate Report
        self.submitButton.clicked.connect(self.generateReport)

        # Change filePATH
        self.changeFolderButton.clicked.connect(self.__changeOutputDir)
        
    ### SLOT FUNCTIONS ###

    @QtCore.pyqtSlot()
    def __changeOutputDir(self):
        # Select output directory
        self.filePATH = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.outputFolderPATH.setText(self.filePATH)

    # checks for existing errors in Printer UI
    @QtCore.pyqtSlot()    
    def __isValidReport(self):
        if (self.__isValidPATH() and self.__isValidID() and self.__isValidCheckboxes()):
            # valid report
            self.submitButton.setEnabled(True)
        else:
            # invalid report
            self.submitButton.setEnabled(False)
        
        self.__setErrorIndicators()


    ### ERROR HANDLER FUNCTIONS ###

    def __setErrorIndicators(self):

        ## Update error msg for checkboxes
        if (self.__isValidCheckboxes()):
            # clear error message
            self.checkboxErrorMsg.setText("")

        else:   # no checkbox selected
            self.checkboxErrorMsg.setText("Select at least one option!")

        ## Update error msg for report ID
        if (self.__isValidID()):
            # clear error message
            self.idErrorMsg.setText("")

        elif (" " in self.reportID.text()):
            # spaces found in name
            self.idErrorMsg.setText("Space is an invalid character!")

        else:
            # report name is empty
            self.idErrorMsg.setText("Report must be named!")

        ## Update error msg for PATH
        if (self.__isValidPATH()):
            self.outputFolderPATH.setText(self.filePATH)

        else:
            self.outputFolderPATH.setText("Invalid PATH!")


