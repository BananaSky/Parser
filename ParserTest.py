from   Parse.Parsers import *
import unittest

# A set of simple unit tests to make sure everything works as advertised

def POStest():
    p = Parser([article, parseTags('N', 'V', 'RB')])
    return p.parse(['a', 'man', 'running', 'quickly'])

def test_until():
    test_parser = Parser([until(just("yes"), consume_2=False), word, word], "sentence")

    return(test_parser.external_parse("no no no yes start here").parsed == ['yes', 'start', 'here'])

test_just     = just('test')(['test']).parsed   == ['test']
test_wildcard = wildcard()(['?>><aji&']).parsed == ['?>><aji&']
test_noneof   = noneOf([just('something')])(['something']).result == False
test_allof    = allOf([just('something')])(['something']).result
test_subsetOf = subsetOf('hello')(['hell']).result
test_parseany = parseAny([just('something'), just('nothing')])(['nothing']).result
test_many     = len(many(just('hi'))(['hi', 'hi']).parsed) > 1

class ParserTest(unittest.TestCase):
    def __init__(self):
        self.tests = [test_just, test_wildcard, test_noneof, test_subsetOf,
                      test_parseany, test_many, test_until, POStest, test_allof]
    def test(self):
        inPrint = lambda s : print("\t" + s)
        if False in [t for t in self.tests]:
            print("Parser Test Failed:")
        else:
            print("Parser Test Passed")
        if not test_just:
            inPrint("just() test failed")
        if not test_wildcard:
            inPrint("wildcard() test failed")
        if not test_noneof:
            inPrint("noneof() test failed")
        if not test_subsetOf:
            inPrint("subsetOf() test failed")
        if not test_parseany:
            inPrint("parseany() test failed")
        if not test_many:
            inPrint("many() test failed")
        if not test_until:
            inPrint("until() test failed")
        if not POStest:
            inPrint("POS Test failed")
        if not test_allof:
            inPrint("allof() Test failed")

if __name__ == "__main__":
    ParserTest().test()
