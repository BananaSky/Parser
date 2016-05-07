from Parse import *
import nltk

punctuation = subsetOf(set(".?!()\'\","))
spaces      = subsetOf(set(" \t\n"))
word        = noneOf([spaces, punctuation])
article     = parseAny([just('a'), just('an')], False)

noun      = singleTemplate(lambda s : nltk.pos_tag([s])[0][1][0] == 'N', True)
adjective = singleTemplate(lambda s : nltk.pos_tag([s])[0][1][0] == 'J', True)
verb      = singleTemplate(lambda s : nltk.pos_tag([s])[0][1][0] == 'V', True)

def parseTags(*tags):
    def template(tokens):
        if len(tokens) >= len(tags):
            tagged_tokens = nltk.pos_tag(tokens)
            parsed = []
            for tagged_token, tag in zip(tagged_tokens, tags):
                current = tagged_token[1][:len(tag)]
                if current == tag:
                    parsed += [tagged_token[0]]
                else:
                    break
            return Result(True, parsed, tokens[len(parsed):])
        return Result(False, [], tokens)
    return template
