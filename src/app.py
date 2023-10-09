from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from components.deck_factory import DeckFactory
from components.vocab_card import VocabCard
from components.json_logger import JSONLogger
from components.progression_chart import ProgressionChart
from datetime import date,timedelta

class VocabularyPracticeApp(QMainWindow):
    def __init__(self):
        super(VocabularyPracticeApp,self).__init__()
        uic.loadUi("src/assets/app.ui",self)
        self.show()
        self.ui_setup()
        self.deck_factory = DeckFactory()
        self.progress_charts = ProgressionChart(self)
        self.set_default_settings()
        self.json_logger = JSONLogger()
        streak_date = date.today()
        streak_amount_today = self.check_streak(streak_date)
        streak_date -= timedelta(days=1)
        streak_amount_yesterday = self.check_streak(streak_date)

        if streak_amount_today != 0:
            self.set_streak(streak_amount_today)
        elif streak_amount_yesterday != 0:
            self.set_streak(streak_amount_yesterday)
        else:
            self.set_streak(0)

    def ui_setup(self):
        self.actionAdd_Spreadsheet.triggered.connect(self.add_spreadsheet_pressed)
        self.actionStart.triggered.connect(self.start_pressed)
        self.actionUndo.triggered.connect(self.undo_pressed)
        self.actionSet_Amount.triggered.connect(self.set_amount_pressed)
        self.actionSet_Mode.triggered.connect(self.set_mode_pressed)
        self.actionToday_s_Stats.triggered.connect(self.today_stats_pressed)
        self.actionBar_Chart.triggered.connect(self.week_stats_bar_pressed)
        self.actionPercent_Chart.triggered.connect(self.week_stats_percent_pressed)
        self.actionBar_Chart_2.triggered.connect(self.weekly_stats_bar_pressed)
        self.actionPercent_Chart_2.triggered.connect(self.weekly_stats_percent_pressed)
        self.correct_button.clicked.connect(self.correct_button_pressed)
        self.incorrect_button.clicked.connect(self.incorrect_button_pressed)
        self.show_button.clicked.connect(self.show_button_pressed)

    def set_default_settings(self):
        self.deck_factory.set_amount(10)
        self.practice_mode = "Practice Vocab"
        self.is_done = False
        self.is_practicing = False

    def add_spreadsheet_pressed(self):
        try:
            spreadsheet_path = QFileDialog.getOpenFileName(self,'Select spreadsheet file','',"csv(*.csv)")
            self.deck_factory.read_spreadsheet(spreadsheet_path[0])

        except FileNotFoundError:
            self.generate_msg("No file was selected...",1)
        
    def disable_buttons(self):
        self.show_button.setEnabled(False)
        self.correct_button.setEnabled(False)
        self.incorrect_button.setEnabled(False)

    def enable_buttons(self):
        self.show_button.setEnabled(True)
        self.correct_button.setEnabled(True)
        self.incorrect_button.setEnabled(True)

    def start_pressed(self):
        if self.deck_factory.vocab_df.empty:
            self.disable_buttons()
            self.generate_msg("You did not add a spreadsheet...",1)
        elif len(self.deck_factory.vocab_df) == 0:
                self.disable_buttons()
                self.generate_msg("Spreadsheet appears to be empty...",1)
        else:
            self.enable_buttons()
            self.vocab_deck = self.deck_factory.create_vocab_deck()
            self.deck_length = len(self.vocab_deck)
            self.counter = 0
            self.correct = 0
            self.incorrect = 0
            self.deck_index = 0
            self.is_done = False
            self.is_practicing = True
            self.display_card()

    def undo_pressed(self):
        if self.deck_factory.vocab_df.empty:
            self.disable_buttons()
            self.generate_msg("You did not add a spreadsheet...",1)
        elif len(self.deck_factory.vocab_df) == 0:
                self.disable_buttons()
                self.generate_msg("Spreadsheet appears to be empty...",1)
        elif self.is_done==False and self.is_practicing==True:
            self.deck_index -= 1
            if self.deck_index < 0:
                self.deck_index = 0
            self.card = self.vocab_deck[self.deck_index]

            #Subtract by 2 because display_card() will add 1 to counter
            self.counter -= 2
            if self.counter < 0:
                self.counter = 0
            
            self.set_counter_text("({} out of {} vocabs)".format(self.counter,self.deck_length))
            self.set_progress_value(int((self.counter/self.deck_length)*100))

            result = self.check_card_is_correct()
            if result:
                if self.correct > 0:
                    self.correct -= 1
                else:
                    self.correct = 0
            else:
                if self.incorrect > 0:
                    self.incorrect -= 1
                else:
                    self.incorrect = 0
            self.display_card()
        else:
            self.disable_buttons()
            self.generate_msg("You have already completed this practice run, please press start again if you want to practice more...",0)

    def check_card_is_correct(self):
        return self.card.is_correct

    def set_amount_pressed(self):
        if self.is_practicing == False:
            amount,ok = QInputDialog.getText(self, 'Set Amount', 'Type number of vocab cards to generate for deck:')
            if ok:
                self.deck_factory.set_amount(amount)
        else:
            self.generate_msg("Finish current practice before setting amount...",1)

    def set_mode_pressed(self):
        if self.is_practicing == False:
            practice_modes = ("Practice Vocab", "Practice Translation")
            practice_mode,ok = QInputDialog.getItem(self, 'Set Practice Mode', 'Select Practice Mode:',practice_modes,0,False)
            if ok and practice_mode:
                self.practice_mode = practice_mode
        else:
            self.generate_msg("Finish current practice before setting amount...",1)

    def today_stats_pressed(self):
        self.progress_charts.generate_today_stats()

    def week_stats_bar_pressed(self):
        self.progress_charts.generate_week_stats(False)

    def week_stats_percent_pressed(self):
        self.progress_charts.generate_week_stats(True)

    def weekly_stats_bar_pressed(self):
        self.progress_charts.generate_weekly_stats(False)

    def weekly_stats_percent_pressed(self):
        self.progress_charts.generate_weekly_stats(True)

    def display_card(self):
        self.card = self.vocab_deck[self.deck_index]
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
        self.card.set_correct()
        self.deck_index += 1
        if self.deck_index < len(self.vocab_deck) and self.is_done == False:
            self.display_card()
        elif self.is_done == True:
            self.generate_msg("No more cards in deck...",0)
        else:
            self.create_log()
            self.is_done = True
            self.is_practicing = False
            self.generate_msg("No more cards in deck, logging stats...",0)
            today = date.today()
            streak_amount = self.check_streak(today)
            self.set_streak(streak_amount)
            self.disable_buttons()

    def incorrect_button_pressed(self):
        self.incorrect += 1
        self.card.set_incorrect()
        self.deck_index += 1
        if self.deck_index < len(self.vocab_deck) and self.is_done == False:
            self.json_logger.add_index_to_dictionary(self.card.index)
            self.display_card()
        elif self.is_done == True:
            self.generate_msg("No more cards in deck...",0)
        else:
            self.json_logger.add_index_to_dictionary(self.card.index)
            self.create_log()
            self.is_done = True
            self.is_practicing = False
            self.generate_msg("No more cards in deck, logging stats...",0)
            today = date.today()
            streak_amount = self.check_streak(today)
            self.set_streak(streak_amount)
            self.disable_buttons()

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

    def generate_msg(self,msg,is_error):
        message = QMessageBox()
        message.setText(msg)
        if is_error:
            message.setWindowTitle('Error Message')
        else:
            message.setWindowTitle('Message')
        message.exec_()

    def check_streak(self,date_to_check):
        streak_amount = self.json_logger.check_streak(date_to_check)
        return streak_amount

    def set_streak(self,amount):
        if amount < 1000:
            self.streak_label.setText("{}".format(amount))
        else:
            self.streak_label.setText("{}+".format(999))

def main():
    app = QApplication([])
    window = VocabularyPracticeApp()
    window.setWindowTitle('Vocabulary Practice')
    app.exec()

if __name__ == "__main__":
    main()