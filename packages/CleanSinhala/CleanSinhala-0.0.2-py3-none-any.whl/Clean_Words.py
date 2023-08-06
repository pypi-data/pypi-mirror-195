
def simplify(word):    
    simplify_words={
        'මූහූදට':'මුහුදට',
        U'\U0001F622':'sad',
        'පතුම්':'පැතුම්',
        'Chanaka':'Eranga'
    }
    # def tokenization(text):
    #     tokens = nltk.word_tokenize(text)
    #     return tokens
    try:
        return simplify_words[word]
    except KeyError:
        return word

    
   