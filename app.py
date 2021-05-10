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
from threading import *

Font = ("Comic Sans MS", "10", "normal")
Bfont = ("Comic Sans MS", "10", "bold")
file_path = ''
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
        Speak("Can't hear")
        Listen()

def Action():
    command = Listen()
    if command is not None:
        command = command.lower()
    else:
        return
    print(command)

    if 'mute' in command:
        command = Listen()
        i = 0
        while 'start' not in command:
            command = Listen()
            if command is not None:
                command = command.lower()
            else:
                pass
            Speak('Waiting')
            i+=1
    elif 'open' and 'voice' in command:
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
            Open_via_Voice(path)
        else:
            Speak('Try Again')

    elif 'save' in command:
        Save()
    elif 'open' in command:
        Open()

    elif 'compile' in command:
        Compile()
        Speak('Compiled successfully')
    elif 'close' in command:
        Speak('Exiting....')
        os._exit(0)
    elif 'run' or ('compile' and 'run') in command:
        Run()
        Speak('Compiled and Ran successfully')
    else:
        return

    
def multi_thread():
    t = Thread(target = Start)
    t.start()


def Start():
    while True:
        Action()

def Path(path):
    global file_path
    file_path = path

def Open():
    path = askopenfilename(filetypes = [('C++ Files', '*.cpp')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        Path(path)
    if file_path != '':
        lb.config(text = file_path)

def Open_via_Voice(path):
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        Path(path)
    if file_path != '':
        lb.config(text = file_path)


def Save():
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
            Save()
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)    
    if file_path != '':
        lb.config(text = file_path)

def Compile():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    code_output.insert('1.0', "Compiling...")
    command = ['g++', file_path]
    inp = code_input.get('1.0', END)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
    a, error = process.communicate()
    code_output.delete('1.0', END)
    code_output.insert('1.0',  error)

def Run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    code_output.insert('1.0', "Running...")
    command = ['g++', file_path]
    inp = code_input.get('1.0', END)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
    a, error = process.communicate()
    p = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
    code = editor.get('1.0', END)
    if "cin" or "scanf" in code:
        inp = inp.encode('ascii')   
        p.stdin.write(inp)
    output, err = p.communicate()
    # print(type(p.stdout))
    # print(p.stdout)
    # print(output)
    code_output.delete('1.0', END)
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)

def ConfigPos(event):
    pos = "Line: "
    pos = pos + editor.index(INSERT)
    pos = pos.replace('.', ' | Char: ')
    pos_lb.config(text = pos)

# def multiple_yview(x, y):
#     editor.yview(x, y)
#     code_input.yview(x, y)
#     code_output.yview(x, y)

app = Tk()
app.title('Programmophone')

logo = ImageTk.PhotoImage(Image.open("img/cpp.png").resize((30, 30), Image.ANTIALIAS))

lb = Label(app, justify = RIGHT, compound = LEFT, padx = 10, text = "newfile.cpp",  font = Bfont, image = logo)
lb.pack() 

header = Menu(app)
header.add_command(label='Open', command=Open)
header.add_command(label='Save', command=Save)
header.add_command(label='Compile', command=Compile)
header.add_command(label='Run', command=Run)
header.add_command(label='Close', command=exit)
app.config(menu=header)

F1 = Frame(relief = SUNKEN, borderwidth=3)
pos_lb = Label(F1, padx = 10, text = "Line: 0 | Char: 0", font = Bfont)

F2 = Frame(relief = SUNKEN, borderwidth=2)
F3 = Frame(relief = SUNKEN, borderwidth=2)

lb_in = Label(F2, padx = 10, text = "Input",  font = Bfont)
lb_out = Label(F3, padx = 10, text = "Output",  font = Bfont)
lb_in.pack(side= TOP, anchor="w")
lb_out.pack(side= TOP, anchor="w")


a = Scrollbar(master = F1 , orient = 'vertical')
a.pack(side = RIGHT, fill = Y)
b = Scrollbar(master = F2 , orient = 'vertical')
b.pack(side = RIGHT, fill = Y)
c = Scrollbar(master = F3 , orient = 'vertical')
c.pack(side = RIGHT, fill = Y)

editor = Text(master = F1, width = 100, height = 27, wrap = NONE, font = Font, yscrollcommand = a.set)
editor.pack(side = TOP, fill = X)
editor.bindtags(('Text', 'post-class-bindings', '.', 'all'))
a.config(command = editor.yview)

editor.bind_class("post-class-bindings", "<KeyPress>", ConfigPos)
editor.bind_class("post-class-bindings", "<Button-1>", ConfigPos)

code_input = Text(master = F2, width = 100, height = 7, font = Font, yscrollcommand = b.set)
code_input.pack(side = TOP, fill = X)
b.config(command = code_input.yview)

code_output = Text(master = F3, width = 100, height = 7, font = Font, yscrollcommand = c.set)
code_output.pack(side = TOP, fill = X)
c.config(command = code_output.yview)


F1.pack(fill = BOTH, padx = 3, pady = 3)
pos_lb.pack(side= TOP, anchor="w")

F2.pack(fill = BOTH, padx = 3, pady = 3)
F3.pack(fill = BOTH, padx = 5, pady = 5)

multi_thread()
app.mainloop()