from Parse import *
import nltk
import string

'''
A collection of standard parsers:

punctuation()
whitespace()
letters()
lowercase()
uppercase()
digits()
hexdigits()
octdigits()
word()

Also, some basic Part Of Speech parsers:

noun()
adjective()
verb()

These Require nltk to run.

However, it is better if an entire sentence's part of speech can be matched,
as some words are context-dependent:

parseTags() will take a list of tags (represented by strings: http://www.winwaed.com/blog/2011/11/08/part-of-speech-tags/)

ParseTags can also be used to parse other things, such as cardinal numbers!
'''

punctuation = subsetOf(string.punctuation)
whitespace  = subsetOf(string.whitespace)
letters     = subsetOf(string.ascii_letters)
lowercase   = subsetOf(string.ascii_lowercase)
uppercase   = subsetOf(string.ascii_uppercase)
digits      = subsetOf(string.digits)
hexdigits   = subsetOf(string.hexdigits)
octdigits   = subsetOf(string.octdigits)
word        = noneOf([whitespace, punctuation, digits])

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
