from .ParserClass    import Parser
from .ParseTemplates import singleTemplate, multiTemplate
from copy import deepcopy

'''
Single Token Parsers:
just()     -returns a function that parses a string exactly,
wildcard() -parses single string (non whitespace),
noneOf()   -takes a list of parsers and tries them against a single string
allOf()    -does the same, but ensuring all parsers pass
subsetOf() -takes any container of characters and ensures that the string consists entirely of those characters
parseAny() -returns the result of the first matching parser out of a list of parsers it is given

Multi Token Parsers:
many()  -repeats a single parser until it fails, but returns true no matter what
until() -parsers with a second parser (wildcard by default) until it's first parser is true, optionally returning either or both results
'''

def just(string, consume=True):
    return singleTemplate(lambda s : string == s, consume)

def wildcard(consume=True):
    return singleTemplate(lambda s : True, consume)

def noneOf(parsers, consume=True):
    return singleTemplate(lambda s : True not in [p([s]).result for p in parsers], consume)

def allOf(parsers, consume=True):
    return singleTemplate(lambda s : False not in [p([s]).result for p in parsers], consume)

def subsetOf(l, consume=True):
    return singleTemplate(lambda s : False not in [c in l for c in s], consume)

def parseAny(parsers, consume=True):
    def template(tokens):
        for p in parsers:
            parse_result = p(deepcopy(tokens))
            if parse_result.result:
                if consume: return parse_result
                else: return Result(True, [], parse_result.remaining)
        return Result(False, [], tokens)
    return template

# Multi Token Parsers

def many(parser, consume=True, at_least_one=False):
    def template(tokens):
        parse_result = parser(deepcopy(tokens))
        if parse_result.result:
            return parse_result.result, parse_result.parsed
        else:
            return False, []
    return multiTemplate(template, consume, at_least_one)

def until(target_parser, parser=wildcard(), consume=True, consume_2=False):
    def template(original_tokens):
        tokens = deepcopy(original_tokens)
        parse_result = target_parser(tokens)

        parsed   = []
        parsed_2 = []
        while (not parse_result.result):
            if len(tokens) < 1:
                return Result(False, [], original_tokens)

            parse_result   = target_parser(tokens)
            parse_result_2 = parser(tokens)

            if parse_result.result:
                if consume:
                    parsed += parse_result.parsed
                tokens = tokens[len(parse_result.parsed):]

            elif parse_result_2.result:
                if consume_2:
                    parsed_2 += parse_result_2.parsed
                tokens = tokens[len(parse_result_2.parsed):]
            else:
                return Result(False, [], original_tokens)

        return Result(True, parsed_2 + parsed, tokens)
    return template
