from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from mplwidget import MplWidget
import sys

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar

class ProgressionChartUI(QMainWindow):
    def __init__(self):
        #initialize UI
        super(ProgressionChartUI,self).__init__()
        uic.loadUi("src/assets/progression_chart.ui",self)
        self.show()
        self.update_graph()
        
    def update_graph(self):
        self.stat_percent_label.setText("80%")
        labels = ['Correct','Incorrect']
        colors = ['limegreen','red']
        sizes = [80,20]
        self.mpl_widget.ax.pie(sizes, wedgeprops=dict(width=0.5),colors=colors,labels=labels)
        self.mpl_widget.canvas.draw()
        

def main():
    app = QApplication([])
    window = ProgressionChartUI()
    window.setWindowTitle('Progression Chart')
    app.exec()

if __name__ == "__main__":
    main()