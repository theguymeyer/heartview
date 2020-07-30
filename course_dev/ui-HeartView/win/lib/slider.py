from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

# Slider - class definition for sliders used in the control panel
class Slider(QtGui.QSlider):

    minimumChanged = QtCore.Signal(int)
    maximumChanged = QtCore.Signal(int)

    # TODO def __init__(self, parent = None):

    def setMinimum(self, minimum):
        self.minimumChanged.emit(minimum)
        super(Slider, self).setMinimum(minimum)

    def setMaximum(self, maximum):
        self.maximumChanged.emit(maximum)
        super(Slider, self).setMaximum(maximum)

    def attachLabels(self, minLabel, maxLabel, valueLabel):
        self.minimumChanged.connect(minLabel.setNum)
        self.maximumChanged.connect(maxLabel.setNum)
        self.valueChanged.connect(valueLabel.setNum)

    # inserts the slider into the QGridLayout according to the row and col specs
    def addSliderToLayout(self, parentLayout, parentRow, parentCol, parentRowSpan, parentColSpan, minLabel, maxLabel, valueLabel):
        slider_vbox = QtGui.QVBoxLayout()
        slider_hbox = QtGui.QHBoxLayout()
        slider_hbox.setContentsMargins(0, 0, 0, 0)
        slider_vbox.setContentsMargins(0, 0, 0, 0)
        slider_vbox.setSpacing(0)

        slider_vbox.addWidget(self)
        slider_vbox.addLayout(slider_hbox)
        slider_hbox.addWidget(minLabel, QtCore.Qt.AlignLeft)
        slider_hbox.addWidget(valueLabel, QtCore.Qt.AlignCenter)
        slider_hbox.addWidget(maxLabel, QtCore.Qt.AlignRight)
        slider_vbox.addStretch()

        # ensure that the parent layout is a grid
        if (isinstance(parentLayout, QtWidgets.QGridLayout)):
            parentLayout.addLayout(slider_vbox, parentRow, parentCol, parentRowSpan, parentColSpan)
