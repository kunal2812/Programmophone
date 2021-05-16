import subprocess
import os
import time
import sys
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr
import textdistance
from spellchecker import SpellChecker

recognizer = sr.Recognizer()
spell = SpellChecker()
spell.word_frequency.load_text_file('assets/vocabulary.txt')
vocab =  set(open('assets/vocabulary.txt').read().split(','))
dict =  {"hash":'#', 'slash':'/', 'hyphen':'-', 'underscore':'_', 'backslash':'\\', 
            'less than':'<', 'greater than':'>', 'asterisk':'*', 'exclamation':'!',
             'ampersand':'&', 'modulo':'%', 'plus':'+', 'minus':'-', 'divide':'/', 'dot':'.',
              'and':'&&', 'or':'||', 'bitwise and':'&', 'bitwise or':'|', 'xor': '^', 'percent':'%',
              'equalto':'=', 'equal to':'=', 'none':'', 'left shift':'<<', 'right shift':'>>', 'single quote':"''",
              'single quotes':"''", "double quote":"\"\"", "double quotes":"\"\"", 'not':'!', 'arrow':'->', 'comma':',',
              'semi colon':';', 'semi-colon':';'
        }

def Correction(command):
    words = command.split(' ')
    # print(words)
    ans = ''
    for word in words:
        if word in vocab:
            ans = ans + word + " "
            continue
        else:
            ans = ans + spell.correction(word) + ' '
    ans = Getchar(ans)
    return ans

def Getchar(ans):
    for key in dict.keys():
        if key in ans:
            ans = ans.replace(key, dict[key])
    return ans

def Speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.say(text)
    engine.runAndWait()
    return

def Listen():
    try:
        with sr.Microphone(device_index = 2) as source:
            print('Speak Now')
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source,timeout=2)
            text = recognizer.recognize_google(voice)
            text = text.lower()
            text = Correction(text)
            return text
    except:
        pass

def RemovePrev():
    cmd = 'rm -frv a.exe'
    p   = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    out = p.stdout.read()

# while True:
#     try:
#         text = Listen()
#         print(Getchar(text))
#     except:
#         pass
