from PyQt5.QtWidgets import *
from PyQt5 import uic
from components.deck_factory import DeckFactory
from components.vocab_card import VocabCard
from components.json_logger import JSONLogger
from components.progression_chart import ProgressionChartUI

class VocabularyPracticeApp(QMainWindow):
    def __init__(self):
        super(VocabularyPracticeApp,self).__init__()
        uic.loadUi("src/assets/app.ui",self)
        self.show()
        self.ui_setup()
        self.deck_factory = DeckFactory()
        self.set_default_settings()

        self.json_logger = JSONLogger()

    def ui_setup(self):
        self.actionAdd_Spreadsheet.triggered.connect(self.add_spreadsheet_pressed)
        self.actionStart.triggered.connect(self.start_pressed)
        self.actionSet_Amount.triggered.connect(self.set_amount_pressed)
        self.actionSet_Mode.triggered.connect(self.set_mode_pressed)
        self.correct_button.clicked.connect(self.correct_button_pressed)
        self.incorrect_button.clicked.connect(self.incorrect_button_pressed)
        self.show_button.clicked.connect(self.show_button_pressed)

    def set_default_settings(self):
        self.deck_factory.set_amount(10)
        self.practice_mode = "Practice Vocab"

    def add_spreadsheet_pressed(self):
        try:
            spreadsheet_path = QFileDialog.getOpenFileName(self,'Select spreadsheet file','',"csv(*.csv)")
            self.deck_factory.read_spreadsheet(spreadsheet_path[0])

        except FileNotFoundError:
            message = QMessageBox()
            message.setText("No file was selected...")
            message.setWindowTitle('Message')
            message.exec_()
        
    def disable_buttons(self):
        self.show_button.setEnabled(False)
        self.correct_button.setEnabled(False)
        self.incorrect_button.setEnabled(False)

    def enable_buttons(self):
        self.show_button.setEnabled(True)
        self.correct_button.setEnabled(True)
        self.incorrect_button.setEnabled(True)

    def start_pressed(self):
        if len(self.deck_factory.vocab_df) == 0:
                self.disable_buttons()
        else:
            self.enable_buttons()
            self.vocab_deck = self.deck_factory.create_vocab_deck()
            self.deck_length = len(self.vocab_deck)
            self.vocab_deck.reverse()
            self.counter = 0
            self.correct = 0
            self.incorrect = 0
            self.display_card()

    def set_amount_pressed(self):
        amount,ok = QInputDialog.getText(self, 'Set Amount', 'Type number of vocab cards to generate for deck:')
        if ok:
            self.set_amount(amount)

    def set_amount(self,amount):
        self.deck_factory.set_amount(amount)

    def set_mode_pressed(self):
        practice_modes = ("Practice Vocab", "Practice Translation")
        practice_mode,ok = QInputDialog.getItem(self, 'Set Practice Mode', 'Select Practice Mode:',practice_modes,0,False)
        if ok and practice_mode:
            self.practice_mode = practice_mode

    def display_card(self):
        self.card = self.vocab_deck.pop()
        self.counter += 1

        if self.practice_mode == "Practice Vocab":
            self.show_button_toggle = 0
            self.set_show_button_text()

            self.set_main_text(self.card.vocab)
            self.set_sub_text(self.card.spelling)
            self.set_counter_text("({} out of {} vocabs)".format(self.counter,self.deck_length))
            self.set_progress_value(int((self.counter/self.deck_length)*100))
            
        elif self.practice_mode == "Practice Translation":
            self.show_button_toggle = 1
            self.set_show_button_text()

            self.set_main_text(self.card.translation)
            self.set_sub_text("")
            self.set_counter_text("({} out of {} vocabs)".format(self.counter,self.deck_length))
            self.set_progress_value(int((self.counter/self.deck_length)*100))

    def switch_display_card(self):
        if self.show_button_toggle == 0:
            self.set_main_text(self.card.vocab)
            self.set_sub_text(self.card.spelling)
        else:
            self.set_main_text(self.card.translation)
            self.set_sub_text("")
    
    def set_main_text(self,text):
        self.main_text_label.setText(text)

    def set_sub_text(self,text):
        self.sub_text_label.setText(text)
    
    def set_counter_text(self,text):
        self.counter_text_label.setText(text)

    def set_progress_value(self,value):
        self.progressBar.setValue(value)

    def set_show_button_text(self):
        if self.show_button_toggle:
            self.show_button.setText("Show Vocab")
        else:
            self.show_button.setText("Show Translation")

    def correct_button_pressed(self):
        self.correct += 1
        if len(self.vocab_deck) != 0:
            self.display_card()
        else:
            self.create_log()
            message = QMessageBox()
            message.setText("No more cards in deck, logging stats...")
            message.setWindowTitle('Message')
            message.exec_()

    def incorrect_button_pressed(self):
        self.incorrect += 1
        if len(self.vocab_deck) != 0:
            self.display_card()
        else:
            self.create_log()
            message = QMessageBox()
            message.setText("No more cards in deck, logging stats...")
            message.setWindowTitle('Message')
            message.exec_()

    def show_button_pressed(self):
        if self.show_button_toggle == 0:
            self.show_button_toggle = 1
            self.set_show_button_text()
            self.switch_display_card()
        else:
            self.show_button_toggle = 0
            self.set_show_button_text()
            self.switch_display_card()

    def create_log(self):
        self.json_logger.append_daily_stats(self.correct,self.incorrect)

    def display_progression_chart(self):
        self.progression_window = ProgressionChartUI(self)
        self.progression_window.setWindowTitle('Progression Chart')
        self.progression_window.show()

def main():
    app = QApplication([])
    window = VocabularyPracticeApp()
    window.setWindowTitle('Vocabulary Practice')
    app.exec()

if __name__ == "__main__":
    main()