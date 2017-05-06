from producer_class import addterminals

def getGString():
    wordbank = {
        'Det' : ['the', 'this', 'that', 'every', 'another', 'a single'],
        'Ord' : ['fourth', 'eleventh', 'last', 'middle', 'third', 'final', 'penultimate'],
        'Adj' : ['red', 'blue', 'winning', 'cheerful', 'elated', 'big', 'little', 'scared', 'rare', 'mucosal', 'phallic'],
        'SingNoun' : ['spider', 'bucket', 'steak', 'milk', 'computer', 'snowman', 'milksteak', 'funnel', 'babycarrot'],
        'SingPropNoun' : ['Brendan', 'Ed', 'Jimmy', 'Hannah', 'Ryan', 'Helena', 'Svetlana', 'Pamela', 'Vladimir'],
        'AdvDeg' : ['very', 'mostly', 'rarely', 'never']
    }

    skeleton_gram_str = ''.join(open('species3.pcfg'))

    for w in wordbank.keys():
        skeleton_gram_str = addterminals(skeleton_gram_str, w, wordbank[w])

    return skeleton_gram_str, wordbank