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
engine.setProperty('rate', 130)
recognizer = sr.Recognizer()

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
            return text
    except:
        Listen()

def RemovePrev():
    cmd = 'rm -frv a.exe'
    p   = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    out = p.stdout.read()

def SaveVoice(file_path, editor, lb):
    if file_path == '':
        p = 'files/'
        Speak('What name would you like me to give to the file ?')
        command = Listen()
        command = command.lower()
        command = command.replace('dot', '.')
        command = command.replace(' ', '')
        
        Speak('I am saving it as ')
        for char in command:
            Speak(char)
        Speak('Say yes to confirm and no to try again')
        cmd = Listen()
        cmd = cmd.lower()
        if 'yes' in cmd:
            path = os.path.join(p, command)
        else:
            SaveVoice(file_path, editor, lb)
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)    
    if file_path != '':
        lb.config(text = file_path)

def OpenVoice(editor, lb):
    p = 'files/'
    Speak('Which one of the following would you like me to open ?')
    files = os.listdir(p)
    for file in files:
        Speak(file)
        time.sleep(2)
    command = Listen()
    command = command.lower()
    command = command.replace('dot', '.')
    command = command.replace(' ', '')
    path = os.path.join(p, command)
    if os.path.isfile(path):
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            Path(path)
        if file_path != '':
            lb.config(text = file_path)
    else:
        Speak('Try Again')

'''
Activate voice mode
deactivate voice mode
add a for loop
initialize i to 0
include <header>
using namespace <std>
<datatype> main
'''