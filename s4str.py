from producer_class import addterminals

def getGString():
    wordbank = {
        'Det' : ['the', 'this', '\'dis', 'each', 'every', 'another'],
        'Ord' : ['first', 'ninth', 'tenth', 'third', 'final'],
        'Adj' : ['yellow', 'slimy', 'gross', 'disgusting', 'hip', 'jovial', 'lovely', 'honest', 'wet', 'blotto', 'spooky'],
        'SingNoun' : ['hair', 'kiosk', 'water', 'sludge', 'pond', 'simulation', 'horse', 'syndicate', 'bulldog'],
        'SingPropNoun' : ['Jim', 'Bob', 'Adam', 'Sally', 'Jeb!', 'Cher', 'Charles Shaw', 'Leonard,' 'Gordon Ramsay'],
        'VintPast':  ['disappeared', 'agreed', 'waited', 'scratched', 'cried', 'dawdled', 'died', 'slept'],
        'VintPres' : ['vanishes', 'eats', 'stands', 'waits', 'sits', 'talks', 'sleeps', 'farts'],
        'VintFut' : ['will appear', 'will live', 'will prevail', 'will wait', 'will talk'],
        'Adverb' : ['quickly', 'properly', 'sneakily', 'simply', 'courageously', 'covertly']
    }

    skeleton_gram_str = ''.join(open('species4.pcfg'))

    for w in wordbank.keys():
        skeleton_gram_str = addterminals(skeleton_gram_str, w, wordbank[w])

    return skeleton_gram_str, wordbank