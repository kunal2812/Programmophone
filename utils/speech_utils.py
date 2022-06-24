'''This file contains utilities for Speech recognition and then further text processing'''

import pyttsx3
import speech_recognition as sr
from spellchecker import SpellChecker
from tkinter import *

recognizer = sr.Recognizer()
recognizer.energy_threshold = 650 
recognizer.phrase_threshold = 0.15
recognizer.pause_threshold = 0.5

spell = SpellChecker()
#Loading custom vocabulary for spell check based on levenshtein distance algorithm
spell.word_frequency.load_text_file('assets/vocabulary.txt')
vocab =  set(open('assets/vocabulary.txt').read().split(','))

#Dictionary for encoding the words into corresponding symbols
dict =  {"hash":'#', ' slash ':'/', 'hyphen':'-', 'underscore':'_', 'backslash':'\\', 
            'less than':'<', 'greater than':'>', 'asterisk':'*', 'exclamation':'!',
            'ampersand':'&', 'modulo':'%', 'plus':'+', 'minus':'-', 'divide':'/', 'dot':'.',
            'and':'&&', ' or ':'||', 'bitwise and':'&', 'bitwise or':'|', 'xor': '^', 'percent':'%',
            'equalto':'=', 'equal to':'=', 'none':'', 'left shift':'<<', 'right shift':'>>', "double quotes":"\"\"",
            'single quotes':"''", "double coats":"\"\"", 'single quote':"''", "double quote":"\"\"",  'not':'!', 'arrow':'->', 'comma':',',
            'semi colon':';', 'semi-colon':';',  'single coats':"''", "double coat":"\"\"", 'single coat':"''",
            'bull':'bool','vivid':'evade', 'entmen':'int main', 'see out':'print', 'cout':'print',
            'see in':'input', 'cin':'input', 'new line':'newline', 'ent':'int', 'man':'main', 'men':'main', ' space ':' ', 
            'entertain':'main', 'ant man':'main', 'write':'right', 'zero':'0', ' one ':'1', ' two ':'2', 'three':'3', 'four':'4',
            'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9', 'STD':'std', 'new line': 'newline', 'colon':':', 'ethan':'main',
            'tab':'         ', 'bracket':'brackets', 'inter':'enter', 'brake':'break', 'hasty':'hey misty', 'payal':'file', 'mister':'misty'
        }

def Correction(command):
    '''
    Checks spelling followed by symbol encoding
    '''
    words = command.split(' ')
    # print(words)
    ans = ''
    for word in words:
        if word in vocab:
            ans = ans  + word + ' '
            continue
        elif len(word) > 2:
            ans = ans  + spell.correction(word) + ' '
        else:
            ans = ans + word + ' '
    ans = Getchar(ans)
    return ans

def Getchar(ans):
    '''
    Changes words into symbols using the dictionary
    '''
    for key in dict.keys():
        if key in ans:
            ans = ans.replace(key, dict[key])
    return ans

def Speak(text):
    '''
    Simple text to speech function which first decodes some symbols that voice engine doesn't recognize and skips them, followed by generation of speech
    '''
    text = text.replace(';', ' semi colon ')
    text = text.replace('->', ' arrow operator ')    
    text = text.replace('-', ' dash ')
    text = text.replace('{', ' curly bracket open ')    
    text = text.replace('#', ' hash ')
    text = text.replace('}', ' curly bracket close ')
    text = text.replace('(', ' round bracket open ')
    text = text.replace(')', ' round bracket close ')
    text = text.replace('[', ' square bracket open ')
    text = text.replace(']', ' square bracket close ')
    text = text.replace('"', ' double quotes ')
    text = text.replace('\'', ' single quotes ')
    text = text.replace(',', ' comma ')
    text = text.replace('\\', ' backslash ')    
    text = text.replace('|', ' pipe ')
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 130) 
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
        engine.say(text)
        engine.runAndWait()
    except:
        pass
    return

def Listen():
    '''
    Speech to text based on API call
    '''
    try:
        with sr.Microphone() as source:
            print('Speak Now')
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            voice = recognizer.listen(source,timeout=3)
            text = recognizer.recognize_google(voice)
            # text = input('Enter\n')
            # print(text)
            text = text.lower()
            text = Correction(text)
            print(text)
            return text
    except:
        print("Not found")
        pass