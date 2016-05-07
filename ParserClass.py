from re             import findall # used only for tokenization
from copy           import deepcopy
from ParseTemplates import *

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
