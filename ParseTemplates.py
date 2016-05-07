from collections              import namedtuple

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
