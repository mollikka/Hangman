from random import Random
from math import log2

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

class HangmanRandomSolver(HangmanSolver):

    def __init__(self, game, dictionary, random_seed = None):
        super(HangmanRandomSolver, self).__init__(game, dictionary)
        self.letters = list(set(l for word in self.dictionary for l in word))
        self.rng = Random(random_seed)

    def guess(self):
        letter = self.rng.choice(self.letters)
        self.game.guess(letter)
        if letter in self.game.get_hint():
            self.update_dictionary()
            self.letters = list(set(l for word in self.dictionary for l in word
                                    if not l in self.game.get_guessed()))
        else:
            self.remove_letter_from_dictionary(letter)
            self.letters.remove(letter)
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

class HangmanEntropySolver(HangmanSolver):

    def __init__(self, game, dictionary):
        super(HangmanEntropySolver, self).__init__(game, dictionary)
        self.letters = list(set(l for word in self.dictionary for l in word))

    def score(self, info_group):
        return sum([i/len(info_group) * log2(i/len(info_group))
                                    for i in info_group.values()])

    def guess(self):
        hint = self.game.get_hint()
        information_groups = {}

        for letter in self.letters:

            info_group = {}

            for word in self.dictionary:
                #if not letter in word: continue
                masked_word = "".join([i if i==letter else "_" for i in word])
                if masked_word in info_group:
                    info_group[masked_word] += 1
                else:
                    info_group[masked_word] = 1
            if len(info_group) == 0: continue
            information_groups[letter] = self.score(info_group)

        best_letter = min(information_groups, key=information_groups.get)
        #best_letters = [i for i in information_groups
        #          if information_groups[i] == information_groups[best_letter]]
        my_guess = best_letter
        amount_of_hits = self.game.guess(my_guess)

        if amount_of_hits == -1:
            raise Exception

        if amount_of_hits == 0:
            self.remove_letter_from_dictionary(my_guess)
            self.letters.remove(my_guess)
        else:
            self.update_dictionary()
            self.letters = list(set(l for word in self.dictionary for l in word
                                    if not l in self.game.get_guessed()))

        return my_guess

class HangmanInfoSolver(HangmanEntropySolver):

    def score(self, info_group):
        return info_group[max(info_group, key=info_group.get)]
