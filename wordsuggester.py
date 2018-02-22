import re, codecs
from collections import Counter

class WordSuggester:
    
    def __init__(self):
        try:
            # Needs to be done with codecs.open so that vowels with accents work as well.
            self.__words = Counter(self.tokenize(codecs.open(r"all_verb_forms.txt", encoding='utf-8').read()))
        except:
            print("Verb form list wasn't found or was invalid.")
            
    def tokenize(self, text):
        return re.findall(r'[a-záàéèíìóòúù\-\']+', text)

    def one_edit_away(self, usinput):
        # Makes a set of strings that are one edit away from usinput
        letters    = "aáàbcdeéèfghiíìjklmnoóòpqrstuúùvwxyz-\'"
        splits     = [(usinput[:i], usinput[i:])    for i in range(len(usinput) + 1)]
        insertions = [L + letter + R                for L, R in splits for letter in letters]
        deletes    = [L + R[1:]                     for L, R in splits if R]
        replaces   = [L + letter + R[1:]            for L, R in splits if R for letter in letters]
        transposes = [L + R[1] + R[0] + R[2:]       for L, R in splits if len(R)>1]
        
        return set(deletes + transposes + replaces + insertions)

    def two_edits_away(self, usinput): 
        # Makes a list of strings that are two edits away from usinput
        return (e2 for e1 in self.one_edit_away(usinput) for e2 in self.one_edit_away(e1))

    def known_words(self, words):
        # Makes a list of real word forms from a list of strings
        return set(w for w in words if w in self.__words)

    def word_in_lexicon(self, word):
        # Checks if a word is in the lexicon
        if word in self.__words:
            return True
        return False

    def suggestions(self, word):
        # Makes a list of possible spelling corrections for the unrecognized input
        suggestions = [form for form in self.known_words(self.one_edit_away(word))]
        for form in self.known_words(self.two_edits_away(word)):
            if form not in suggestions:
                suggestions.append(form)
        return suggestions
