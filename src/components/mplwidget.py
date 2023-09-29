import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np

class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.fig = Figure()
        self.ax = self.fig.add_axes([0,0,1,1])
        self.ax.axis('equal')
        self.canvas = FigureCanvas(self.fig)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        
    
    