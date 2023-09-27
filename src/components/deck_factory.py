from vocab_card import VocabCard
import pandas
import numpy as np

class AmountNoneException(Exception):
    "Raised when DeckFactory amount is equal to none"
    def __init__(self):
        self.message = "DeckFactory amount is equal to none"
        super().__init__(self.message)

class DeckFactory:
    def __init__(self):
        print("DeckFactory has been started...")
        self.amount = None

    def read_spreadsheet(self,sheet_path):
        self.vocab_df = pandas.read_csv(sheet_path)

    def get_random_indexes(self,amount):
        indexes = np.random.choice(np.arange(0,len(self.vocab_df)),size=amount,replace=False)
        indexes.sort()
        return indexes
    
    def get_vocab_from_df(self,index):
        return self.vocab_df.iloc[index,0]
    
    def get_spelling_from_df(self,index):
        return self.vocab_df.iloc[index,1]
    
    def get_translation_from_df(self,index):
        return self.vocab_df.iloc[index,2]
        
    def create_vocab_deck(self):
        if self.amount == None:
            raise AmountNoneException()
        else:
            print("Creating vocab deck with {} cards...".format(self.amount))
            indexes = self.get_random_indexes(self.amount)
            deck = []
            for index in indexes:
                vocab = self.get_vocab_from_df(index)
                spelling = self.get_spelling_from_df(index)
                translation = self.get_translation_from_df(index)
                vocab_card = VocabCard(vocab,spelling,translation,index)
                deck.append(vocab_card)
            return deck

    def set_amount(self,amount):
        self.amount = int(amount)

