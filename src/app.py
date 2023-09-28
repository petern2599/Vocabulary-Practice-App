from PyQt5.QtWidgets import *
from PyQt5 import uic
from components.deck_factory import DeckFactory
from components.vocab_card import VocabCard

class VocabularyPracticeApp(QMainWindow):
    def __init__(self):
        super(VocabularyPracticeApp,self).__init__()
        uic.loadUi("src/assets/app.ui",self)
        self.show()
        self.deck_factory = DeckFactory()
        self.deck_factory.set_amount(10)

        self.actionAdd_Spreadsheet.triggered.connect(self.add_spreadsheet_pressed)
        self.actionStart.triggered.connect(self.start_pressed)
        self.correct_button.clicked.connect(self.correct_button_pressed)
        self.incorrect_button.clicked.connect(self.incorrect_button_pressed)

    def add_spreadsheet_pressed(self):
        spreadsheet_path = QFileDialog.getOpenFileName(self,'Select file','')
        self.deck_factory.read_spreadsheet(spreadsheet_path[0])

    def start_pressed(self):
        self.vocab_deck = self.deck_factory.create_vocab_deck()
        self.deck_length = len(self.vocab_deck)
        self.vocab_deck.reverse()
        self.counter = 0
        self.correct = 0
        self.incorrect = 0
        self.display_card()

    def display_card(self):
        card = self.vocab_deck.pop()
        self.counter += 1
        self.set_main_text(card.vocab)
        self.set_sub_text(card.spelling)
        self.set_counter_text("({} out of {} vocabs)".format(self.counter,self.deck_length))
        self.set_progress_value(int((self.counter/self.deck_length)*100))
    
    def set_main_text(self,text):
        self.main_text_label.setText(text)

    def set_sub_text(self,text):
        self.sub_text_label.setText(text)
    
    def set_counter_text(self,text):
        self.counter_text_label.setText(text)

    def set_progress_value(self,value):
        self.progressBar.setValue(value)

    def correct_button_pressed(self):
        self.correct += 1
        if len(self.vocab_deck) != 0:
            self.display_card()
        else:
            message = QMessageBox()
            message.setText("No more cards in deck")
            message.setWindowTitle('Message')
            message.exec_()

    def incorrect_button_pressed(self):
        self.incorrect += 1
        if len(self.vocab_deck) != 0:
            self.display_card()
        else:
            message = QMessageBox()
            message.setText("No more cards in deck")
            message.setWindowTitle('Message')
            message.exec_()

    

def main():
    app = QApplication([])
    window = VocabularyPracticeApp()
    window.setWindowTitle('Vocabulary Practice')
    app.exec()

if __name__ == "__main__":
    main()