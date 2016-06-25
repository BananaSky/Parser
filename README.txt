Parser
A small python library for parsing, similar to haskell's parsec

Usage is mostly defined in ParserTest.py, but the entire repository is only ~200 lines, so there's very little documentation so far

Here is a short example of how the package works:

  lucas@Strain-11:~/Desktop$ python3
  Python 3.4.3+ (default, Oct 14 2015, 16:03:50)
  [GCC 5.2.1 20151010] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> from Parser import *
  >>> word_parser = Parser([word], 'word_parser')
  >>> punc_parser = Parser([punctuation], 'punc_parser')
  >>> word_parser(['something'])
  Result(result=True, parsed=['something'], remaining=[], name='word_parser')
  >>> word_parser.external_parse('something')
  Result(result=True, parsed=['something'], remaining=[], name='word_parser')
  >>> # notice the lack of square brackets when external parse is used
  ...
  >>> combined_parser = Parser([word_parser, punc_parser], 'combined')
  >>> combined_parser(['hello', '!'])
  Result(result=True, parsed=['hello', '!'], remaining=[], name='combined')
  >>> combined_parser.external_parse('hello!')
  Result(result=True, parsed=['hello', '!'], remaining=[], name='combined')
  >>> # external parse will tokenize strings for you
  ...
  >>> # if nltk is installed, and all of the corpus is downloaded, you can parse by noun or other parts of speech
  ...
  >>> # ex: noun(token) or Parser([noun], 'noun_parser')
  ...
  >>> # parseTags() takes a list of POS tags and attempts to parse them. This is better, as most tagging is context dependent
  ...
  >>> # raw parsers like noun() or word() do similar things to the full parser class, but return a Result Object instead of a NamedResult
  ... # they also do not tokenize strings
  ... # single token parsers (like word or noun), work on a single token.
  ... # but multi token parsers, like many(word) will work on a list of tokens:
  ...
  >>> many(word)['this', 'is', 'a', 'sentence']
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: 'function' object is not subscriptable
  >>> many(word)(['this', 'is', 'a', 'sentence'])
  Result(result=True, parsed=['this', 'is', 'a', 'sentence'], remaining=[])
  >>> # both multi-token and single token parsers can be used in the Parser object
  ...
  >>> sentence_parser = Parser([many(word), punctuation], 'sentence')
  >>> sentence_parser.external_parse('this is a sentence.')
  Result(result=True, parsed=['this', 'is', 'a', 'sentence', '.'], remaining=[], name='sentence')
  >>> # the full list of parsers is available in Parser/Parse/Parsers
  ... # remind me to make better file paths
  ...
  >>>
