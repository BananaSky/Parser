from collections              import namedtuple

'''
This module defines some basic data structures, namely Result and NamedResult

Result is what a bare template will return, it contains:
result    -a boolean indicating success
parsed    -a list of parsed tokens, if the parser is set to consume them
remaining -a list of tokens that were not parsed

NamedResult is returned only by Parser Classes:
it returns all of the same things as result, except it also returns a field name, which is a string

It also defines templates:
parseTemplate() -takes a function(consumer), which should return (result, consumed):
    result      -a boolean indicating success
    consumed    -the tokens that were parsed

    parseTemplate() will then handle the optional consumption of the parsed tokens,
    and then return a Result namedtuple accordingly

singleTemplate() -a layer around parseTemplate meant for making single-token parsers
    takes a comparison function (string -> bool) and a boolean determining consumption

multiTemplate() is similar to singletemplate, but takes a consumer and parses it repeatedly

'''

Result      = namedtuple('Result', ['result', 'parsed', 'remaining'])
NamedResult = namedtuple('Result', ['result', 'parsed', 'remaining', 'name'])

def parseTemplate(consumer, consume=True):
    def template(tokens):
        (result, consumed) = consumer(tokens)
        if result:
            if consume:
                return Result(result, consumed, tokens[len(consumed):])
            else:
                return Result(result, [], tokens[len(consumed):])
        else:
            return Result(result, [], tokens)
    return template

def singleTemplate(comparison, consume=True):
    def template(tokens):
        if len(tokens) > 0:
            return (comparison(tokens[0]), [tokens[0]])
        else:
            return False, []
    return parseTemplate(template, consume)

def multiTemplate(consumer, consume=True, at_least_one=False):
    def template(tokens):
        (result, consumed) = consumer(tokens)
        if result:
            parsed = consumed
            tokens = tokens[len(consumed):]
            while result and len(tokens) > 0:
                (result, consumed) = consumer(tokens)
                tokens = tokens[len(consumed):]
                if consume:
                    parsed += consumed

            return Result(True, parsed, tokens)
        else:
            return Result(not at_least_one, consumed, tokens)
    return template
