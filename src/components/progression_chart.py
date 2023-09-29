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
        self.mpl_widget.set_size(left=.12,bottom=.12,width=.72,height=.72)
        self.update_graph()
        self.show()
        
    def update_graph(self):
        self.stat_percent_label.setText("80%")
        labels = ['Correct','Incorrect']
        colors = ['limegreen','red']
        sizes = [60,40]
        self.mpl_widget.ax.pie(sizes, wedgeprops=dict(width=0.5),startangle=90,colors=colors,labels=labels,textprops={'fontsize': 8})
        self.mpl_widget.canvas.draw()
        

def main():
    app = QApplication([])
    window = ProgressionChartUI()
    window.setWindowTitle('Progression Chart')
    app.exec()

if __name__ == "__main__":
    main()