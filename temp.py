import textdistance
from spellchecker import SpellChecker
from SR import *

dict =  {"hash":'#', 'slash':'/', 'hyphen':'-', 'underscore':'_', 'backslash':'\\', 
            'less than':'<', 'greater than':'>', 'asterisk':'*', 'exclamation':'!',
             'ampersand':'&', 'modulo':'%', 'plus':'+', 'minus':'-', 'divide':'/', 'dot':'.',
              'and':'&&', ' or ':'||', 'bitwise and':'&', 'bitwise or':'|', 'xor': '^', 'percent':'%',
              'equalto':'=', 'equal to':'=', 'none':'', 'left shift':'<<', 'right shift':'>>', 'not':'!'
        }
vocab = ['a', 'add', 'ampersand', 'and', 'array', 'backslash', 'bits/stdc++.h', 'bitwise', 
         'bool', 'case', 'char', 'class', 'compile', 'condition', 'copy', 'cpp', 'd', 'dequeue', 
         'divide', 'do', 'double', 'double slash', 'else', 'else', 'else', 'enum', 'equal to', 
         'equalto', 'escape', 'evade', 'false', 'float', 'for', 'greater', 'hey', 'hyphen', 'if',
         'include', 'initialization', 'int', 'iostream', 'left', 'less', 'line', 'list', 'll', 
         'long', 'main', 'map', 'misty', 'modulo', 'multiply', 'namespace', 'newline', 'node', 
         'npos', 'null', 'open', 'or', 'pair', 'plus', 'pointer', 'private', 'public', 'py', 
         'queue', 'right', 'save', 'set', 'shift', 'slash', 'stack', 'statement', 'std', 'stdio', 
         'stdio.h', 'stdlib.h', 'string', 'substr', 'substract', 'switch', 'tab', 'than', 'tree', 
         'true', 'txt', 'underscore', 'unordered', 'unordered_map', 'unordered_set', 'unsigned',
          'using', 'void', 'while', 'xor', 'exception', 'limits', 'new', 'typeinfo']

# print(sorted(vocab))
spell = SpellChecker()
spell.word_frequency.load_text_file('vocab.txt')
while True:

   command = Listen()
   words = command.split(' ')
   print(words)
   ans = ''
   # minterm = 100

   for word in words:
      if word in vocab:
         ans = ans + word + " "
         continue
      else:
         ans = ans + spell.correction(word) + ' '

   print(ans)

   for key in dict.keys():
      if key in ans:
         ans = ans.replace(key, dict[key])

   print(ans)
