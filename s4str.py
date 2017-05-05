from producer_class import addterminals

def getGString():
    wordbank = {
        'Det' : ['the', 'this', '\'dis', 'each', 'every', 'another'],
        'Ord' : ['first', 'ninth', 'tenth', 'third', 'final'],
        'Adj' : ['yellow', 'slimy', 'gross', 'disgusting', 'hip', 'jovial', 'lovely'],
        'SingNoun' : ['hair', 'kiosk', 'water', 'sludge', 'pond', 'simulation', 'horse'],
        'SingPropNoun' : ['Jim', 'Bob', 'Adam', 'Sally'],
        'VintPast':  ['disappeared', 'agreed', 'waited'],
        'VintPres' : ['vanishes', 'eats', 'stands'],
        'VintFut' : ['will appear', 'will live', 'will prevail'],
        'Adverb' : ['quickly', 'properly', 'sneakily']
    }

    skeleton_gram_str = ''.join(open('species4.pcfg'))

    for w in wordbank.keys():
        skeleton_gram_str = addterminals(skeleton_gram_str, w, wordbank[w])

    return skeleton_gram_str, wordbank