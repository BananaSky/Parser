from re             import findall # used only for tokenization
from copy           import deepcopy
from ParseTemplates import *

'''
Defines a Parser class and a tokenize() function

Parser is a formal version of bare parsers, mostly in that it is named
It takes a list of parsers, and parses them in sequence
It also takes a string(name), which it returns with NamedResult
'''

def tokenize(sentence):
    return findall(r"[\w']+|[.,!?;]", sentence)

class Parser(object):
    def __init__(self, parsers=[], name=""):
        self.parsers = parsers
        self.name    = name

    def external_parse(self, sentence):
        return self.parse(tokenize(sentence))

    def parse(self, original_tokens):
        tokens = deepcopy(original_tokens)
        parsed = []

        for parser in self.parsers:
            parseResult = parser(deepcopy(tokens))
            if parseResult.result:
                parsed += parseResult.parsed
                tokens =  parseResult.remaining
            else:
                return NamedResult(False, [], tokens, self.name)
        return NamedResult(True, parsed, tokens, self.name)
