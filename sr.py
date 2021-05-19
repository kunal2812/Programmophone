import subprocess
import pyttsx3
import speech_recognition as sr
from spellchecker import SpellChecker
import beepy

recognizer = sr.Recognizer()
spell = SpellChecker()
spell.word_frequency.load_text_file('assets/vocabulary.txt')
vocab =  set(open('assets/vocabulary.txt').read().split(','))

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
            'tab':'         ', 'bracket':'brackets', 'inter':'enter'
        }

def Correction(command):
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
    for key in dict.keys():
        if key in ans:
            ans = ans.replace(key, dict[key])
    return ans

def Speak(text):

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

    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()
    return

def Listen():
    try:
        with sr.Microphone(0) as source:
            print('Speak Now')
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            voice = recognizer.listen(source,timeout=3)
            text = recognizer.recognize_google(voice)
            # text = input('Enter\n')
            # print(text)
            text = text.lower()
            text = Correction(text)
            # print(text)
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
