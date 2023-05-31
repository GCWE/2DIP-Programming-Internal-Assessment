# Imports the module used for Natural Language Processing in Python
import nltk

# Imports the module used for numerical manipulation
import numpy as np

# Uncomment if running program for the first time (for version 1)
# nltk.download("punkt")

# Imports the word stemmer, which attempts to find the "root" of a given word (i.e. strips its suffix)
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    """Separates a sentence into its individual words, numbers and punctuation"""
    return nltk.word_tokenize(sentence)

def stem(word):
    """Finds the "root" of a given word and makes them lowercase"""
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    Stems the tokenized sentence (by calling the above function) and analyses its occurrence in all the responses for a given tag.
    
    For example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bag = [0, 1, 0, 1, 0, 0, 0]
    """
    
    tokenized_sentence = [stem(word) for word in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    
    for index, word, in enumerate(all_words):
        if word in tokenized_sentence:
            bag[index] = 1.0
    
    return bag