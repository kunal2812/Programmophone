from tkinter import *
import tkinter.ttk as ttk
import tkinter.font
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os
import time
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def Speak(text):
    engine.say(text)
    engine.runAndWait()

def Listen():
    try:
        with sr.Microphone(device_index = 2) as source:
            print('Speak Now')
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source,timeout=10)
            text = recognizer.recognize_google(voice)
            return text
    except:
        print("Can't hear")

def Action():
    command = Listen()
    command = command.lower()
    print(command)
    if 'compile' in command:
        Compile()
    elif 'run' or ('compile' and 'run') in command:
        Run()
    
    
