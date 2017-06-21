from re import compile as regex
from random import choice

from game import HangmanGame
from solver import HangmanSolver
from solver import HangmanFrequencySolver

re = regex("^[a-zåäö]+$")

finnish_words = open("/usr/share/dict/finnish","r").readlines()
finnish_words = [w.lower().strip() for w in finnish_words if re.match(w)]

english_words = open("/usr/share/dict/american-english","r").readlines()
english_words = [w.lower().strip() for w in english_words if re.match(w)]

def play(word, words, solver, verbose=True):

    G = HangmanGame(word)
    H = solver(G, words)

    if verbose:
        print("Playing Hangman!")
        print(G.get_hint())
        print()
    while G.get_hint().count("_"):
        if verbose:
            dictionary = H.get_dictionary()
            print("Dictionary contains",len(dictionary),"words")
            if len(dictionary) < 15:
                for word in dictionary:
                    print(word)
            print(G.get_hint())
        guess = H.guess()
        if verbose:
            print("Guessing", guess)
            print(G.get_hint())
            print()

    if verbose:
        print("The word is",G.get_hint())
        bad_guesses = G.get_guessed() - set(G.get_hint())
        print("Guessed",len(G.get_guessed()),"times with",len(bad_guesses),
                "bad guesses (",",".join(list(bad_guesses)),")")

    return G

def find_worst_words(words, solver):
    worst_words = {}

    for i,word in enumerate(words):
        G = play(word, words, solver, False)
        score = G.get_bad_guess_count()
        if not len(word) in worst_words or worst_words[len(word)][0] < score:
            worst_words[len(word)] = (score, word)

        if i%250 == 0:
            print(i,"words evaluated")
            for i in sorted(worst_words):
                print(i, worst_words[i][0], worst_words[i][1])
            print()
    print(i,"words evaluated")
    for i in sorted(worst_words):
        print(i, worst_words[i][0], worst_words[i][1])

if __name__ == "__main__":

    find_worst_words(finnish_words, HangmanFrequencySolver)
