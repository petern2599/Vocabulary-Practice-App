class VocabCard:
    def __init__(self,vocab, spelling, translation, index):
        self.vocab = vocab
        self.spelling = spelling
        self.translation = translation
        self.index = index
        self.is_correct = False

    def get_vocab(self):
        return self.vocab
    
    def get_spelling(self):
        return self.spelling
    
    def get_translation(self):
        return self.translation
    
    def set_correct(self):
        self.is_correct = True
    
    def set_incorrect(self):
        self.is_correct = False
