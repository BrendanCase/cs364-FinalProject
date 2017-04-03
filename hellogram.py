from ProducerClass import Producer

def main():
    test = Producer('/u/_junebug_', """
        S -> NP VP [1.0]
        NP -> P N [.7] | NP C NP [.3]
        VP -> V [1.0]
        P -> 'the' [.7] | 'all' [.3]
        N -> 'cats' [.4] | 'dogs' [.4] | 'rats' [.2]
        V -> 'jump' [1.0]
        C -> 'and' [.5] | 'or' [.5]""")

    for i in range(10):
        print(test.getPost())

#program entry point
if __name__ == '__main__':
    main()