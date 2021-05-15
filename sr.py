import subprocess
import os
import time
import sys
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr
import textdistance
from spellchecker import SpellChecker

engine = pyttsx3.init()
engine.setProperty('rate', 130)
recognizer = sr.Recognizer()
spell = SpellChecker()
spell.word_frequency.load_text_file('assets/vocab.txt')
vocab =  set(open('assets/vocab.txt').read().split(','))

def Correction(command):
    words = command.split(' ')
    print(words)
    ans = ''
    for word in words:
        if word in vocab:
            ans = ans + word + " "
            continue
        else:
            ans = ans + spell.correction(word) + ' '
    return ans

def Speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def Listen():
    try:
        with sr.Microphone(device_index = 2) as source:
            print('Speak Now')
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source,timeout=10)
            text = recognizer.recognize_google(voice)
            text = text.lower()
            text = Correction(text)
            return text
    except:
        Listen()

def RemovePrev():
    cmd = 'rm -frv a.exe'
    p   = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    out = p.stdout.read()
