from PyQt5.QtWidgets import *
from PyQt5 import uic
from components.deck_factory import DeckFactory
from components.vocab_card import VocabCard

class VocabularyPracticeApp(QMainWindow):
    def __init__(self):
        super(VocabularyPracticeApp,self).__init__()
        uic.loadUi("src/assets/app.ui",self)
        self.show()


def main():
    app = QApplication([])
    window = VocabularyPracticeApp()
    window.setWindowTitle('Vocabulary Practice')
    app.exec()

if __name__ == "__main__":
    main()