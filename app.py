from tkinter import *
import tkinter.ttk as ttk
import tkinter.font
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os
import sys
import time
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr
from threading import *
from LineNum import *

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
        sys.exit()
    elif 'run' or ('compile' and 'run') in command:
        Run()
        Speak('Compiled and Ran successfully')
    else:
        return

    
def multi_thread():
    t = Thread(target = Start)
    t.daemon=True
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


app = Tk()
app.geometry("1200x670-100-38")
app.title('Programmophone')
app.minsize(1200, 670)

logo = ImageTk.PhotoImage(Image.open("img/cpp.png").resize((30, 30), Image.ANTIALIAS))

lb = Label(app, justify = RIGHT, compound = LEFT, padx = 10, text = "newfile.cpp",  font = Bfont, image = logo)
lb.pack() 

header = Menu(app)
header.add_command(label='Open', command=Open)
header.add_command(label='Save', command=Save)
header.add_command(label='Compile', command=Compile)
header.add_command(label='Run', command=Run)
header.add_command(label='Close', command=sys.exit)
app.config(menu=header)

F1 = Frame(app, relief=SUNKEN, borderwidth=2)
F1.pack(side=TOP, fill=BOTH)

F1_left = CustomFrame(F1, height=27, relief = SUNKEN, borderwidth=2)
F1_left.pack(side=LEFT, fill = BOTH, padx=(0, 10))

F1_right = Frame(F1, relief=SUNKEN, borderwidth=2)
F1_right.pack(side = RIGHT, fill = BOTH, padx=(20, 0))

activity_lb = Label(F1_right, padx=10, text = "Activity Log", font=Bfont)
activity_lb.pack(anchor=W)

a = Scrollbar(F1_right, orient=VERTICAL)
a.pack(side=RIGHT, fill=Y, pady=(0,25))

activity_log = Text(F1_right, width = 50, height=27, yscrollcommand=a.set, borderwidth=2)
activity_log.pack(fill = BOTH, pady=(0,20))
activity_log.bind("<Key>", lambda e: "break")

a.config(command=activity_log.yview)

F2 = Frame(relief = SUNKEN, borderwidth=2)
F2.pack(side=BOTTOM, fill=BOTH)

F2_left = Frame(F2, relief = SUNKEN, borderwidth=2)
F2_left.pack(side=LEFT, fill=BOTH)
F2_right = Frame(F2, relief = SUNKEN, borderwidth=2)
F2_right.pack(side=RIGHT, fill=BOTH)

lb_in = Label(F2_left, padx = 10, text = "Input",  font = Bfont)
lb_out = Label(F2_right, padx=10, text = "Output",  font = Bfont)
lb_in.pack(anchor = 'w')
lb_out.pack(anchor='w')

b = Scrollbar(master = F2_left , orient = 'vertical')
b.pack(side=RIGHT, fill = Y)

editor = F1_left.text

code_input = Text(master = F2_left, font = Font, width=50, yscrollcommand = b.set, borderwidth=2)
code_input.pack(fill = BOTH, padx=2)

b.config(command = code_input.yview)

c = Scrollbar(master = F2_right , orient = 'vertical')
c.pack(side=RIGHT, fill = Y)

code_output = Text(master = F2_right, font = Font, width=170, yscrollcommand = c.set, borderwidth=2)
code_output.pack(fill = BOTH, padx=2)
code_output.bind("<Key>", lambda e: "break")

c.config(command = code_output.yview)

multi_thread()
app.mainloop()