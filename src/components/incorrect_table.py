from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from components.deck_factory import DeckFactory

class IncorrectTableUI(QMainWindow):
    def __init__(self,main_app):
        #initialize UI
        super(IncorrectTableUI,self).__init__()
        #Load UI file
        uic.loadUi("src/assets/incorrect_table.ui",self)

        self.main_app = main_app

        self.deck_factory = self.main_app.deck_factory
        

    def set_ui_components(self):
        pass
    
    def resize_table(self,dictionary):
        self.dictionary_length = len(dictionary)
        self.incorrect_table_widget.setRowCount(self.dictionary_length)
        self.incorrect_table_widget.setColumnCount(5)
        self.incorrect_table_widget.setHorizontalHeaderItem(0,QTableWidgetItem("Index"))
        self.incorrect_table_widget.setHorizontalHeaderItem(1,QTableWidgetItem("Vocabulary/Grammar"))
        self.incorrect_table_widget.setHorizontalHeaderItem(2,QTableWidgetItem("Spelling"))
        self.incorrect_table_widget.setHorizontalHeaderItem(3,QTableWidgetItem("Translation"))
        self.incorrect_table_widget.setHorizontalHeaderItem(4,QTableWidgetItem("Frequency"))

        header = self.incorrect_table_widget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    def populate_table(self,dictionary):
        counter = 0
        for index, frequency in dictionary.items():
            vocab = self.deck_factory.get_vocab_from_df(int(index))
            spelling = self.deck_factory.get_spelling_from_df(int(index))
            translation = self.deck_factory.get_translation_from_df(int(index))
            self.add_item(counter,index,vocab,spelling,translation,frequency)
            counter += 1
        
    def add_item(self,row,index,vocab,spelling,translation,frequency):
        self.incorrect_table_widget.setItem(row,0,QTableWidgetItem(index))
        self.incorrect_table_widget.setItem(row,1,QTableWidgetItem(vocab))
        self.incorrect_table_widget.setItem(row,2,QTableWidgetItem(spelling))
        self.incorrect_table_widget.setItem(row,3,QTableWidgetItem(translation))
        self.incorrect_table_widget.setItem(row,4,QTableWidgetItem(str(frequency)))


def main():
    app = QApplication([])
    window = IncorrectTableUI()
    window.setWindowTitle('Progress Message')
    app.exec()

if __name__ == "__main__":
    main()