import evaluator
from length import LengthRule
from apostrophe import ApostropheRule as A
from closeword import WordRule as W

def main():
    #eval = evaluator.Evaluator([A()])
    apos = A()
    assert apos.evaluate("my dog's bone is furry'") == 2
    assert apos.evaluate("he is a dog") == 0

    clo = W(['dog', 'bone', 'my'], ['is', 'furry'])
    print('my hound is a bone')
    print(clo.evaluate('my hound is a bone'))
    print('my dog hound bark woof animal mammal')
    print(clo.evaluate('my dog hound bark woof animal mammal'))
    print('is furry')
    print(clo.evaluate('is furry'))
    print('dog bone is furry hound meat was fuzzy')
    print(clo.evaluate('dog bone is furry hound meat was fuzzy'))



if __name__ == '__main__':
    main()