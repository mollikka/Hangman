class HangmanSolver:

    def __init__(self, game, dictionary):
        self.game = game
        self.dictionary = dictionary

        word_length = len(self.game.get_hint())
        self.dictionary = [word for word in self.dictionary
                                if len(word) == word_length]

    def get_dictionary(self):
        return [i for i in self.dictionary]

    def update_dictionary(self):
        hint = self.game.get_hint()

        for i, hint_letter in enumerate(hint):
            if hint_letter == "_": continue

            self.dictionary = [word for word in self.dictionary
                                if word[i] == hint_letter]

    def remove_letter_from_dictionary(self, letter):
        self.dictionary = [word for word in self.dictionary
                                if not letter in word]

    def guess(self):
        #override this
        for word in self.dictionary:
            for letter in word:
                amount_of_hits = self.game.guess(letter)

                if amount_of_hits == -1:
                    continue

                if amount_of_hits == 0:
                    self.remove_letter_from_dictionary(letter)

                if amount_of_hits > 0:
                    self.update_dictionary()

                return letter

class HangmanFrequencySolver(HangmanSolver):

    def __init__(self, game, dictionary):
        super(HangmanFrequencySolver, self).__init__(game, dictionary)
        self.update_symbols()

    def update_symbols(self):
        hint = self.game.get_hint()
        guessed = self.game.get_guessed()
        self.symbols = {}
        for word in self.dictionary:
            #count each letter in the word ONCE
            for letter in set(word):
                if letter in hint: continue
                if letter in guessed: continue
                if not letter in self.symbols:
                    self.symbols[letter] = 0
                self.symbols[letter] += 1

    def guess(self):
        word_length = len(self.game.get_hint())
        options = [(w, self.symbols[w]) for w in self.symbols]
        #choose the letter that is most likely to be in the word
        options.sort(key=lambda x: -x[1])
        if self.game.guess(options[0][0]) == 0:
            self.remove_letter_from_dictionary(options[0][0])
        self.update_dictionary()
        self.update_symbols()
        return options[0][0]

