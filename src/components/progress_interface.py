from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from datetime import datetime
import time

class TimerWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        for i in range(3):
            time.sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()

class ProgressUI(QMainWindow):
    def __init__(self):
        #initialize UI
        super(ProgressUI,self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint) 
        #Load UI file
        uic.loadUi("src/assets/progress_gif.ui",self)
    
    def set_ui_components(self):
        pass

    def show_25_percent(self):
        self.movie = QMovie("src/assets/progress-25.gif")
        self.gif_label.setMovie(self.movie)

        self.thread = QThread()
        self.timer_worker = TimerWorker()
        self.timer_worker.moveToThread(self.thread)

        self.thread.started.connect(self.timer_worker.run)
        self.timer_worker.finished.connect(self.thread.quit)
        self.timer_worker.finished.connect(self.timer_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.show()
        
        self.movie.start()
        self.thread.start()
        
        self.thread.finished.connect(lambda: self.close())

    def show_50_percent(self):
        self.movie = QMovie("src/assets/progress-50.gif")
        self.gif_label.setMovie(self.movie)

        self.thread = QThread()
        self.timer_worker = TimerWorker()
        self.timer_worker.moveToThread(self.thread)

        self.thread.started.connect(self.timer_worker.run)
        self.timer_worker.finished.connect(self.thread.quit)
        self.timer_worker.finished.connect(self.timer_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.show()
        
        self.movie.start()
        self.thread.start()
        
        self.thread.finished.connect(lambda: self.close())

    def show_75_percent(self):
        self.movie = QMovie("src/assets/progress-75.gif")
        self.gif_label.setMovie(self.movie)

        self.thread = QThread()
        self.timer_worker = TimerWorker()
        self.timer_worker.moveToThread(self.thread)

        self.thread.started.connect(self.timer_worker.run)
        self.timer_worker.finished.connect(self.thread.quit)
        self.timer_worker.finished.connect(self.timer_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.show()
        
        self.movie.start()
        self.thread.start()
        
        self.thread.finished.connect(lambda: self.close())

    def show_100_percent(self):
        self.movie = QMovie("src/assets/progress-100.gif")
        self.gif_label.setMovie(self.movie)

        self.thread = QThread()
        self.timer_worker = TimerWorker()
        self.timer_worker.moveToThread(self.thread)

        self.thread.started.connect(self.timer_worker.run)
        self.timer_worker.finished.connect(self.thread.quit)
        self.timer_worker.finished.connect(self.timer_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.show()
        
        self.movie.start()
        self.thread.start()
        
        self.thread.finished.connect(lambda: self.close())
           

def main():
    app = QApplication([])
    window = ProgressUI()
    window.setWindowTitle('Progress Message')
    app.exec()
    

if __name__ == "__main__":
    main()