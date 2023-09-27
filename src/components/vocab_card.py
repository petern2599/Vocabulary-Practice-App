class VocabCard:
    def __init__(self,vocab, spelling, translation, index):
        self.vocab = vocab
        self.spelling = spelling
        self.translation = translation
        self.index = index

    def get_vocab(self):
        return self.vocab
    
    def get_spelling(self):
        return self.spelling
    
    def get_translation(self):
        return self.translation
