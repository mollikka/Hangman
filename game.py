class HangmanGame:

    def __init__(self, word):
        self.word = word
        self.guessed = set()
        self.bad_guess_count = 0
        self.good_guess_count = 0

    def guess(self, letter):
        if letter in self.guessed:
            return -1
        else:
            self.guessed.add(letter)
            if self.word.count(letter) == 0:
                self.bad_guess_count += 1
            else:
                self.good_guess_count += 1
            return self.word.count(letter)

    def get_bad_guess_count(self):
        return self.bad_guess_count

    def get_good_guess_count(self):
        return self.good_guess_count

    def get_hint(self):
        hint = self.word
        for i,letter in enumerate(self.word):
            if letter not in self.guessed:
                hint = hint[:i] + "_" + hint[i+1:]
        return hint

    def get_missing(self):
        return len([i for i in self.word if not i in self.guessed])

    def get_guessed(self):
        return self.guessed

if __name__ == "__main__":
    G = HangmanGame("batman")
    for letter in "aeioubmtkrn":
        print(letter, G.get_guessed())
        print(letter,"is in the word",G.guess(letter),"times.",G.get_missing(),"unsolved")
        print(G.get_hint())
